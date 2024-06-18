export default async({request}) => {
    const data = await request.formData()
    console.log(data.get("content"))
    return {}
}