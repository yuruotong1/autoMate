import { useStore } from "@renderer/store/useStore";
import { requireAlignmentPrompt, programmerPrompt} from "./prompt";
import useOpenai from "./useOpenai";

export  default ()=>{
  const setCode = useStore(state=>state.setCode)
  const setChatMessages = useStore(state=>state.setChatMessage)
  const chatMessages = useStore(state=>state.chatMessages)
  const getResponse=(chat_messages: Array<any>)=>{
    // const setCode = useStore(state=>state.setCode)
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
    const programmerCallBack = (allContent: string) => {  
      allContent = allContent.replace(/^```python/, "").replace(/^```/, "").replace(/```$/, "").trim()
      setCode(allContent)
      chatMessages.pop()  
      setChatMessages([...chatMessages, {
        id: Date.now().toString(),
        createAt: Date.now(),
        updateAt: Date.now(),
        role: "assistant",
        content: "自动化代码生成成功，请在右侧查看代码"
      }])

  }
  if (allContent.includes("【自动化方案】")) {
    setChatMessages([...chatMessages, {
      id: Date.now().toString(),
      createAt: Date.now(),
      updateAt: Date.now(),
      role: "assistant",
      content: "请稍等，我正在生成自动化代码..."
    }])
    useOpenai(programmerPrompt(), [{
      role: "user",
      content: allContent
    }], programmerCallBack)
  } else {
    console.log("Response does not contain '【自动化方案】'");
  }
  })
  return response
  }
  return {getResponse}
  
}

