import { IpcMainInvokeEvent, dialog } from "electron"
import { ipcMain } from "electron"
import { getWindowByName } from "./windows"
import { findOne } from "./db/query"
const { app, globalShortcut } = require('electron')

ipcMain.handle("shortcut", (_event: IpcMainInvokeEvent) => {
  // react 严格模式会执行两次，可能会导致快捷键重复注册，这里在注册前会删除旧快捷键
  return registerSearchShortCut()
  
})


export function registerSearchShortCut(){
  globalShortcut.unregisterAll()
  const ret = findOne(`select * from config where id=1`) as {content: string}
  const shortcut = JSON.parse(ret.content).shortcut as string
  if (shortcut && globalShortcut.isRegistered(shortcut)){
    dialog.showErrorBox('提示', '快捷键注册失败，请更换')
    return false
  }

  const win = getWindowByName('search')
  const res =  globalShortcut.register(shortcut, () => {
    win.isVisible() ? win.hide() : win.show()
  })
  return res
}
app.on('will-quit', () => {
  // Unregister all shortcuts.
  globalShortcut.unregisterAll()
})
