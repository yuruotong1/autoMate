import Result from "./components/Result"
import Search from "./components/Search"
import { CodeProvider } from "./context/CodeContext"
import useShortCut from "./hooks/useShortCut"
import Error from "./components/Error"
import { MutableRefObject, RefObject, useEffect, useRef } from "react"
import useIgnoreMouseEvents from "./hooks/useIgnoreMouseEvents"


function App(): JSX.Element {
  const mainRef = useRef<HTMLDivElement>(null)
  const {setIgnoreMouseEvents} = useIgnoreMouseEvents()
  useEffect(()=>{
    setIgnoreMouseEvents(mainRef as MutableRefObject<HTMLDivElement>)
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
function setIgnoreMouseEvents(mainRef: RefObject<HTMLDivElement>) {
  throw new Error("Function not implemented.")
}

