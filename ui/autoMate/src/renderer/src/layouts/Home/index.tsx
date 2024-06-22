import Result from "@renderer/components/Result"
import Search from "@renderer/components/Search"
import { CodeProvider } from "@renderer/context/CodeContext"
import useShortCut from "@renderer/hooks/useShortCut"
import Error from "@renderer/components/Error"
import { MutableRefObject, useEffect, useRef } from "react"
import useIgnoreMouseEvents from "@renderer/hooks/useIgnoreMouseEvents"


function Home(): JSX.Element {
  const mainRef = useRef<HTMLDivElement>(null)
  const {setIgnoreMouseEvents} = useIgnoreMouseEvents()
  useEffect(()=>{
    setIgnoreMouseEvents(mainRef as MutableRefObject<HTMLDivElement>)
    // //为开发方便，临时代码
    // window.api.openConfigWindow()
  }, [])
  // // 注册快捷键
  const shortCut = useShortCut()
  shortCut.register()
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

