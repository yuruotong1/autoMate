import { ProChat, ProChatInstance } from '@ant-design/pro-chat';
import useChat from '@renderer/hooks/useChat';
import { useStore } from '@renderer/store/useStore';
import { useTheme } from 'antd-style';
import { useEffect, useRef } from 'react';
export default function Chat(props: {id: number, revalidator: () => void, search: string}) {
  const {id, revalidator, search} = props;
  const {getResponse} = useChat()
  const theme = useTheme();
  const chatMessages = useStore(state=>state.chatMessages)
  const setMessages = useStore(state=>state.setChatMessage)
  const proChatRef = useRef<ProChatInstance>();
  // 确保 useeffect 只执行一次
  const effectRan = useRef(false);

  useEffect(()=>{
    if (effectRan.current === false) {
    if (search) {
      proChatRef.current?.sendMessage(search)
    }
    effectRan.current = true;
  }
  }, [])
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
            const response = await getResponse(messages, id, revalidator)
            return new Response(response.content)// 支持流式和非流式
    }}
  />
  )

}
