export async function shutdownServer(){
    try{
        await fetch('http://127.0.0.1:5000/shutdown')  

    // 退出时会报异常
    }catch(e){
       
    }
}