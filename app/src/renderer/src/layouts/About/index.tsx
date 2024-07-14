import { Button } from "antd";
import { useEffect, useState } from "react";

function About() {
    const [version, setVersion] = useState('');
    const [updateInfo, setUpdateInfo] = useState('');
   
    useEffect(() => {
        window.api.updateInfo((value)=>{
            if(value === '软件更新失败，重试中...'){
                window.api.checkUpdate();
            }
            setUpdateInfo(value)
        })

        window.api.checkUpdate();
        
        window.api.getVersion().then((res) => {
            setVersion(res)
        })
    }, []);
    
    return (
        <main className="flex items-center justify-center h-screen">
            <div className="flex flex-col items-center">
                <h1 className="text-2xl">
                    autoMate
                </h1>
                v{version}
                <div>
                <div className="text-sm mt-5 mr-5">
                    {updateInfo}
                </div>

                {updateInfo === '下载完成，重启软件完成更新！' && (
                <div>检测到新版本，点击重启完成更新！
                <Button type="primary" onClick={()=>{
                    window.api.restartApp()
                }}>重启</Button>
                </div>)}
                </div>
            </div>
        </main>
    );
}

export default About;