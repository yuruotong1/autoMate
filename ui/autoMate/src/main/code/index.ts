import { app } from 'electron'
import { createWindow } from './window'
import * as ipc from './ipc'
import { registerShortCut } from './shortCut'
import ignoreMouseEvents from './ignoreMouseEvents'


app.whenReady().then(() => {
  const win = createWindow()
  ipc.registerIpc(win)
  registerShortCut(win)
  ignoreMouseEvents(win) 
})


