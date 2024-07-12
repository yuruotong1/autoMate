import { localServerBaseUrl } from "@renderer/config";

export default () => {

  const getResponse = async (chat_messages: Array<any>) => {
    
    const messages = chat_messages
      .filter((m) => ['assistant', 'user'].includes(m.role)) // 过滤出 role 为 assistant 和 user 的消息
      .map((m) => {
        return {
            role: m.role,
            content: m.content
        }
    })

    const response = await fetch(localServerBaseUrl + "/llm", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({messages, isStream: false })
    })
    return response.json()

    
  }
  return { getResponse }
}