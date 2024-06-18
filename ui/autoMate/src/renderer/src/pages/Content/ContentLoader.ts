export default async({params}) => {
    const content = await window.api.sql(`select * from contents where id = ${params.id}`, "findOne")
    const categories = await window.api.sql(`select * from categories order by id desc`, "findAll")
    return {
        content,
        categories
    }
}
