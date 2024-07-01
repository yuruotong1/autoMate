import { ProChat, ProChatInstance, ProChatProvider, useProChat } from '@ant-design/pro-chat';
import { useStore } from '@renderer/store/useStore';
import useChat from '@renderer/hooks/useChat';
import { useTheme } from 'antd-style';
import { useRef } from 'react';
export default function Chat(props: {id: number}) {
  const {id} = props;
  const setMessages = useStore(state=>state.setChatMessage)
  const chatMessages = useStore(state=>state.chatMessages)
  const {getResponse} = useChat()
  const theme = useTheme();
  const proChatRef = useRef<ProChatInstance>();

  return (
    <ProChatProvider>
    <ProChat
        chats={chatMessages}
        onChatsChange={(chat)=>{
          setMessages(chat)
        }}
        chatRef={proChatRef}
        style={{ background: theme.colorBgLayout }}
        // assistantMeta={{ avatar: '', title: '智子', backgroundColor: '#67dedd' }}
        helloMessage={
            <div className='text-black'>你好，我叫智子，你的智能Agent助手！我可以帮你生成自动化代码，有什么要求可以随时吩咐！</div>
        }
  
        request={async (messages) => {
            // // const proChat = useProChat()
            const response = await getResponse(messages, id, proChatRef.current)
            return response// 支持流式和非流式
    }}
  />
  </ProChatProvider>
  )

}
