import { Link, NavLink, Outlet, useLoaderData, useNavigate } from "react-router-dom"
import "./category.scss"
import { Add, DatabaseConfig, FolderClose } from "@icon-park/react"
import { useEffect } from "react"

export const Category = () => {
    const categories = useLoaderData() as CategoryType[]
    const navigate = useNavigate()
    useEffect(() => {
        if (categories) {
            navigate(`/config/category/contentList/${categories[0].id}`)
        }
    }, [categories])
    return (
    <main className="category-page">
        <div className="categories">
            {categories.map((category) => (
                <NavLink 
                to={`/config/category/contentList/${category.id}`} 
                key={category.id} 
                className={({isActive}) => (isActive ? 'active' : '')}
                >
                    <FolderClose theme="outline" size="12" strokeWidth={3}></FolderClose>
                    <div className="truncate">{category.name}</div>
                    </NavLink>
            ))}
        </div>

        <div className="nav">
        <Add theme="outline" size="20" fill="#333"/>
        <DatabaseConfig theme="outline" size="20" fill="#333"/>
        </div>
        <div className="content">
            <Outlet></Outlet>
        </div>
    </main>
 )
}