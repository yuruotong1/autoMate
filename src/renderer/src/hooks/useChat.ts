import { requireAlignmentPrompt } from "./prompt";
import useOpenai from "./useOpenai";

export async function useChat(chat_messages: Array<any>){
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
  const response = await useOpenai(requireAlignmentPrompt(), messages)
  return response
}

