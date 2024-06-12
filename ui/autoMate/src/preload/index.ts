import { contextBridge, ipcRenderer } from 'electron'
import { electronAPI } from '@electron-toolkit/preload'

// Custom APIs for renderer
const api = {
  hideWindow: () =>{
    ipcRenderer.send("hideWindow")
  },
  shortCut: (type: 'search', shortCut: string) => {
    return ipcRenderer.invoke("shortCut", type, shortCut)
  },
  setIgnoreMouseEvents: (ignore: boolean, options?: { forward: boolean }) => {
    ipcRenderer.send("setIgnoreMouseEvents", ignore, options)
  },
  openConfigWindow: () => {
    ipcRenderer.send("openConfigWindow")
  },
  sql: (sql: string, type: SqlActionType) => {
    return ipcRenderer.invoke("sql", sql, type)
  }

}

// Use `contextBridge` APIs to expose Electron APIs to
// renderer only if context isolation is enabled, otherwise
// just add to the DOM global.
if (process.contextIsolated) {
  try {
    contextBridge.exposeInMainWorld('electron', electronAPI)
    contextBridge.exposeInMainWorld('api', api)
  } catch (error) {
    console.error(error)
  }
} else {
  // @ts-ignore (define in dts)
  window.electron = electronAPI
  // @ts-ignore (define in dts)
  window.api = api
}
