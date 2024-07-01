import { BrowserWindow, IpcMainEvent, IpcMainInvokeEvent, app } from "electron"
import { OptionsType, createWindow} from "./createWindow"

export const config = {
    search: {
        id: 0,
        options: {
            initShow: true,
            hash: '',
            openDevTools: true,
        }
    },
    code: {
        id: 0,
        options: {
            initShow: true,
            width: 1300,
            height: 700,
            openDevTools: true,
            frame: true,
            transparent: false,
            hash: '/#config/category/contentList'
        }
    },
    config: {
        id: 0,
        options: {
            initShow: true,
            width: 600,
            height: 400,
            openDevTools: true,
            frame: true,
            transparent: false,
            hash: '/#config'
        }
    }

} as Record<WindowNameType, {id: number,  options: OptionsType }>
// createWindow({})

// 根据名称获取窗口
export const getWindowByName = (name: WindowNameType)=>{
   
     // 根据id取得窗口
     let win = BrowserWindow.fromId(config[name].id)
     // 避免重复点击重复创建窗口
     if (!win) {
         win = createWindow(config[name].options)
         config[name].id = win.id
     }
     return win
}


// 根据触发来源获取窗口 
export const getWindowByEvent = (event: IpcMainEvent | IpcMainInvokeEvent) => {
    return BrowserWindow.fromWebContents(event.sender)!
}


app.whenReady().then(() => {
    // getWindowByName('search')
    getWindowByName('code')
    // getWindowByName('config')

})