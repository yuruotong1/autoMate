import { redirect } from "react-router-dom"

export default async ({ request }) => {
    const formData = await request.formData()
    const data = Object.fromEntries(formData)
    switch (request.method) {
        case "POST": {
            return await window.api.sql(
                "insert into categories (name, created_at) values('未命名', datetime())",
                "create",
            )
        }
        case "DELETE": {
            await window.api.sql(
                `delete from categories where id = @id`,
                "del",
                {
                    id: data.id
                })

            await window.api.sql(
                `update contents set category_id = 0 where category_id = @category_id`,
                "update",
                {
                    category_id: data.id
                }
            )
            return redirect("/config/category/contentList")
        }
        case "PUT": {
            return await window.api.sql(
                `update categories set name = @name where id = @id`,
                "update",
                data
            )
        }
    }
    return {}
}   
