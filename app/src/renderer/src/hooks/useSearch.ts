
import { ChangeEvent } from "react"
import { useStore } from "@renderer/store/useStore"
export default()=>{
    const setData = useStore((state)=>state.setData)
    const setSearch = useStore((state)=>state.setSearch)
    const handleSearch = async (e: ChangeEvent<HTMLInputElement>) => {
      let inputValue = e.target.value ? e.target.value : "#####@@@@@@@@@@!$%^&&"
      setSearch(e.target.value)
      const data = await window.api.sql(
          `select * from contents where title like @content`,
        'findAll', 
        {content: `%${inputValue}%`})
      
      setData(data as ContentType[])
    }
    return {handleSearch}
}

