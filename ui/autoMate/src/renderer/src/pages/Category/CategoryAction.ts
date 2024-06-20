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
            return await window.api.sql(
                `delete from categories where id = @id`,
                "del",
                {
                    id: data.id
                })
        }
    }
    return {}
}   
