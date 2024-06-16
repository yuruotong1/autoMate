import { Outlet } from "react-router-dom"
import "./category.scss"
import { Add, DatabaseConfig } from "@icon-park/react"

export const Category = () => {
    return (
    <main className="category-page">
        <div className="categories">vue.js</div>
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