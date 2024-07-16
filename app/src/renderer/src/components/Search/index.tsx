import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@components/ui/tooltip"
import useSearch from "@renderer/hooks/useSearch"
import { SettingOne } from "@icon-park/react"
import { Button, Input } from "antd"
import { useStore } from "@renderer/store/useStore"
import { useEffect, useState } from "react"
export default function Search(): JSX.Element {
  const { handleSearch } = useSearch()
  const search = useStore((state) => state.search)
  const [version, setVersion] = useState('')
  const [updateInfo] = useState('')
  useEffect(() => {
    window.api.getVersion().then((res) => {
      setVersion(res)
    })
    window.api.updateInfo((value) => {
      if (value === '软件更新失败，重试中...') {
        window.api.checkUpdate();
      }
    })

    window.api.checkUpdate();
  }, []);
  return (
    <main className="bg-slate-50 p-3 rounded-lg drag" >
      <div className="bg-slate-200 p-3 rounded-l flex items-center gap-1 no-drag">
        <TooltipProvider delayDuration={200}>
          <Tooltip>
            <TooltipTrigger>
              <SettingOne
                theme="outline"
                size="22"
                fill="#34495e"
                strokeWidth={4}
                className="cursor-pointer"
                onClick={() => window.api.openWindow('code')}
              />
            </TooltipTrigger>
            <TooltipContent>
              <p>编辑代码</p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
        <Input
          value={search}
          placeholder="请输入常用的action名字以快速调用"
          onChange={handleSearch}
          autoFocus
        />
      </div>
      <section className="text-center text-slate-600 text-xs mt-2 no-drag select-none">
        <div>
          autoMate V{version}
          <span className="text-blue-600 cursor-pointer" onClick={() => window.api.openWindow('config')}>点击配置AI API</span>
        </div>
        {updateInfo === '成功' && <Button type="primary" onClick={() => window.api.restartApp()}>重启</Button>}
      </section>

    </main>
  )
}
