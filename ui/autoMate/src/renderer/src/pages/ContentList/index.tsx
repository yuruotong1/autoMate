import { NavLink, Outlet, useLoaderData } from "react-router-dom"
import "./content.scss"

export const ContentList = () => {
    const contentList = useLoaderData() as ContentType[]
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