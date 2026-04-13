"""
autoMate CLI — RPA + AI human-in-the-loop automation.

Commands
--------
  run   <task>     Describe a task in natural language; AI writes a Markdown
                   script and executes it, learning from any failures.
  exec  <name>     Run a saved script by name.
  list             List all saved scripts.
  show  <name>     Print the Markdown script.
  delete <name>    Remove a script from the library.
"""

from __future__ import annotations

import logging
import sys
from typing import Optional

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

from core import script_manager
from core.engine import Engine, RunResult, StepResult, StepStatus
from core.learner import Learner
from core.script import MarkdownStep, Script

console = Console()

logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")


# ---------------------------------------------------------------------------
# Script generation via LLM
# ---------------------------------------------------------------------------

def _generate_script(task: str, model: str, api_key: str, base_url: str) -> Script:
    """
    Ask the LLM to write a Markdown automation script for *task*.

    The LLM returns the script body directly as Markdown — no schema required.
    """
    from auto_control.llm_client import configure, run as llm_run
    from pydantic import BaseModel

    configure(base_url=base_url, api_key=api_key, model=model)

    class ScriptOutput(BaseModel):
        name: str          # snake_case identifier
        description: str   # one-sentence summary
        body: str          # full Markdown script body

    system_prompt = """You are an RPA script author for a desktop automation tool called autoMate.

Given a task description, write a Markdown automation script with:

1. A `## Steps` section listing each UI action as a numbered item.
   - End each step with an inline action hint in `[action:value]` syntax, e.g.:
     `[key:win]`  `[type:notepad]`  `[click:OK]`  `[wait:2]`  `[scroll_down]`
   - Supported actions: click, double_click, right_click, type, key, wait, scroll_up, scroll_down
   - For keys use: enter, escape, tab, ctrl+c, ctrl+v, ctrl+s, alt+f4, win, etc.
   - Use `[click:<visible text>]` to click elements by their on-screen label.
   - Only use `[click:coord=X,Y]` as a last resort if no visible text exists.

2. An optional `## Notes` section with context, fallback tips, or timing info.

3. An optional `## Code` section with a Python code block for custom steps
   (imports, waits, subprocess calls, etc.).

Keep steps minimal and human-readable. The description should be one sentence.
Return valid JSON with keys: name (snake_case), description, body (Markdown string).
"""

    messages: list = [{"role": "user", "content": task}]
    import json
    raw  = llm_run(messages, system_prompt, ScriptOutput)
    data = json.loads(raw)

    return Script(
        name        = data["name"],
        description = data.get("description", task),
        body        = data["body"],
    )


# ---------------------------------------------------------------------------
# Progress display
# ---------------------------------------------------------------------------

def _on_progress(step: MarkdownStep, result: StepResult):
    icon = {
        StepStatus.OK:       "[green]✓[/green]",
        StepStatus.SKIPPED:  "[dim]–[/dim]",
        StepStatus.TEACH_ME: "[yellow]?[/yellow]",
        StepStatus.ERROR:    "[red]✗[/red]",
    }.get(result.status, " ")
    label = step.text[:60] + ("…" if len(step.text) > 60 else "")
    console.print(f"  {icon} Step {step.index}: {label}")
    if result.message:
        console.print(f"       [dim]{result.message}[/dim]")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--api-key",  envvar="OPENAI_API_KEY",  default="",
              help="LLM API key (or set OPENAI_API_KEY)")
@click.option("--base-url", envvar="OPENAI_BASE_URL",
              default="https://api.openai.com/v1",
              help="API base URL")
@click.option("--model",    envvar="OPENAI_MODEL",    default="gpt-4o",
              help="Model name")
@click.option("--debug",    is_flag=True, help="Enable debug logging")
@click.pass_context
def cli(ctx, api_key, base_url, model, debug):
    """autoMate — AI-powered desktop automation with human-in-the-loop learning."""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    ctx.ensure_object(dict)
    ctx.obj.update(api_key=api_key, base_url=base_url, model=model)


# ---------------------------------------------------------------------------
# run
# ---------------------------------------------------------------------------

@cli.command()
@click.argument("task")
@click.option("--save/--no-save", default=True, show_default=True,
              help="Save script to library after run")
@click.option("--dry-run", is_flag=True,
              help="Generate script but do not execute")
