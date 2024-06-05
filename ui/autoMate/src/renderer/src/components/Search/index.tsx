import useCode from "@renderer/hooks/useCode"
import { ChangeEvent, useState } from "react"
import { codes } from "@renderer/data"

export default function Search(): JSX.Element {
  const {setData} = useCode()
  const [search, setSearch] = useState('')
  const handleSearch = (e: ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value)
    setData(
      codes.filter((code) => 
        code.content.toLowerCase().includes(e.target.value.toLowerCase() || '@@@@@@')
      )
    )
  }
  return (
    <div className="bg-slate-50 p-3 rounded-lg drag" >
        <section className="bg-slate-200 p-3 rounded-lg">
            <input 
            value={search}
            onChange={handleSearch}
            className="w-full outline-none text-2xl text-slate-600 bg-slate-200" />
        </section>
        <section className="text-center text-slate-600 text-xs mt-2">autoMate</section>
    </div>
  )
}
