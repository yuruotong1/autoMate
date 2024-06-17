import { useLoaderData } from "react-router-dom"
import "./content.scss"
export const Content = () => {
    const content = useLoaderData() as ContentType
    return (
    <main className="content-page">
        <h1>{content.title}</h1>
        <div className="content">{content.content}</div>
    </main>
    )
}