import { ElectronAPI } from '@electron-toolkit/preload'

declare global {
  interface Window {
    electron: ElectronAPI
    api: {
      hideWindow: () => void,
      shortCut: (type: 'search', shortCut: string) => Promise<boolean>
    }
  }
}
