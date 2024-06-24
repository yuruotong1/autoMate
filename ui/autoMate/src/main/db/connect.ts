import Database, * as BetterSqlite3 from 'better-sqlite3';
import { app } from 'electron';
import { resolve } from 'node:path'
import config from './config';
import { existsSync } from 'node:fs';

const db = (): BetterSqlite3.Database => {
    let dir = resolve(app.getPath('home'))
    if (config.databaseDirectory && existsSync(config.databaseDirectory)) {
        dir = config.databaseDirectory
    }

    const db: BetterSqlite3.Database = new Database(dir + '/autoMate.db', {});
    db.pragma('journal_mode = WAL');
    return db
}
export { db };