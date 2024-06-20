import { ipcMain, IpcMainEvent } from "electron"
import { getWindow, WindowNameType } from "./windows"

ipcMain.on('openWindow', (_event: IpcMainEvent, name: WindowNameType) => {
    getWindow(name).show()
})

ipcMain.on('closeWindow', (_event: IpcMainEvent, name: WindowNameType) => {
    getWindow(name).hide() 
})
