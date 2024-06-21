import { useStore } from "@renderer/store/useStore"

export default() => {
    const setError = useStore(state => state.setError)
    const register = async ()=>{
        const ret = await window.api.shortCut()
        ret || setError("注册失败")
        
    }
    return {
        register
    }
}

