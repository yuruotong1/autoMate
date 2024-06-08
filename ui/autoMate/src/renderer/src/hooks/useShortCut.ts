import { useStore } from "@renderer/store/useStore"

export default() => {
    const setError = useStore(state => state.setError)
    const register = async (type: 'search', shortCut: string)=>{
        const ret = await window.api.shortCut(type, shortCut)
        ret || setError("注册失败")
        
    }
    return {
        register
    }
}

