import { useStore } from "@renderer/store/useStore"
import useSearch from "@renderer/hooks/useSearch"
import { SettingOne } from "@icon-park/react"
import { Input } from "antd"
export default function Search(): JSX.Element {
  const search = useStore((state)=>state.search)
  const {handleSearch} = useSearch()
  return (
    <main className="bg-slate-50 p-3 rounded-lg" >
        <section className="bg-slate-200 p-3 rounded-lg flex items-center gap-1">
          <button className="bg-red-500" onClick={()=>{
            window.api.sql('select * from categories', 'findAll').then((res)=>{
              console.log(res)
            })
            }}>
            查询
          </button>
            <SettingOne 
              theme="outline"
              size="22"
              fill="#34495e"
              strokeWidth={4}
              className="cursor-pointer"
              onClick={()=>window.api.openConfigWindow()
              }
            />
            <Input 
            placeholder="请输入内容" 
            value={search}
            onChange={handleSearch}
            autoFocus
            />
        </section>
        <section className="text-center text-slate-600 text-xs mt-2">autoMate</section>
    </main>
  )
}
