import { useNavigate } from "react-router-dom"

export default  () => {
    const navigate = useNavigate()
    const updateContentCategory = async(id: number, category_id: number) => {
        await window.api.sql(
            `UPDATE contents set category_id=@category_id WHERE id=@id`,
            "update",
            {category_id, id}
        )
        navigate(`/config/category/contentList/${category_id}/content/${id}`)

    }
    return {updateContentCategory}
}