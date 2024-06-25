import {  StreamingTextResponse, streamText } from "ai";
import { createOpenAI } from '@ai-sdk/openai';
import { useStore } from "@renderer/store/useStore";

export default async (messages: any)=> {
    
    // todo从数据库中拿配置项数据
    const openai = createOpenAI({
        baseURL: config.llm.baseURL,
        apiKey: config.llm.apiKey,
      });

    const res = await streamText({
        model: openai(config.llm.model),
        messages: messages
    });
    
  return new StreamingTextResponse(res.textStream);
}