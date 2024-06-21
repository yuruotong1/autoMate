import { IpcMainInvokeEvent } from "electron"
import { ipcMain } from "electron"
import { getWindowByName } from "./windows"
import { findOne } from "./db/query"
const { app, globalShortcut } = require('electron')

ipcMain.handle("shortCut", (_event: IpcMainInvokeEvent, type) => {

  // react 严格模式会执行两次，可能会导致快捷键重复注册，这里在注册前会删除旧快捷键，也用户注册过快捷键想修改成其他快捷键
  return registerSearchShortCut( )
  
})


function registerSearchShortCut(){
  const ret = findOne(`select * from config where id=1`) as {content: string}
  const shortCut = JSON.parse(ret.content).shortCut as string
  if (globalShortcut.isRegistered(shortCut)){
    globalShortcut.unregister(shortCut)
  }
  const win = getWindowByName('search')
  const res =  globalShortcut.register(shortCut, () => {
    win.isVisible() ? win.hide() : win.show()
  })
  return res
}
app.on('will-quit', () => {
  // Unregister all shortcuts.
  globalShortcut.unregisterAll()
})