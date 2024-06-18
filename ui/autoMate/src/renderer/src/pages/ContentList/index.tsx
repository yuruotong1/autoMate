import { NavLink, Outlet, useLoaderData, useNavigate } from "react-router-dom"
import "./contentList.scss"
import { useEffect } from "react"
import dayjs from "dayjs"

export const ContentList = () => {
    const contentList = useLoaderData() as ContentType[]
    // const navigate = useNavigate()
    // useEffect(() => {
    //     if (contentList) {
    //         navigate(`/config/category/contentList/${contentList[0].category_id}/content/${contentList[0].id}`)
    //     }
    // }, [contentList])
    return (<main className="contentList-page">
        <div className="list">
            {contentList.map(content => (
                <NavLink 
                   key={content.id} 
                   to={`/config/category/contentList/${content.category_id}/content/${content.id}`}
                   className={({ isActive }) => `${isActive ? "active" : ""}`}> 
                   <div className="truncate">{content.title}</div>
                   <div className="text-[10px] opacity-80 ">{dayjs(content.created_at).format("YYYY/MM/DD")}</div>
                   </NavLink>
            ))}
        </div>
        <div className="content">
            <Outlet />
        </div>
    </main>)
}