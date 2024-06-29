import "./chat-page.scss"
import { Button } from 'antd';
import Chat from "@renderer/components/Chat"
import CodeEditor from "@renderer/components/Chat"
export default function Interactive() {

    return (
        <div>
            <div className='chat-page'>
                <Chat />
            </div>
            <div className='code'>
                <CodeEditor />
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
