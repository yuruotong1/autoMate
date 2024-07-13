import { contextBridge, ipcRenderer } from 'electron'
import { electronAPI } from '@electron-toolkit/preload'

// Custom APIs for renderer
const api = {
  shortcut: () => {
    return ipcRenderer.invoke("shortcut")
  },
  setIgnoreMouseEvents: (ignore: boolean, options?: { forward: boolean }) => {
    ipcRenderer.send("setIgnoreMouseEvents", ignore, options)
  },
  openConfigWindow: () => {
    ipcRenderer.send("openConfigWindow")
  },
  sql: (sql: string, type: SqlActionType, params={}) => {
    return ipcRenderer.invoke("sql", sql, type, params)
  },
  openWindow: (name: WindowNameType, router_url?: string) =>{
    return ipcRenderer.send("openWindow", name, router_url)
  },
  closeWindow: (name: WindowNameType) =>{
    ipcRenderer.send("closeWindow", name)
  },

  initTable: () => {
    ipcRenderer.send("initTable")
  },
  getConfig: () => {
    return (ipcRenderer.invoke("getConfig") as Promise<ConfigType>)
  },
  getVersion: () => {
    return ipcRenderer.invoke("getVersion")
  },
  checkUpdate: () => {
    ipcRenderer.send("checkUpdate")
  },
  updateInfo: (fn: (value: string) => void)=> {
    ipcRenderer.on("updateInfo", (_event, value)=> fn(value))
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
