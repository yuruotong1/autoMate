// import useCode from "@renderer/hooks/useCode"
import { ChangeEvent } from "react"
import { codes } from "@renderer/data"
import { useStore } from "@renderer/store/useStore"
export default()=>{
    // const {setData} = useCode()
    const setData = useStore((state)=>state.setData)
    // const [search, setSearch] = useState('')
    const search = useStore((state)=>state.search)
    const setSearch = useStore((state)=>state.setSearch)
    const handleSearch = (e: ChangeEvent<HTMLInputElement>) => {
      setSearch(e.target.value)
      setData(
        codes.filter((code) => 
          code.content.toLowerCase().includes(e.target.value.toLowerCase() || '@@@@@@')
        ).slice(0, 8)
      )
    }
    return {search, handleSearch}
}

