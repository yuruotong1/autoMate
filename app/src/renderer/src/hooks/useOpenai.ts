import { createOpenAI } from "@ai-sdk/openai"
import { streamText } from "ai"

export default async (systemPrompt: string, chatMessages: Array<Record<string, any>>, callback?: (allContent: string) => void) => {
    const configType = (await window.api.getConfig()) as ConfigType
    const config = JSON.parse(configType.content) as ConfigDataType
    const messages = chatMessages.map((m) => {
        return {
            role: m.role,
            content: m.content
        }
    })
    // 添加 system 消息
    messages.unshift({
        role: 'system',
        content: systemPrompt
    });
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
            let res = ""
            function push() {
                reader
                    .read()
                    .then(({ done, value }) => {
                        if (done) {
                            controller.close();
                            if (callback) {
                                callback(res);
                            }
                            return;
                        }
                        res += value;
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
    return new Response(readableStream)
}