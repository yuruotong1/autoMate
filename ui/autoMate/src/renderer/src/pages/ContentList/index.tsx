import { NavLink, Outlet, useLoaderData, useNavigate } from "react-router-dom"
import "./content.scss"
import { useEffect } from "react"

export const ContentList = () => {
    const contentList = useLoaderData() as ContentType[]
    const navigate = useNavigate()
    useEffect(() => {
        if (contentList) {
            navigate(`/config/category/contentList/${contentList[0].category_id}/content/${contentList[0].id}`)
        }
    }, [contentList])
    return (<main className="content-page">
        <div className="list">
            {contentList.map(content => (
                <NavLink 
                   key={content.id} 
                   to={`/config/category/contentList/${content.category_id}/content/${content.id}`}
                   className={({ isActive }) => `${isActive ? "active" : ""}`}> {content.title} </NavLink>
            ))}
        </div>
        <div className="content">
            <Outlet />
        </div>
    </main>)
}