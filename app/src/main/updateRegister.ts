import { BrowserWindow } from "electron"
import { autoUpdater } from "electron-updater"

export default (win: BrowserWindow) => {
    //自动下载更新
    autoUpdater.autoDownload = false
    //退出时自动安装更新
    autoUpdater.autoInstallOnAppQuit = true
    autoUpdater.removeAllListeners()
    autoUpdater.on('update-available', (_info) => {
        win.webContents.send('updateInfo', `发现新的版本!}`)
        autoUpdater.downloadUpdate()
    })

    //没有新版本时
    autoUpdater.on('update-not-available', (_info) => {
        win.webContents.send('updateInfo', '当前为最新版本')
    })

    autoUpdater.on('update-downloaded', async () => {
        win.webContents.send('updateInfo', `下载完成，重启软件完成更新！`)

    });

    // 监听下载进度
    autoUpdater.on('download-progress', (progress) => {
        win.webContents.send('updateInfo', `发现新的版本，下载进度: ${progress.percent}%`)
    })

    //更新发生错误
    autoUpdater.on('error', (_info) => {

        win.webContents.send('updateInfo', `软件更新失败，重试中...`)
    })
}