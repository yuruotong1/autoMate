import { useStore } from "@renderer/store/useStore"
import useSearch from "@renderer/hooks/useSearch"
import { SettingOne } from "@icon-park/react"
import { Input } from "antd"
import { useEffect, useRef } from "react"
export default function Search(): JSX.Element {
  const search = useStore((state)=>state.search)
  const {handleSearch} = useSearch()
  const mainRef = useRef<HTMLDivElement | null>(null)
  useEffect(()=>{
    mainRef.current?.addEventListener('mouseover', (_e: MouseEvent)=>{
      window.api.setIgnoreMouseEvents(false)
    })
    mainRef.current?.addEventListener('mouseout', (_e: MouseEvent)=>{
      window.api.setIgnoreMouseEvents(true, {forward: true})
    })
  },[])
  return (
    <main className="bg-slate-50 p-3 rounded-lg drag"  ref={mainRef}>
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
            <Input 
            placeholder="请输入内容" 
            value={search}
            onChange={handleSearch}
            autoFocus
            />
            {/* <input 
            value={search}
            onChange={handleSearch}
            className="w-full outline-none text-2xl text-slate-600 bg-slate-200" 
            autoFocus/> */}
        </section>
        <section className="text-center text-slate-600 text-xs mt-2">autoMate</section>
    </main>
  )
}
