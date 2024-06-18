export default async({request, params}) => {
    // params 接收路由中传递过来的数据
    const data = await request.formData()
    const res = window.api.sql(
        `update contents set title=@title, content=@content, category_id=@category_id where id=@id`, 
        "update",
        {title: data.get("title"), 
        content: data.get("content"), 
        category_id: data.get("category_id"),
        id: params.id}
    )
    return res
}