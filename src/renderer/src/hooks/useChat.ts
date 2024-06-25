import {  streamText } from "ai";
import { createOpenAI } from '@ai-sdk/openai';

export default async (messages: any)=> {
    const configType =  await window.api.getConfig()
    const llm = JSON.parse(JSON.parse(configType.content).llm)
    // todo从数据库中拿配置项数据
    const openai = createOpenAI({
        baseURL: llm.baseURL,
        apiKey: llm.apiKey,
      });
    console.log("messages", messages)

    const res = await streamText({
        model: openai(llm.model),
        messages: messages
    });
    
  return res.textStream;
}