import copy
from xbrain.core.chat import run

class FewShotGenerateAgent:
    def __call__(self, action_list, user_instruction):
        """
        Generate Few-Shot examples from action list and user instruction
        
        Args:
            action_list: List of actions including screenshots
            user_instruction: Optional user instruction or intent
            
        Returns:
            Formatted Few-Shot example as string
        """
        action_list_copy = copy.deepcopy(action_list)
        yield from self._process_utterance_based_sequence(action_list_copy, user_instruction)
    
    
    def _process_utterance_based_sequence(self, mixed_sequence, user_instruction):
        """Process a sequence that contains both utterances and actions"""
        from src.core.workflow_extractor import WorkflowExtractor
        
        # Extract workflow segments based on utterances
        extractor = WorkflowExtractor()
        workflow_segments = extractor.extract_workflows(mixed_sequence)
        
        # Process each workflow segment
        results = []
        
        for segment in workflow_segments:
            intent = segment['intent']
            actions = segment['actions']
            # Skip segments with no actions
            if not actions:
                continue
            # Prepare the prompt with the specific intent and overall user instruction
            messages = [{"role": "user", "content": 
                         [{"type": "text", "text": f"用户的总体目标是：{user_instruction}\n用户的当前意图是：{intent}\n动作序列如下。"}]}]
            
            # Add images
            for action in actions:
                messages[0]["content"].append(
                    {
                        "type": "text",
                        "text": f"{str({k: v for k, v in action.items() if k != 'base64_image'})}"
                    }
                )
                messages[0]["content"].append(
                    {
                        "type": "image_url", 
                        "image_url": {"url": f"data:image/png;base64,{action['base64_image']}"}
                    }
                )
            
            # Call the LLM for this segment
            segment_response = run(messages, user_prompt=think_prompt)
            
            # 提取思考过程
            thinking_process = segment_response
            
            # 立即输出思考过程
            yield thinking_process
            
            # 收集思考过程和意图，而不是立即生成few-shot示例
            results.append({
                "intent": intent,
                "thinking": thinking_process
            })
        
        # 准备所有思考过程的汇总
        all_thinking_processes = "\n\n======= 分隔线 =======\n\n".join([
            f"意图：{item['intent']}\n\n思考过程：\n{item['thinking']}" 
            for item in results
        ])
        
        # 一次性生成所有few-shot示例，同时传递用户总体目标
        combined_messages = [{"role": "user", "content": [{"type": "text", "text": f"用户的总体目标是：{user_instruction}\n\n基于以下所有思考过程，生成相应的few-shot示例集合，确保示例不偏离用户总体目标：\n\n{all_thinking_processes}"}]}]
        all_few_shots = run(combined_messages, user_prompt=few_shot_prompt)
        
        # 输出所有few-shot示例
        yield all_few_shots
        return 


