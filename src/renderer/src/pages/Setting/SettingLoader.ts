export default async ({}) =>{
   const config =  (await window.api.sql('select * from config where id=1', 'findOne', {})) as ConfigType
   return JSON.parse(config.content) as ConfigDataType 
}