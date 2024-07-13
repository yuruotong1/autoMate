import { useEffect, useState } from "react";

function About() {
    const [version, setVersion] = useState('');
    const [updateInfo, setUpdateInfo] = useState('');
    window.api.updateInfo((value)=>{
        setUpdateInfo(value)
    })
    useEffect(() => {
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
                <div className="text-sm mt-5">
                    {updateInfo}
                </div>
            </div>
        </main>
    );
}

export default About;