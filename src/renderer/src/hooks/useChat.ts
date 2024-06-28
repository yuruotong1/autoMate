import { useStore } from "@renderer/store/useStore";
import { requireAlignmentPrompt, programmerPrompt } from "./prompt";
import useOpenai from "./useOpenai";

export async function useChat(chat_messages: Array<any>){
  const setCode = useStore(state=>state.setCode)
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
      console.log("allContent", allContent)
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
  const response = await useOpenai(requireAlignmentPrompt(), messages, callBack)
  return response
}

