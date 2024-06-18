export default async({request, params}) => {
    // params 接收路由中传递过来的数据
    const data = await request.formData()
    const res = window.api.sql(
        `update contents set title=@title, content=@content where id=@id`, 
        "update",
        {title: data.get("title"), 
        content: data.get("content"), 
        id: params.id}
    )
    return res
}