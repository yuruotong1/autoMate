import { ProChat } from '@ant-design/pro-chat';
import { useStore } from '@renderer/store/useStore';
import useChat from '@renderer/hooks/useChat';
import { useTheme } from 'antd-style';
export default function Chat() {
  const setMessages = useStore(state=>state.setChatMessage)
  const chatMessages = useStore(state=>state.chatMessages)
  const {getResponse} = useChat()
  const theme = useTheme();

  return (
    <ProChat
        chats={chatMessages}
        onChatsChange={(chat)=>{
          setMessages(chat)
        }}
        style={{ background: theme.colorBgLayout }}
        // assistantMeta={{ avatar: '', title: '智子', backgroundColor: '#67dedd' }}
        helloMessage={
            <div className='text-black'>你好，我叫智子，你的智能Agent助手！我可以帮你生成自动化代码，有什么要求可以随时吩咐！</div>
        }
        request={async (messages) => {
            const response = await getResponse(messages)
            return response// 支持流式和非流式
    }}
  />
  )

}
