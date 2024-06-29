import {  ProChat } from '@ant-design/pro-chat';
import useChat from '@renderer/hooks/useChat';
import { useTheme } from 'antd-style';
export default function Chat() {
  const {getResponse} = useChat()
  const theme = useTheme();
  // const run = async ()=>{
  //   const response = await useChat([{ role: 'user', content: '你好' }])
  //   return response
  // }
  // run()
  return (
    <div style={{ background: theme.colorBgLayout }}>
    <ProChat
        helloMessage={
            <div className='text-black'>你好，我叫智子，你的智能Agent助手，有什么要求可以随时吩咐！</div>
        }
        request={async (messages) => {
            const response = await getResponse(messages)
            // 使用 Message 作为参数发送请求
            return response// 支持流式和非流式
    }}
  />
  </div>)
}
