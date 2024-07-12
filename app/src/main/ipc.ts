import {app, ipcMain, IpcMainEvent } from "electron"
import { getWindowByName, getWindowByEvent} from "./windows"

ipcMain.on('openWindow', (_event: IpcMainEvent, name: WindowNameType, router_url="") => {
    const win = getWindowByName(name, router_url)
    win.show()
})

ipcMain.on('closeWindow', (_event: IpcMainEvent, name: WindowNameType) => {
    getWindowByName(name).hide() 
})

ipcMain.on('setIgnoreMouseEvents', 
    (event: IpcMainEvent, ignore: boolean, options?:{forward: boolean}) => {
    getWindowByEvent(event).setIgnoreMouseEvents(ignore, options)
 })

ipcMain.handle('getVersion', async (_event) => {
    return app.getVersion()
})