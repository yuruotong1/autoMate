import "./chat-page.scss"
import { Button } from 'antd';
import Chat from "@renderer/components/Chat"
import CodeEditor from "@renderer/components/Chat"
import { localServerBaseUrl } from "@renderer/config";
import { useStore } from "@renderer/store/useStore";
export default function Interactive() {
    const code = useStore(state => state.code)
    return (
        <div>
            <div className='chat-page'>
                <Chat />
            </div>
            <div className='code'>
                <CodeEditor />
                <Button onClick={async () => {
                    try {
                        const res = await fetch(localServerBaseUrl + "/", {
                            method: 'POST',
                            body: JSON.stringify({
                                code: code
                            })
                        });
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