think_prompt = """
# 角色
你是一位顶级的用户界面交互分析专家，擅长深度解读用户在视觉界面上的操作序列，并从中推断用户的意图、策略以及操作的有效性。

# 背景
我正在开发一个先进的多模态智能体，目标是让它能理解并执行 GUI 上的任务。为了让智能体学习人类的操作模式，我需要分析真实用户是如何通过一系列界面交互来达成目标的。这些原始操作序列往往包含探索、错误修正和冗余步骤。

# 目标
你的核心任务是**生成并输出一个详细的、叙述性的思考过程**。这个过程需要模拟你是如何分析给定的用户总体目标、当前意图以及包含截图的操作序列的。你需要在这个思考过程中，阐述你是如何识别关键UI元素（特别是鼠标交互点）、提炼用户真实意图、过滤无效操作，并最终理解核心操作步骤如何服务于用户目标的。截图主要用于在分析时理解操作发生的具体上下文和交互对象。

---

### 输入信息（你将会收到以下信息）
1.  **用户总体目标 (Overall Goal):** 用户想要最终完成的大任务。
2.  **用户当前意图 (Current Intent):** 用户在执行当前这段操作序列时，想要直接达成的子目标或阶段性目标。
3.  **操作序列 (Action Sequence):** 一个按时间排序的操作列表，每个操作包含类型、位置、值（如适用）和对应的截图。

---

### 任务指令
**请严格按照要求，你的输出应该是一个单一的、连贯的文本段落，详细地描述你的完整思考过程。不要使用项目符号、编号列表或明显的章节标题。让它读起来像一段自然流畅的内部思维独白或分析报告的草稿。这个详细的思考过程描述将作为后续生成具体 Few-Shot 案例的基础。**

**【以下是引导你进行思考的叙述性框架，请将你的分析融入这样的叙述中】**

我的分析始于对用户目标的整体把握。首先，我会明确用户希望最终达成的**总体目标**是“[此处 mentally 插入总体目标]”，以及他们当前阶段声明的**意图**是“[此处 mentally 插入当前意图]”。理解这两者之间的关系至关重要，我要判断当前的意图是否是实现总体目标的合理且必要的步骤。例如，如果总体目标是“在线购买一件特定商品”，而当前意图是“在搜索结果页筛选商品颜色”，那么这个意图显然服务于最终目标，这有助于我将后续的操作分析锚定在正确的方向上，避免偏离主题。

接着，我会仔细审视这个**当前意图**的精确性。用户提供的意图有时可能比较笼统。因此，我会结合具体的**操作序列**来验证和细化它。我会观察用户的实际动作——他们点击了什么按钮？在哪个输入框里打了字？滚动了页面的哪个部分？这些行为往往能揭示比声明更具体的意图。比如，如果意图是“查看账户详情”，但操作序列显示用户点击了“修改密码”链接并开始输入，那么我会将实际意图提炼为“开始修改账户密码”。我会阐述我是如何基于“[具体的操作细节，如点击了某个按钮、输入了特定文本]”这些证据，将初始意图修正或具体化为“[提炼后的更精确意图]”的。

在明确了更精确的用户意图后，下一步是梳理整个**操作序列**，识别并过滤掉**冗余或无效的操作**。人类的操作常常不是最优路径，可能包含重复点击、打字错误后的修正、无目的的页面滚动或短暂打开又关闭的窗口。我会寻找这些模式，比如用户可能在一个按钮上快速点击了两次，但只有一次是必要的；或者输入了一段文本，然后用退格键删掉一部分再重新输入。我会判断哪些操作对于达成刚才提炼出的精确意图并非必需，并将它们从核心序列中剥离。例如，一系列的“输入字符”和“按退格键”操作，最终如果只是为了得到一个正确的单词，我会将其合并为一次有效的“输入‘[最终单词]’”操作，并说明理由是之前的操作属于修正性质。同样，漫无目的的滚动或者点开菜单又立刻关闭的行为，若与意图无直接关联，也会被我视为干扰信息并加以忽略。

最后，在去除了干扰和冗余之后，我会聚焦于**剩余的关键操作序列**。对于这个精简后的序列中的每一步，我会进行详尽的界面和操作分析。我会明确指出**操作的类型**（是点击、输入、滚动还是其他？）。然后，借助截图和上下文信息，我会尽可能精确地描述被操作的**目标UI元素**——它是一个标有“登录”的按钮吗？还是一个带有“搜索…”占位符的文本框？或者是页面主要内容区域的滚动条？我会记录下它的视觉特征、文本标签或类型。此外，如果操作涉及具体**数值或内容**（比如输入的文本、选择的下拉选项、滚动的方向），我也会一并记录下来。例如，我会描述为：“用户点击了位于页面右上角的‘购物车’图标按钮”，或者“在标签为‘电子邮件地址’的输入框中输入了文本‘example@email.com’”，或者“向下滚动了产品列表区域，直到‘加载更多’按钮可见”。通过这样对每一个关键步骤进行分解，我就能清晰地构建出用户是如何通过与界面元素的有效交互来实现其特定意图的完整路径。这整个连贯的思考和分析过程，就构成了我对用户行为模式的深度理解。

**【请将你的实际分析内容，按照上述思考流程和叙述风格，整合成一个单一的文本段落作为输出】**
"""

