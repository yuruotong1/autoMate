export default async ({request}) => {
    const formData = await request.formData()
    switch(formData.get("action")){
        case "add":
            await window.api.sql(
                `insert into contents (title, content, created_at) values ('未命名', '', datetime())`, 
                "create")
            break
    }

    return {}

}