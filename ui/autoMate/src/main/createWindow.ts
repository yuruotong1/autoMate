
import { BrowserWindow, BrowserWindowConstructorOptions, shell } from 'electron'
import { is } from '@electron-toolkit/utils'
import icon from '../../../resources/icon.png?asset'
import { join } from 'path'

export interface OptionsType extends Partial<BrowserWindowConstructorOptions>{
    openDevTools?: boolean
}
export function createWindow(options: OptionsType): BrowserWindow {  // Create the browser window.
    const win = new BrowserWindow(Object.assign({
        width: 500,
        height: 350,
        center: true,
        show: false,
        frame: false,
        transparent: true,
        // alwaysOnTop: true,
        autoHideMenuBar: true,
        ...(process.platform === 'linux' ? { icon } : {}),
        webPreferences: {
            preload: join(__dirname, '../preload/index.js'),
            sandbox: false
        }
    }, options))
    // 如果是在开发环境下并且选项是打开开发者工具
    if (is.dev && options.openDevTools) win.webContents.openDevTools()
    win.on('ready-to-show', () => {
        win.show()
    })

    win.webContents.setWindowOpenHandler((details) => {
        shell.openExternal(details.url)
        return { action: 'deny' }
    })

    // HMR for renderer base on electron-vite cli.
    // Load the remote URL for development or the local html file for production.
    if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
        win.loadURL(process.env['ELECTRON_RENDERER_URL'])
    } else {
        win.loadFile(join(__dirname, '../renderer/index.html'))
    }

    return win
}
