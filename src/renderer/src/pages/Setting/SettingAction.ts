export default async ({ request }) => {
    const formData = await request.formData()
    const data = Object.fromEntries(formData)
    window.api.sql(`update config set content=@content where id = 1`,
        'update',
        {
            content: JSON.stringify(data)
        }
    )
    return {}
}