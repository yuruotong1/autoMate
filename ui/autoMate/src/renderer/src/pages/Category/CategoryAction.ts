export default async({request}) =>{
    await window.api.sql(
        "insert into categories (name, created_at) values('未命名', datetime())",
        "create",
    )
  return {}
}
