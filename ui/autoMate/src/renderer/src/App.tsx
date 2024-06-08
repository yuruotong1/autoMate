import Result from "./components/Result"
import Search from "./components/Search"
import { CodeProvider } from "./context/CodeContext"
import useShortCut from "./hooks/useShortCut"
import Error from "./components/Error"


function App(): JSX.Element {
  const shortCut = useShortCut()
  shortCut.register("search", "CommandOrControl+n")
  return (
    <CodeProvider>
      <Error/>
      <Search />
      <Result />
    </CodeProvider>
  )
}

export default App
