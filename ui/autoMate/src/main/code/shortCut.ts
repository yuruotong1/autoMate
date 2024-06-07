import { BrowserWindow } from "electron"

const { app, globalShortcut } = require('electron')
export const registerShortCut = (win: BrowserWindow) => {
app.whenReady().then(() => {
  // Register a 'CommandOrControl+X' shortcut listener.
  const ret = globalShortcut.register('CommandOrControl+X', () => {
    win.show()
  })

  if (!ret) {
    console.log('registration failed')
  }
})

app.on('will-quit', () => {
  // Unregister all shortcuts.
  globalShortcut.unregisterAll()
})}