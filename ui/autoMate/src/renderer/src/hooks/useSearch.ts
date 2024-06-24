// import useCode from "@renderer/hooks/useCode"
import { ChangeEvent } from "react"
import { useStore } from "@renderer/store/useStore"
export default()=>{
    // const {setData} = useCode()
    const setData = useStore((state)=>state.setData)
    // const [search, setSearch] = useState('')
    const search = useStore((state)=>state.search)
    const handleSearch = async (e: ChangeEvent<HTMLInputElement>) => {
      const data = await window.api.sql(
        `select * from contents where title like @content`,
         'findAll', 
         {content: `%${e.target.value}%`})
      setData(data as ContentType[])
    }
    return {search, handleSearch}
}

