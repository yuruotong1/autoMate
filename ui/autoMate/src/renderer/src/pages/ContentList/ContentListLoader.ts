export default async({params}) => {
    let sql = "select * from contents"
    if (params.cid) {
        sql += ` where category_id=${params.cid}`
    }
    sql += " order by id desc"
    const res = await window.api.sql(sql, "findAll")
    return res
}