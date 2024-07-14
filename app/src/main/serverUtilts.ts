export async function shutdownServer(){
    await fetch('http://127.0.0.1:5000/shutdown')  
}