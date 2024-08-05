import { BrowserWindow, IpcMainEvent, IpcMainInvokeEvent, Menu, Tray, app } from "electron"
import { OptionsType, createWindow} from "./createWindow"
const { exec } = require('child_process');
import { is } from '@electron-toolkit/utils'
import { shutdownServer } from "./serverUtilts";
export const config = {
    chat: {
        id: 0,
        options: {
            initShow: true,
            width: 600,
            height: 700,
            frame: false,
            transparent: true,
            openDevTools: false,
            hash: ''
        }
    },
    setting: {
        id: 0,
        options: {
            initShow: false,
            width: 830,
            height: 670,
            openDevTools: true,
            frame: true,
            transparent: false,
            hash: '/#setting'
        }
    },
    about: {
        id: 0,
        options: {
            initShow: false,
            width: 500,
            height: 300,
            openDevTools: false,
            frame: true,
            transparent: false,
            hash: '/#about'
        }
    }

} as Record<WindowNameType, {id: number,  options: OptionsType }>
// createWindow({})

// 根据名称获取窗口
export const getWindowByName = (name: WindowNameType, router_url="")=>{
   
     // 根据id取得窗口
     let win = BrowserWindow.fromId(config[name].id)
     // 避免重复点击重复创建窗口
     if (!win) {
         win = createWindow(config[name].options,router_url)
         config[name].id = win.id
     }
     // 在页面加载完成后设置窗口标题
    win.webContents.on('did-finish-load', () => {
        win.setTitle('autoMate');
    });
 
     // 修改窗口图标 (需要提供图标的路径)
    win.setIcon('resources/icon.png');
    
     return win
}


// 根据触发来源获取窗口 
export const getWindowByEvent = (event: IpcMainEvent | IpcMainInvokeEvent) => {
    return BrowserWindow.fromWebContents(event.sender)!
}

function createTray(){
    const tray = new Tray('resources/icon.png')
    tray.setToolTip('autoMate智子')
    tray.setTitle('autoMate')
    tray.addListener('click', () => {
        getWindowByName('chat').show()
    })

    const menu = Menu.buildFromTemplate([
        { label: '关于', click: () => { getWindowByName('about').show() } },

        { label: '设置', click: () => { getWindowByName('setting').show() } },

        { label: '退出', click: async () => { 
            await shutdownServer()
            app.quit() 
        } 
        
        },
    ])
    tray.setContextMenu(menu)
}

app.whenReady().then(() => {
    createTray()
    const win = getWindowByName('chat')
    win.on('blur', () => {
        win.hide()
    })
    if(!is.dev){
        const serverPath = process.platform === 'win32' ? '.\\autoMateServer.exe' : './autoMateServer.exe';
        exec(serverPath, (error: any, stdout: any, stderr: any) => {
            if (error) {
          console.error(`error: ${error}`);
          return;
        }
        console.log(`stdout: ${stdout}`);
        console.error(`stderr: ${stderr}`);
      });}
    
    // getWindowByName('code')
    // getWindowByName('about')

})