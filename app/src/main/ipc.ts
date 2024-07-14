import {app, ipcMain, IpcMainEvent } from "electron"
import { getWindowByName, getWindowByEvent} from "./windows"
import { autoUpdater } from 'electron-updater'
import { shutdownServer } from "./serverUtilts"
import updateRegister from "./updateRegister"


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

ipcMain.on('restartApp', async () => {
    await shutdownServer()
    app.relaunch()
    app.quit()
})

// 检测更新
ipcMain.on('checkUpdate', (event) => {
  
    const win = getWindowByEvent(event);
    autoUpdater.checkForUpdates();
    win.webContents.send('updateInfo', `正在检查更新...`)
    
    
})

// 注册更新事件
ipcMain.on('registerUpdate', (event) => {
    const win = getWindowByEvent(event);
    updateRegister(win)
})