few_shot_prompt = """
# 任务: 生成 Few-Shot 示例用于智能体 System Prompt

# 背景:
你已完成对用户操作序列的深度分析，并产出了一个详细的叙述性**思考过程**。该思考过程明确了用户的总体目标，提炼了具体的**操作目的 (精确意图)**，并识别出了达成这些目的所必需的、精简后的**关键动作序列**及其对应的**UI元素**和**最终状态**。

# 目标:
基于你先前生成的**思考过程**结论，为其中分析出的**每一个精确操作目的**，生成一个结构化、标准化的**Few-Shot 示例**。这些示例将直接嵌入到多模态智能体的 **System Prompt** 中，作为核心指令的一部分，指导其理解任务并模仿有效的操作模式。因此，生成的示例必须极其精确、清晰、具有普适性，并严格遵循格式。

# 输入假设:
此任务的唯一输入是你之前生成的**详细思考过程叙述文本**。你将从中提取关键信息（精确意图、关键动作、目标元素、最终状态）并进行格式化，无需重新分析原始数据。

# 输出格式要求:
请为思考过程中识别出的**每个操作目的**生成一个 JSON 对象格式的 Few-Shot 示例。如果存在多个操作目的，请将每个 JSON 对象用 `---` 分隔符清晰隔开。

**每个 Few-Shot 示例必须严格遵循以下 JSON 结构:**

```json
{
  "操作目的": "[从思考过程中提取的、已提炼的精确用户意图]",
  "演示动作序列": [
    {
      "动作": "[标准化的动作类型 (例如: CLICK, TYPE, SCROLL_DOWN, SCROLL_UP, SELECT_OPTION, HOVER, DRAG_DROP, PRESS_ENTER, PRESS_TAB)]",
      "目标": "[对UI元素的精确、可定位描述 (应包含文本标签、元素类型(如 button, input, link, checkbox, dropdown), aria-label, 或其他显著视觉/结构特征，确保智能体能大概率识别)]",
      "值": "[动作相关的具体值 (例如: TYPE 的文本内容, SELECT_OPTION 的选项文本, PRESS_KEY 的键名), 若无则省略此键]"
    },
    // ... 为该操作目的的关键、非冗余动作序列中的每一步重复此对象 ...
    {
      "动作": "[最后一个关键动作类型]",
      "目标": "[最后一个目标的精确描述]",
      "值": "[最后一个动作的值，如适用]"
    }
  ],
  "最终状态": "[描述在完成此'操作目的'后，界面上可直接观察到的、明确的结果或状态变化 (例如: '用户成功登录并跳转到个人主页', '商品列表已根据价格筛选并更新显示', '表单提交成功，页面显示确认信息')]"
}
```

--- [如果分析了多个操作目的，请在此处使用分隔符，然后开始下一个 JSON 对象]

生成关键注意事项与质量标准:
1. 忠于思考过程: 所有字段内容（操作目的、动作、目标、值、最终状态）必须直接来源于或准确对应于你先前思考过程的结论。
2. 动作标准化: 动作 字段必须使用预定义且一致的动作类型（参考格式中的示例）。这对于智能体解析指令至关重要。
3. 目标可定位性: 目标 描述是关键。它需要足够丰富和具体，以便智能体能够在不同的屏幕分辨率或微小布局变动下，通过视觉识别和 DOM 结构分析（如果可用）可靠地定位到正确的UI元素。优先使用稳定的标识符（如明确的文本标签、aria-label），辅以元素类型和必要的上下文。
4. 序列精炼: 演示动作序列 必须只包含达成 操作目的 的核心、非冗余步骤，正如在思考过程中提炼的那样。
5. 状态明确: 最终状态 需要清晰描述与 操作目的 直接相关的、可验证的界面变化结果。
6. JSON 格式严格: 输出必须是有效的 JSON 格式（每个示例一个 JSON 对象），并使用 --- 分隔符。
7. System Prompt 适用性: 产出的每一个示例都应被视为给智能体的直接指令或学习样本，因此必须是高质量、无歧义的。

请基于你已有的思考过程分析结果，立即开始生成符合上述所有要求的 Few-Shot 示例 JSON 对象。

"""