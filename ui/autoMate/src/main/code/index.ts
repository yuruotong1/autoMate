import { app } from 'electron'
import { createWindow } from './window'
import * as ipc from './ipc'
import { registerShortCut } from './shortCut'
import ignoreMouseEvents from './ignoreMouseEvents'


app.whenReady().then(() => {
  const window = createWindow()
  ipc.registerIpc(window)
  registerShortCut(window)
  ignoreMouseEvents(window)
})


