import "./chat-page.scss"
import { Button } from 'antd';
import Chat from "@renderer/components/Chat"
import CodeEditor from "@renderer/components/CodeEditor"
import { localServerBaseUrl } from "@renderer/config";
import { useStore } from "@renderer/store/useStore";
import { useTheme } from "antd-style";
export default function Interactive() {
    const code = useStore(state => state.code)
    const theme = useTheme();
    return (
        <div className="chat-page">
            <div className='chat' style={{ background: theme.colorBgLayout }}>
                <Chat />
            </div>
            <div className='code'>
                <CodeEditor/>
                <Button onClick={async () => {
                    try {
                        const res = await fetch(localServerBaseUrl + "/execute", {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                code: code
                            })
                        });
                        const data = await res.json();
                        
                        console.log("run_result", data);
                    } catch (error) {
                        console.error('Error fetching data:', error);
                    }
                }}>运行</Button>
            </div>
        </div>
    )
}
