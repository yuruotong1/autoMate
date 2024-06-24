// import { Random } from "mockjs";
import { db } from "./connect";
import { findOne } from "./query";

export function initTable() {
    

db().exec(`
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT not null,
    name TEXT not null,
    created_at text not null
);
`)


db().exec(`
CREATE TABLE IF NOT EXISTS contents (
    id INTEGER PRIMARY KEY AUTOINCREMENT not null,
    title TEXT not null,
    content TEXT not null,
    category_id INTEGER,
    created_at TEXT not null
);
`)


db().exec(`
CREATE TABLE IF NOT EXISTS config (
    id INTEGER PRIMARY KEY AUTOINCREMENT not null,
    content TEXT not null
);
`)

initData()
}

function initData() {
    const initData = findOne('select * from config')
    if (initData) return
    db().exec(`insert into config (id, content) values(1,'{"shortCut":"Alt+Space","databaseDirectory":""}')`)
    
}


// for (let i = 0; i < 20; i++) {
//     const name = Random.title(5, 10)
//     db().exec(`insert into config (content) values('${name}')`)
// }

// for (let i = 0; i < 20; i++) {
//     const name = Random.title(5, 10)
//     db().exec(`insert into categories (name, created_at) values('${name}', datetime())`)
// }

// for (let i = 1; i < 20; i++) {
//     const title = Random.title(5, 10)
//     const content = Random.paragraph(5, 10)
//     db().exec(`insert into contents (title, content, category_id, created_at) values('${title}', '${content}', ${i}, datetime())`)
// }