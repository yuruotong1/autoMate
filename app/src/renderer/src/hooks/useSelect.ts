import {useStore} from "@renderer/store/useStore"
import { useCallback, useEffect } from "react"
export default()=>{
    const data = useStore((state)=>state.data) 
    const setData = useStore((state)=>state.setData)
    const search = useStore((state)=>state.search)
    const setSearch = useStore((state)=>state.setSearch)
    const selectId = useStore((state)=>state.selectId)
    const setSelectId = useStore((state)=>state.setSelectId)
    const handleKeyEvent = useCallback((e: KeyboardEvent) => {
       
       switch(e.key){
        case 'ArrowUp': {
            // 初始没有数据，所以data.length为0 ，防止向上箭头，将数据变为-1
            if (data.length === 0) return
            // 找到当前id的索引
            const index = data.findIndex((item)=>item.id === selectId)
            setSelectId(data[index - 1]?.id || data[data.length - 1].id)
            break
        }
        case 'ArrowDown':{
            // 初始没有数据，所以data.length为0 ，防止向上箭头，将数据变为-1
            if (data.length === 0) return
            // 找到当前id的索引
            const index = data.findIndex((item)=>item.id === selectId)
            setSelectId(data[index + 1]?.id || data[0].id)
            break
        }
        case 'Enter': {
            select(selectId)
            break
        }
        case 'Escape': {
            window.api.closeWindow('search')
            break
        }
       }
       // 将 data 和 currentIndex 变化时，重新定义该函数，currentIndex会更新为最新值
    }, [data, selectId])

    // 选中代码块
    async function select(id: Number){
        if (id === 0) {
            setData([])
            window.api.closeWindow('search')
            const new_id = await window.api.sql(
                `insert into contents (title, content, category_id, created_at) values ('${search}', '', 0, datetime())`, 
                "create")
            window.api.openWindow('code', `/0/content/${new_id}/${search}`)
            setSearch("")
            return
        }
        setData([])
        setSearch('')
        // if (content) await navigator.clipboard.writeText(content)
        window.api.closeWindow('search')
        const category_id = data.find((item)=>item.id == id)?.category_id
        window.api.openWindow('code', `/${category_id}/content/${id}/${search}`)
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
    useEffect(() =>  setSelectId(data[0]?.id || 0), [data])
    return {data, selectId, select}
}

