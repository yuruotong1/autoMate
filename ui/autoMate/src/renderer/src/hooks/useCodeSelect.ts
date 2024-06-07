import useCode from "@renderer/hooks/useCode"
import { useCallback, useEffect, useState } from "react"
export default()=>{
    const {data, setData} = useCode()
    const [id, setId] = useState(0)
    const handleKeyEvent = useCallback((e: KeyboardEvent) => {
       // 初始没有数据，所以data.length为0 ，防止向上箭头，将数据变为-1
       if (data.length === 0) return
       switch(e.key){
        case 'ArrowUp':
            setId((id)=>{
                // 找到当前id的索引
                const index = data.findIndex((item)=>item.id === id)
                return data[index - 1]?.id || data[data.length - 1].id
            })
            break
        case 'ArrowDown':
            setId((id)=>{
                // 找到当前id的索引
                const index = data.findIndex((item)=>item.id === id)
                return data[index + 1]?.id || data[0].id
            })
            break
        case 'Enter': {
            select(id)
            break
        }
       }
       // 将 data 和 currentIndex 变化时，重新定义该函数，currentIndex会更新为最新值
    }, [data, id])

    // 选中代码块
    async function select(id: Number){
        const content = data.find((item)=>item.id == id)?.content
        setData([])
        if (content) await navigator.clipboard.writeText(content)
        window.api.hideWindow()
    }

    useEffect(() => {
        document.addEventListener('keydown', handleKeyEvent)
        // 如果 data 发生变化，先前的事件监听器会被移除，然后再添加新的监听器，以确保使用最新的 data
        // 如果不移除，data变化会不停添加监听器 
        return () => {
            document.removeEventListener('keydown', handleKeyEvent)
        }
    }, [handleKeyEvent])
    // 当输入数据变化时，将当前索引重置为0
    useEffect(() =>  setId(0), [data])
    return {data, id, select}
}

