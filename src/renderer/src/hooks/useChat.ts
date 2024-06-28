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
    compatibility: 'compatible'
  });
  const stream = await streamText({
    model: openai(config.llm.model),
    messages: [...messages],
  });
 // 获取 reader
 const reader = stream.textStream.getReader();
 const encoder = new TextEncoder();

  const readableStream = new ReadableStream({
    async start(controller) {
      function push() {
        reader
          .read()
          .then(({ done, value }) => {
            if (done) {
              controller.close();
              return;
            }
            controller.enqueue(encoder.encode(value));
            push();
          })
          .catch((err) => {
            console.error('读取流中的数据时发生错误', err);
            controller.error(err);
          });
      }
      push();
    },
  });

  return new Response(readableStream) // 支持流式和非流式
}

