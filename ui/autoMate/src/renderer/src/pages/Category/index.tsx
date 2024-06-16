import { Outlet, useLoaderData } from "react-router-dom"
import "./category.scss"
import { Add, DatabaseConfig } from "@icon-park/react"

export const Category = () => {
    const categories = useLoaderData() as CategoryType[]
    return (
    <main className="category-page">
        <div className="categories">
            {categories.map((category) => (
                <div key={category.id} className="item">{category.name}</div>
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