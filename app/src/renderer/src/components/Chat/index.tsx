import { ProChat, ProChatInstance } from '@ant-design/pro-chat';
import useChat from '@renderer/hooks/useChat';
import { useStore } from '@renderer/store/useStore';
import { useTheme } from 'antd-style';
import { useRef } from 'react';
export default function Chat() {
  const {getResponse} = useChat()
  const theme = useTheme();
  const chatMessages = useStore(state=>state.chatMessages)
  const setMessages = useStore(state=>state.setChatMessage)
  const proChatRef = useRef<ProChatInstance>();

  return (
    <ProChat
        chats={chatMessages}
        onChatsChange={(chat)=>{
          setMessages(chat)
        }}
        chatRef={proChatRef}
        style={{ 
          background: theme.colorBgLayout, 
          height: '900px', 
          width: '100%', 
          borderRadius: '20px', 
          padding: '20px',
        }}
        helloMessage={
            <div className='text-black'><b>你好，我叫智子，你的AI自动化代码助手！</b>有什么要求可以随时吩咐！</div>
        }
  
        request={async (messages) => {
            const response = await getResponse(messages)
            if (response.status === 0 && response.code != "") {
              setTimeout(() => {
                proChatRef.current?.pushChat({
                type: 'text',
                content: response.content,
                role: 'coder',
                originData: response
              });
              
            }, 1000); // 延时1秒推送消息
          }
            return new Response(response.content)
    }}
  />
  )

}