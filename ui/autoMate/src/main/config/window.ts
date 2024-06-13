
import { BrowserWindow, shell } from 'electron'
import { is } from '@electron-toolkit/utils'
import icon from '../../../resources/icon.png?asset'
import { join } from 'path'
import url from 'node:url'

export function createWindow(): BrowserWindow {  // Create the browser window.
    const win = new BrowserWindow({
      width: 1250,
      height: 750,
      center: true,
      show: false,
      frame: true,
      transparent: false,
      // alwaysOnTop: true,
      autoHideMenuBar: true,
      ...(process.platform === 'linux' ? { icon } : {}),
      webPreferences: {
        preload: join(__dirname, '../preload/index.js'),
        sandbox: false
      }
    })
  
    win.webContents.openDevTools()
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
      win.loadURL(process.env['ELECTRON_RENDERER_URL'] + "/#config")
    } else {
      win.loadURL(
        url.format({
          pathname: join(__dirname, '../renderer/index.html'),
          protocol: 'file',
          slashes: true,
          hash: 'config'
        })
      )
    }

    return win
  }
  