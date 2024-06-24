import {  ChatMessage, ProChat } from '@ant-design/pro-chat';
import useChat from '@renderer/hooks/useChat';
export const Chat = () => {

  return (
    <ProChat
        helloMessage={
            '<b>你好，我叫智子，你的智能Agent助手！</b><br><br>你可以输入“/”搜索行为，或者可有什么要求可以随时吩咐！'
        }
        request={async (messages) => {
            const response =  await useChat(messages)
            // 使用 Message 作为参数发送请求
            return response; // 支持流式和非流式
    }}
  />
  )
}
