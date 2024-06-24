import {ipcMain, IpcMainEvent } from "electron"
import { getWindowByName, getWindowByEvent} from "./windows"

ipcMain.on('openWindow', (_event: IpcMainEvent, name: WindowNameType) => {
    getWindowByName(name).show()
})

ipcMain.on('closeWindow', (_event: IpcMainEvent, name: WindowNameType) => {
    getWindowByName(name).hide() 
})



ipcMain.on('setIgnoreMouseEvents', 
    (event: IpcMainEvent, ignore: boolean, options?:{forward: boolean}) => {
    getWindowByEvent(event).setIgnoreMouseEvents(ignore, options)
 })