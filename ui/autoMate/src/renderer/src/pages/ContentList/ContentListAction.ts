export default async ({request, params}) => {
    const formData = await request.formData()
    const cid = params.cid || 0
    switch(formData.get("action")){
        case "add":
            await window.api.sql(
                `insert into contents (title, content, category_id, created_at) values ('未命名', '', ${cid}, datetime())`, 
                "create")
            break
    }

    return {}

}