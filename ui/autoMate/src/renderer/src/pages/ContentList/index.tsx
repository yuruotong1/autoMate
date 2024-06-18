import { NavLink, Outlet, useLoaderData} from "react-router-dom"
import "./contentList.scss"
import dayjs from "dayjs"

export const ContentList = () => {
    const contentList = useLoaderData() as ContentType[]
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