import { useStore } from "@renderer/store/useStore"

export default() => {
    const setError = useStore(state => state.setError)
    const register = async ()=>{
        const ret = (await window.api.sql('', 'config')) as Record<string, any>
        const isBind = await window.api.shortCut(ret.shortCut)
        isBind || setError("注册失败")
        
    }
    return {
        register
    }
}

