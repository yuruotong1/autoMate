import { BrowserWindow } from "electron"
import { OptionsType, createWindow} from "./createWindow"
export type WindowNameType = 'search' | 'config'
export const config = {
    search: {
        id: 0,
        options: {}
    },
    config: {
        id: 0,
        options: {}
    }

} as Record<WindowNameType, {id: number,  options: OptionsType }>
// createWindow({})


export const getWindow = (name: WindowNameType)=>{
     // 根据id取得窗口
     let win = BrowserWindow.fromId(config[name].id)
     // 避免重复点击重复创建窗口
     if (!win) {
         win = createWindow(config[name].options)
         config[name].id = win.id
     }
     return win
}