
import { BrowserWindow, BrowserWindowConstructorOptions, shell } from 'electron'
import { is } from '@electron-toolkit/utils'
import icon from '../../resources/icon.png?asset'
import { join } from 'path'
import url from 'node:url'
export interface OptionsType extends Partial<BrowserWindowConstructorOptions>{
    openDevTools?: boolean,
    hash?: string
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


    if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
        // win.loadURL(process.env['ELECTRON_RENDERER_URL'] + "/#config/category/contentList")
        win.loadURL(process.env['ELECTRON_RENDERER_URL'] + options.hash)
      } else {
        win.loadURL(
          url.format({
            pathname: join(__dirname, '../renderer/index.html'),
            protocol: 'file',
            slashes: true,
            hash: 'config/category/contentList'
          })
        )
      }
  

    return win
}
