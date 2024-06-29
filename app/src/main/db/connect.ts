import Database, * as BetterSqlite3 from 'better-sqlite3';
import { app } from 'electron';
import { resolve } from 'node:path'

const db = (): BetterSqlite3.Database => {
    let dir = resolve(app.getPath('home'), "autoMate.db")

    const db: BetterSqlite3.Database = new Database(dir, {});
    db.pragma('journal_mode = WAL');
    return db
}
export { db };