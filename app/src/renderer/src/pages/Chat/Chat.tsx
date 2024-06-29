import {  ProChat } from '@ant-design/pro-chat';
import useChat from '@renderer/hooks/useChat';
import { useTheme } from 'antd-style';
import "./chat-page.scss"
import Code from './Code';
import { Button } from 'antd';
export const Chat = () => {
  const {getResponse} = useChat()

  const theme = useTheme();
  // const run = async ()=>{
  //   const response = await useChat([{ role: 'user', content: '你好' }])
  //   return response
  // }
  // run()
  return (
    <div className='chat-page'>
    <div style={{ background: theme.colorBgLayout }} className='chat'>
    <ProChat
        helloMessage={
            <div className='text-black'>你好，我叫智子，你的智能Agent助手，有什么要求可以随时吩咐！</div>
        }
        request={async (messages) => {
            const response = await getResponse(messages)
            console.log('response', response)
            // 使用 Message 作为参数发送请求
            return response// 支持流式和非流式
    }}
  />
  </div>
  <div className='code'>
    <Code />
    <Button onClick={async () => {
      try {
        const res = await fetch("http://127.0.0.1:5000/");
        const data = await res.json();
        console.log(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    }}>运行</Button>
  </div>
  </div>
  )
}
