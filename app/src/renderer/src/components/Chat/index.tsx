import { ProChat, ProChatInstance } from '@ant-design/pro-chat';
import useChat from '@renderer/hooks/useChat';
import useRunCode from '@renderer/hooks/useRunCode';
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
  const {id, revalidator} = props;
  const { runCode } = useRunCode()

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
          setMessages(chat)
        }}
        chatItemRenderConfig={{
          contentRender: (props, defaultDom) => {
            if (props.originData!.role === 'coder' && props.originData!.originData) {
              try {
                // const resJson = JSON.parse(item?.originData?.content);
                return (<div className='flex flex-row'>
                  <Button onClick={()=>{
                    const code = props.originData!.originData.code;
                    runCode(code)
                  }}>
                    运行
                  </Button>
                  <Button className='ml-2' onClick={()=>{
                      // 更新代码
                     window.api.sql(
                      `update contents set content=@content where id=@id`, 
                      "update",
                      {
                        content: props.originData!.originData.code,
                        id
                      }
                  )
                  // 让代码展示区域重新加载
                  revalidator()
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
            const response = await getResponse(messages)
            console.log(response)
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