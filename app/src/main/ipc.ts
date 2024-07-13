import {app, ipcMain, IpcMainEvent } from "electron"
import { getWindowByName, getWindowByEvent} from "./windows"
import { autoUpdater } from 'electron-updater'


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

ipcMain.on('checkUpdate', (event) => {
    //自动下载更新
    autoUpdater.autoDownload = false
    //退出时自动安装更新
    autoUpdater.autoInstallOnAppQuit = true
    const win = getWindowByEvent(event);
    autoUpdater.checkForUpdates();
    win.webContents.send('updateInfo', `正在检查更新...`)
    autoUpdater.on('update-available', (_info) => {
        win.webContents.send('updateInfo', `发现新的版本!}`)
        autoUpdater.downloadUpdate()
        })

    //没有新版本时
  autoUpdater.on('update-not-available', (_info) => {
    win.webContents.send('updateInfo', '当前为最新版本')
  })

    autoUpdater.on('update-downloaded', async () => {
        win.webContents.send('updateInfo', `下载完成，请重启程序完成更新！`)
    });

      // 监听下载进度
  autoUpdater.on('download-progress', (progress) => {
    win.webContents.send('updateInfo', `发现新的版本，下载进度: ${progress.percent}%`)
  })

    //更新发生错误
    autoUpdater.on('error', (info) => {
        win.webContents.send('updateInfo', `软件更新失败,消息为：${info.message}\n请手动下载最新版本\nhttps://github.com/yuruotong1/autoMate/releases`)
      })
    
})