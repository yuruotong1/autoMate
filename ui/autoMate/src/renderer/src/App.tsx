import Result from "./components/Result"
import Search from "./components/Search"
import { CodeProvider } from "./context/CodeContext"
import useShortCut from "./hooks/useShortCut"
import Error from "./components/Error"
import { useEffect, useRef } from "react"


function App(): JSX.Element {
  const mainRef = useRef<HTMLDivElement>(null)
  useEffect(()=>{
    mainRef.current?.addEventListener('mouseover', ()=>{
      window.api.setIgnoreMouseEvents(false)
    })

    document.body.addEventListener('mouseover', (e: MouseEvent)=>{
      if (e.target === document.body) {
        window.api.setIgnoreMouseEvents(true, {forward: true})
      }
    })
  }, [])
  const shortCut = useShortCut()
  shortCut.register("search", "CommandOrControl+n")
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

export default App
