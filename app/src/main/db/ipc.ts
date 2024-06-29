import { IpcMainInvokeEvent, ipcMain } from "electron";
import * as query from './query'
import { initTable } from "./tables";
ipcMain.handle('sql', (_event: IpcMainInvokeEvent, sql: string, type: SqlActionType, params={}) => {
    return query[type](sql, params)
})



ipcMain.on('initTable', () => {
    initTable()
})

ipcMain.handle('getConfig', async () => {
    return query.findOne('SELECT * FROM config where id = 1')
})
