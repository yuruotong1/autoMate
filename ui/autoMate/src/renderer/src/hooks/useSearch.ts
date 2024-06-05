import useCode from "@renderer/hooks/useCode"
import { ChangeEvent, useState } from "react"
import { codes } from "@renderer/data"
export default()=>{
    const {setData} = useCode()
    const [search, setSearch] = useState('')
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

