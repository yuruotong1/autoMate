export default async({params, request}) => {
    const url = new URL(request.url)
    const searchWord = url.searchParams.get("searchWord")
    let sql = "select * from contents"
    if (searchWord) {
        sql += ` where title like @searchWord order by id desc`
        console.log("hello")
        return window.api.sql(sql, "findAll", {searchWord: `%${searchWord}%`})
    }
    if (params.cid != undefined) {
        sql += ` where category_id=${params.cid}`
    }
    sql += " order by id desc"
    return  window.api.sql(sql, "findAll")
}