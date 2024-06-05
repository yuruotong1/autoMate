import useCode from "@renderer/hooks/useCode"
import { useCallback, useEffect, useState } from "react"
import styles from './styles.module.scss'
export default function Result() {
    const {data} = useCode()
    const [currentIndex, setCurrentIndex] = useState(0)
    const handleKeyEvent = useCallback((e: KeyboardEvent) => {
       // 初始没有数据，所以data.length为0 ，防止向上箭头，将数据变为-1
       if (data.length === 0) return
       switch(e.key){
        case 'ArrowUp':
            setCurrentIndex(currentIndex - 1 < 0 ? data.length - 1 : currentIndex - 1)
            break
        case 'ArrowDown':
            setCurrentIndex(currentIndex + 1 >= data.length ? 0 : currentIndex + 1)
            break
        case 'Enter':
            console.log(data[currentIndex].content)
            break
       }
       // 将 data 和 currentIndex 变化时，重新定义该函数
    }, [data, currentIndex])
    useEffect(() => {
        document.addEventListener('keydown', handleKeyEvent)
        // 如果 data 发生变化，先前的事件监听器会被移除，然后再添加新的监听器，以确保使用最新的 data
        // 如果不移除，data变化会不停添加监听器 
        return () => {
            document.removeEventListener('keydown', handleKeyEvent)
        }
    }, [handleKeyEvent])
    return (
    <main className = {styles.main}>
        {currentIndex}
        {data.map((item, index) => (
            <div key={item.id} className={currentIndex == index? styles.active : ''}>
                <p>{item.content}</p>
            </div>
        ))}

    </main>
  )
}
