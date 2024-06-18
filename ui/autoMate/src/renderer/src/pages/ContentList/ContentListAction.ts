import { redirect } from "react-router-dom"

export default async ({request, params}) => {
    const formData = await request.formData()
    const cid = params.cid || 0
    switch(formData.get("action")){
        case "add": {
            const id = await window.api.sql(
                `insert into contents (title, content, category_id, created_at) values ('未命名', '', ${cid}, datetime())`, 
                "create")
            return redirect(`content/${id}`)
        }
    }

    return {}

}