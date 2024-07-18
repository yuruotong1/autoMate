import Result from "./components/Result"
import Search from "./components/Search"
import Error from "./components/Error"
import { MutableRefObject, useEffect, useRef } from "react"
import useIgnoreMouseEvents from "./hooks/useIgnoreMouseEvents"


function App(): JSX.Element {
  const mainRef = useRef<HTMLDivElement>(null)
  const {setIgnoreMouseEvents} = useIgnoreMouseEvents()
  useEffect(()=>{
    setIgnoreMouseEvents(mainRef as MutableRefObject<HTMLDivElement>)
  }, [])
  // const shortcut = useShortCut("CommandOrControl+n")
  // shortcut.register()
  return (
    <div>
      <main className="relative" ref={mainRef}>
      <Error/>
      <Search />
      <Result />
      </main>
    </div>
  )
}

export default App

