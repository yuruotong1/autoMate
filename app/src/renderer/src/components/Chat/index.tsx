import { ProChat, ProChatInstance } from '@ant-design/pro-chat';
import useChat from '@renderer/hooks/useChat';
import { useStore } from '@renderer/store/useStore';
import { Button } from 'antd';
import { useTheme } from 'antd-style';
import { useEffect, useRef } from 'react';
export default function Chat(props: {id: number, revalidator: () => void, search: string}) {
  const {search} = props;
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
        chatItemRenderConfig={{
          contentRender: (props, defaultDom) => {
            if (props.originData?.role === 'coder') {
              try {
                // const resJson = JSON.parse(item?.originData?.content);
                return (<div className='flex flex-row'>
                  <Button onClick={()=>{
                    console.log('运行')
                  }}>
                    运行
                  </Button>
                  <Button className='ml-2' onClick={()=>{
                    console.log('应用')
                  }}>
                   应用
                  </Button>
                </div>)
                
              } catch (error) {
                return defaultDom;
              }
            }
            return defaultDom;
          }
        }}
        chatRef={proChatRef}
        style={{ background: theme.colorBgLayout }}
        // assistantMeta={{ avatar: '', title: '智子', backgroundColor: '#67dedd' }}
        helloMessage={
            <div className='text-black'><b>你好，我叫智子，你的AI自动化代码助手！</b>有什么要求可以随时吩咐！</div>
        }
  
        request={async (messages) => {
            // const response = await getResponse(messages)
            // if (response.isExistCode === 0) {
            // setTimeout(() => {
            //   proChatRef.current?.sendMessage({
            //     type: 'text',
            //     content: response.content,
            //     role: 'coder',
            //     originData: response
            //   });
            // }, 1000); // 延时1秒推送消息
            
            // }

            // return new Response(response.content)// 支持流式和非流式
            setTimeout(() => {
              proChatRef.current?.pushChat({
                type: 'text',
                content: "hello",
                role: 'coder',
                originData: "dd"
              });
            }, 1000); // 延时1秒推送消息
            return new Response("hello")
    }}
  />
  )

}