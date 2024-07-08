import Result from "@renderer/components/Result"
import Search from "@renderer/components/Search"
import { CodeProvider } from "@renderer/context/CodeContext"
import Error from "@renderer/components/Error"
import { MutableRefObject, useEffect, useRef } from "react"
import useIgnoreMouseEvents from "@renderer/hooks/useIgnoreMouseEvents"
import { useStore } from "@renderer/store/useStore"


function Home(): JSX.Element {
  const mainRef = useRef<HTMLDivElement>(null)
  const {setIgnoreMouseEvents} = useIgnoreMouseEvents()
  window.api.initTable()
  // 注册快捷键
  window.api.shortcut()
  const setError = useStore((state)=>state.setError)
  useEffect(()=>{
    setIgnoreMouseEvents(mainRef as MutableRefObject<HTMLDivElement>)
    // //为开发方便，临时代码
    // window.api.openConfigWindow()
   
  }, [])
  window.api.getConfig().then((res)=>{
    const config  = JSON.parse(res.content) as ConfigDataType
    if (config.llm.api_key=="") {
      setError("没有检测到大模型配置信息，请“点击配置”进行配置。如有疑问可查看文档:https://s0soyusc93k.feishu.cn/wiki/JhhIwAUXJiBHG9kmt3YcXisWnec")
    }
  })

  return (
    <CodeProvider>
      <main className="relative" ref={mainRef}>
      <Error/>
      <Search />
      <Result />
      </main>
    </CodeProvider>
  )
}

export default Home

