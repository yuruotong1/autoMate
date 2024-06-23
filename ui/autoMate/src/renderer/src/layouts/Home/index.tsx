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
  const config = useStore(state => state.config)
  window.api.shortCut(config.shortCut)
  useEffect(()=>{
    setIgnoreMouseEvents(mainRef as MutableRefObject<HTMLDivElement>)
    // //为开发方便，临时代码
    // window.api.openConfigWindow()
   
  }, [])

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

