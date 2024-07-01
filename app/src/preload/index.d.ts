import { ElectronAPI } from '@electron-toolkit/preload'
import { BrowserWindow } from 'electron'

declare global {
  interface Window {
    electron: ElectronAPI
    api: {
      shortCut: () => Promise<boolean>,
      setIgnoreMouseEvents: (ignore: boolean, options?: { forward: boolean }) => void,
      openConfigWindow: () => void,
      sql: <T>(sql: string, type: SqlActionType, params?: Record<string, any>) => Promise<T>
      openWindow: (name: WindowNameType, router_url?: string) => BrowserWindow,
      closeWindow: (name: WindowNameType) => void,
      initTable: () => void,
      getConfig: () => Promise<ConfigType>
    }
  }
}
