import { useStore } from "@renderer/store/useStore"
import { Alert } from "antd"
import { useEffect } from "react"

function Error(){
    const error = useStore(state => state.error)
    const setError = useStore(state => state.setError)
    useEffect(() => {   
       const id = setTimeout(() => setError(""), 10000)
       return () => clearTimeout(id)
    }, [error])
    if (!error) return <></>
    return (<main className="absolute top-0 z-10  w-full">
        <Alert message={error} type="error" showIcon />
        </main>)  

}

export default Error

