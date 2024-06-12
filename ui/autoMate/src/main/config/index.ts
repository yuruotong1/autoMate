import { BrowserWindow } from "electron"
import { createWindow } from "./window"
let win = null as null|BrowserWindow
const createConfigWindow=()=>{
  // 解决重复创建窗口
  if(!win) win = createWindow()
  // 窗口关闭时，将win置为null，可再次打开
  win.on("closed", ()=>{
    win = null
  })
}

export { createConfigWindow }
