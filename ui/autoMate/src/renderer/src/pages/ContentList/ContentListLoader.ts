export default async({params}) => {
    const res = await window.api.sql(`select * from contents where category_id=${params.cid}`, "findAll")
    return res
}