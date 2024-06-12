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

export const update = (sql: string) => {
    return db.prepare(sql).run().changes;
}

export const del = (sql: string) => {
    return db.prepare(sql).run().changes;
}