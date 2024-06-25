import { ElectronAPI } from '@electron-toolkit/preload'

declare global {
  interface Window {
    electron: ElectronAPI
    api: {
      shortCut: () => Promise<boolean>,
      setIgnoreMouseEvents: (ignore: boolean, options?: { forward: boolean }) => void,
      openConfigWindow: () => void,
      sql: <T>(sql: string, type: SqlActionType, params?: Record<string, any>) => Promise<T>
      openWindow: (name: WindowNameType) => void,
      closeWindow: (name: WindowNameType) => void,
      initTable: () => void,
    }
  }
}
