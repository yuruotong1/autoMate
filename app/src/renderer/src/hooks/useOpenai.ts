
import { localServerBaseUrl } from "@renderer/config"
export default async (systemPrompt: string, chatMessages: Array<Record<string, any>>) => {
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

    const response = await fetch(localServerBaseUrl + "/llm", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({messages, isStream: false })
    })
    return response.json()
}