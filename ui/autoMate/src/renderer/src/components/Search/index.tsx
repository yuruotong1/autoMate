import useSearch from "@renderer/hooks/useSearch"
import { SettingOne } from "@icon-park/react"
import { Input } from "antd"
export default function Search(): JSX.Element {
  const {handleSearch} = useSearch()
  return (
    <main className="bg-slate-50 p-3 rounded-lg drag" >
        <div className="bg-slate-200 p-3 rounded-l flex items-center gap-1 no-drag">
            <SettingOne 
              theme="outline"
              size="22"
              fill="#34495e"
              strokeWidth={4}
              className="cursor-pointer"
              onClick={()=>window.api.openWindow('code')
              }
            />
            <Input 
            placeholder="请输入内容" 
            onChange={handleSearch}
            autoFocus
            />
        </div>
        <section className="text-center text-slate-600 text-xs mt-2 no-drag select-none">
          autoMate 
          <span className="text-blue-600 cursor-pointer" onClick={()=>window.api.openWindow('config')}>点击配置</span>
        </section>
    </main>
  )
}
