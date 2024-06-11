import {ipcMain, BrowserWindow} from "electron";
import { createConfigWindow } from "../config";
export const registerIpc = (win: BrowserWindow)=>{
ipcMain.on('hideWindow', () => {
    win.hide()
})

ipcMain.on('openConfigWindow', () => {
   createConfigWindow()
})
}