@click.pass_context
def run(ctx, task, save, dry_run):
    """Describe a TASK; AI generates and executes the automation script."""
    cfg = ctx.obj

    with console.status("[bold cyan]Generating script…"):
        try:
            script = _generate_script(task, cfg["model"], cfg["api_key"], cfg["base_url"])
        except Exception as exc:
            console.print(f"[red]Script generation failed:[/red] {exc}")
            sys.exit(1)

    console.print(f"\n[bold]Script:[/bold] [cyan]{script.name}[/cyan]  "
                  f"— {script.description}")
    console.print(f"[dim]{len(script.steps())} steps[/dim]\n")
    console.print(Markdown(script.body))

    if dry_run:
        console.print("\n[yellow]Dry-run — not executing.[/yellow]")
        if save:
            p = script_manager.save(script)
            console.print(f"[green]Saved:[/green] {p}")
        return

    if not click.confirm("\nExecute?", default=True):
        return

    learner = Learner(print_fn=lambda msg: console.print(msg))

    def on_teach(step: MarkdownStep) -> Optional[tuple[int, int]]:
        return learner.teach(step, script=script)

    engine = Engine(on_teach=on_teach, on_progress=_on_progress)

    console.print()
    result: RunResult = engine.run(script)

    if result.success:
        console.print(f"\n[green bold]Done![/green bold] "
                      f"All {len(script.steps())} steps completed.")
    else:
        console.print(f"\n[red bold]Stopped:[/red bold] {result.error}")

    if save:
        p = script_manager.save(script)
        console.print(f"[dim]Script saved → {p}[/dim]")


# ---------------------------------------------------------------------------
# exec
# ---------------------------------------------------------------------------

@cli.command("exec")
@click.argument("name")
@click.pass_context
def exec_cmd(ctx, name):
    """Run a saved script by NAME."""
    try:
        script = script_manager.load(name)
    except FileNotFoundError as exc:
        console.print(f"[red]{exc}[/red]")
        sys.exit(1)

    console.print(f"[bold]Running:[/bold] [cyan]{script.name}[/cyan]  "
                  f"({len(script.steps())} steps)")

    learner = Learner(print_fn=lambda msg: console.print(msg))

    def on_teach(step: MarkdownStep) -> Optional[tuple[int, int]]:
        return learner.teach(step, script=script)

    engine = Engine(on_teach=on_teach, on_progress=_on_progress)
    result = engine.run(script)
    script_manager.save(script)   # persist run counts + any learned hints

    if result.success:
        console.print("\n[green bold]Done![/green bold]")
    else:
        console.print(f"\n[red bold]Stopped:[/red bold] {result.error}")


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------

@cli.command("list")
def list_scripts():
    """List all saved scripts."""
    scripts = script_manager.load_all()
    if not scripts:
        console.print("[dim]No scripts yet.  "
                      "Use [bold]automate run \"<task>\"[/bold] to create one.[/dim]")
        return

    table = Table(title="Script Library", show_lines=True)
    table.add_column("Name",      style="bold cyan")
    table.add_column("Stability", justify="center")
    table.add_column("Steps",     justify="right")
    table.add_column("Runs",      justify="right")
    table.add_column("Description")

    _style = {"stable": "green", "learning": "yellow", "draft": "dim"}

    for s in scripts:
        st = _style.get(s.stability, "")
        table.add_row(
            s.name,
            f"[{st}]{s.stability}[/{st}]",
            str(len(s.steps())),
            f"{s.success_runs}/{s.total_runs}",
            s.description or "—",
        )

    console.print(table)


# ---------------------------------------------------------------------------
# show
# ---------------------------------------------------------------------------

@cli.command()
@click.argument("name")
def show(name):
    """Print script NAME as Markdown."""
    try:
        script = script_manager.load(name)
    except FileNotFoundError as exc:
        console.print(f"[red]{exc}[/red]")
        sys.exit(1)

    console.print(Markdown(f"# {script.name}\n\n{script.body}"))


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------

@cli.command()
@click.argument("name")
@click.confirmation_option(prompt="Delete this script?")
def delete(name):
    """Delete script NAME from the library."""
    if script_manager.delete(name):
        console.print(f"[green]Deleted:[/green] {name}")
    else:
        console.print(f"[red]Not found:[/red] {name}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    cli()
