import { localServerBaseUrl } from "@renderer/config";
import { useStore } from "@renderer/store/useStore";

export default()=>{
    const setChatMessages = useStore(state => state.setChatMessage)
    const chatMessages = useStore(state => state.chatMessages)
    const runCode = async function (code: string) {
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
    
    setChatMessages([...chatMessages,
    {
        role: "coder",
        content: "代码运行结果如下：" + JSON.stringify(data),
        createAt: new Date().getTime(),
        updateAt: new Date().getTime(),
        id: new Date().getTime().toString()
    }])
}

    return { runCode }
}