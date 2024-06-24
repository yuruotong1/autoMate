import {  streamText } from "ai";
import { createOpenAI } from '@ai-sdk/openai';

export default async (messages: any)=> {
    // todo从配置项中拿数据
    const openai = createOpenAI({
        baseURL: 'https://api.openai.com/v1',
        apiKey: '',
      });

    const res = await streamText({
        model: openai('gpt-4-turbo'),
        messages: messages
    });
    
  return res.textStream;
}