import { Form, useLoaderData, useRevalidator, useSubmit } from "react-router-dom"
import "./content.scss"
import CodeEditor from "@renderer/components/CodeEditor"
import { Button } from "antd"
import { useState } from "react"
import useRunCode from "@renderer/hooks/useRunCode"


export const Content = () => {
    const { content, categories, search } = useLoaderData() as {
        content: ContentType
        categories: CategoryType[]
        search: string
    }
    const revalidator = useRevalidator();
    const submit = useSubmit()
    const [open, setOpen] = useState(false);
    const { runCode } = useRunCode()
    return (
        <Form method="PUT">
            <main className="content-page" key={content.id}>
                <input name="id" type="text" defaultValue={content.id} hidden></input>
                <input autoFocus defaultValue={content.title} name="title" onChange={(e) => {
                    submit(e.target.form)
                }} />
                <div className="flex justify-between">
                    <select name="category_id" value={content.category_id} onChange={(e) =>
                        submit(e.target.form)
                    }>
                        <option value="0">未分类</option>
                        {categories.map((category) => (
                            <option key={category.id} value={category.id}>{category.name}</option>
                        ))}
                    </select>
                    <Button onClick={async () => {
                       setOpen(true)
                       const code_content = (await window.api.sql(`select * from contents where id = ${content.id}`, "findOne")) as ContentType
                       const code = code_content.content
                       runCode(code)
                    }}>运行</Button>
                </div>
                <CodeEditor
                    open={open}
                    setOpen={setOpen}
                    id={content.id}
                    defaultValue={content.content}
                    revalidator={() => revalidator.revalidate()}
                    search={search}
                />
            </main>
        </Form>
    )
}