import {db} from './connect'

export const findAll = (sql: string) => {
    return db.prepare(sql).all();
}

export const findOne = (sql: string) => {
    return db.prepare(sql).get();
}

export const create = (sql: string) => {
    return db.prepare(sql).run().lastInsertRowid;
}


//使用 params 是为了防止 sql 注入
export const update = (sql: string, params: Record<string, any>) => {
    return db.prepare(sql).run(params).changes;
}

export const del = (sql: string) => {
    return db.prepare(sql).run().changes;
}