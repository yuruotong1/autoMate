import { requireAlignmentPrompt, programmerPrompt} from "./prompt";
import useOpenai from "./useOpenai";
import { ProChatInstance } from "@ant-design/pro-chat";

export  default ()=>{
  const getResponse=(chat_messages: Array<any>, id:number, proChatRef: ProChatInstance|undefined, revalidator: () => void)=>{
  const messages = chat_messages.map((m) => {
    return {
      role: m.role, 
      content: m.content
    }
  })

  // 添加 system 消息
  messages.unshift({
    role: 'system',
    content: requireAlignmentPrompt()
  });
  const response = useOpenai(requireAlignmentPrompt(), messages, (allContent)=>{
    const programmerCallBack = (chat_id: string, allContent: string) => {  
      allContent = allContent.replace(/^```python/, "").  replace(/^```/, "").replace(/```$/, "").trim()
      window.api.sql('update contents set content = @content where id = @id', 
      'update', 
      {content: allContent, id})
      proChatRef!.setMessageContent(chat_id, "代码已经生成完毕！")
      revalidator()

  }
  if (allContent.includes("【自动化方案】")) {
    const chat_id = Date.now().toString()
    proChatRef!.pushChat({
      id: chat_id,
      createAt: Date.now(),
      updateAt: Date.now(),
      role: "assistant",
      content: "请稍等，我正在生成自动化代码..."
    })
    useOpenai(programmerPrompt(), [{
      role: "user",
      content: allContent
    }], (allContent)=>{
      programmerCallBack(chat_id, allContent)
    })
  } else {
    console.log("Response does not contain '【自动化方案】'");
  }
  })
  return response
  }
  return {getResponse}
  
}

