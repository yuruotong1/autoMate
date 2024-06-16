import { Link, Outlet, useLoaderData } from "react-router-dom"
import "./category.scss"
import { Add, DatabaseConfig } from "@icon-park/react"

export const Category = () => {
    const categories = useLoaderData() as CategoryType[]
    return (
    <main className="category-page">
        <div className="categories">
            {categories.map((category) => (
                <Link to={`/config/category/contentList/${category.id}`} key={category.id} className="item" >{category.name}</Link>
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