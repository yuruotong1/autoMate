import { useStore } from "@renderer/store/useStore"
import useSearch from "@renderer/hooks/useSearch"
import { SettingOne } from "@icon-park/react"
export default function Search(): JSX.Element {
  const search = useStore((state)=>state.search)
  const {handleSearch} = useSearch()
  return (
    <div className="bg-slate-50 p-3 rounded-lg drag" >
        <section className="bg-slate-200 p-3 rounded-lg flex items-center gap-1 nodrag">
            <SettingOne 
              theme="outline"
              size="22"
              fill="#2f3542"
              strokeWidth={4}
              className="cursor-pointer"
              onClick={()=>{
                console.log("点击了设置")
                alert("设置")}}
            />
            <input 
            value={search}
            onChange={handleSearch}
            className="w-full outline-none text-2xl text-slate-600 bg-slate-200" />
        </section>
        <section className="text-center text-slate-600 text-xs mt-2">autoMate</section>
    </div>
  )
}
