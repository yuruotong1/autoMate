import { useStore } from "@renderer/store/useStore"

function Error(){
    const {error} = useStore()
    if (!error) return <></>
    return <><div className="bg-red-600 text-white">{error}</div></>
}

export default Error

