import { createOpenAI } from "@ai-sdk/openai";
import { StreamingTextResponse, streamText } from "ai";
// import { createOpenAI } from '@ai-sdk/openai';

export async function useChat(chat_messages: Array<any>){
  const configType =  (await window.api.getConfig()) as ConfigType
  const config = JSON.parse(configType.content) as ConfigDataType
  const messages = chat_messages.map((m) => {
    return {
      role: m.role, 
      content: m.content
    }
  })
  const openai = createOpenAI({
    apiKey: config.llm.apiKey,
    baseURL: config.llm.baseURL,
  });
  const stream = await streamText({
    model: openai(config.llm.model),
    messages: messages,
  });

  return new StreamingTextResponse(stream.textStream) // 支持流式和非流式
}

