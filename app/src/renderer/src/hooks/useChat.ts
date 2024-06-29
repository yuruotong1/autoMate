import { useStore } from "@renderer/store/useStore";
import { requireAlignmentPrompt, programmerPrompt, extraCodePrompt } from "./prompt";
import useOpenai from "./useOpenai";

export  default ()=>{
  const setCode = useStore(state=>state.setCode)
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
  const callBack = (allContent: string) => {

    const programmerCallBack = (allContent: string) => {  
        allContent = allContent.replace(/^```python/, "").replace(/^```/, "").replace(/```$/, "").trim()
        setCode(allContent)

      
    }
    if (allContent.includes("【自动化方案】")) {
      useOpenai(programmerPrompt(), [{
        role: "user",
        content: allContent
      }], programmerCallBack)
    } else {
      console.log("Response does not contain '【自动化方案】'");
    }
  }
  const response = useOpenai(requireAlignmentPrompt(), messages, callBack)
  return response
  }
  return {getResponse}
  
}

