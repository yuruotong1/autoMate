import { ProChat, ProChatInstance, ProChatProvider } from '@ant-design/pro-chat';
import useChat from '@renderer/hooks/useChat';
import { useStore } from '@renderer/store/useStore';
import { useTheme } from 'antd-style';
import { useRef } from 'react';
export default function Chat(props: {id: number, revalidator: () => void}) {
  const {id, revalidator} = props;
  const {getResponse} = useChat()
  const theme = useTheme();
  const proChatRef = useRef<ProChatInstance>();
  const chatMessages = useStore(state=>state.chatMessages)
  const setMessages = useStore(state=>state.setChatMessage)
  return (
    <ProChat
        chats={chatMessages}
        onChatsChange={(chat)=>{
          console.log('chat', chat)
          setMessages(chat)
        }}
        chatRef={proChatRef}
        style={{ background: theme.colorBgLayout }}
        // assistantMeta={{ avatar: '', title: '智子', backgroundColor: '#67dedd' }}
        helloMessage={
            <div className='text-black'><b>你好，我叫智子，你的AI自动化代码助手！</b>有什么要求可以随时吩咐！</div>
        }
  
        request={async (messages) => {
            const response = await getResponse(messages, id, proChatRef.current, revalidator)
            return response// 支持流式和非流式
    }}
  />
  )

}
