import { StreamingTextResponse, streamText } from "ai";
import { createOpenAI } from '@ai-sdk/openai';

export async function useChat(messages: any){
  const configType =  await window.api.getConfig()
  const llm = JSON.parse(JSON.parse(configType.content).llm)

  const openai = createOpenAI({
    // custom settings, e.g.
    apiKey: llm.apiKey, // your openai key
    baseURL: llm.baseURL, // if u dont need change baseUrl，you can delete this line
    compatibility: 'compatible',
  });
  const stream = await streamText({
    model: openai(llm.model),
    messages: messages,
  });
  console.log('stream', stream)
  return new StreamingTextResponse(stream.textStream);
}

