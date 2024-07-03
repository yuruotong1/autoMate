import { useStore } from "@renderer/store/useStore";
import { requireAlignmentPrompt, programmerPrompt } from "./prompt";
import useOpenai from "./useOpenai";
import { ProChatInstance } from "@ant-design/pro-chat";

export default () => {
  const setIsCodeLoading = useStore(state => state.setIsCodeLoading)

  const getResponse = async (chat_messages: Array<any>, id: number, revalidator: () => void, proChatRef: ProChatInstance|undefined) => {

    const response =  useOpenai(requireAlignmentPrompt(), chat_messages)
    response.then(async (res) => {
      if (res.content.includes("【自动化方案】")) {
        const chat_id = Date.now().toString()
        proChatRef!.pushChat({
          id: chat_id,
          createAt: new Date(),
          updateAt: new Date(),
          role: "assistant",
          content: "根据自动化方案生成代码中，请稍等..."
        })
        setIsCodeLoading(true)
        const programmerResponse = await useOpenai(programmerPrompt(), [{
          role: "user",
          content: res.content
        }])
        const code = programmerResponse.content.replace(/^```python/, "").replace(/^```/, "").replace(/```python$/, "").replace(/```$/, "").trim()
        proChatRef!.setMessageContent(
          chat_id,
          "根据测试方案生成的python代码如下\n```python\n" + code + "\n```"
        )
          window.api.sql('update contents set content = @content where id = @id',
          'update',
          { content: code, id})
        // 更新数据
        revalidator()
        // 关闭loading
        setIsCodeLoading(false)
      }
    })
    return response

    
  }
  return { getResponse }
}