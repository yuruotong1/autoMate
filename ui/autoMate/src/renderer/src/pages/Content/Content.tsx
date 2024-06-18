import { useLoaderData } from "react-router-dom"
import "./content.scss"
import { Button } from "antd"
export const Content = () => {
    const content = useLoaderData() as ContentType
    return (
    <main className="content-page">
        <input defaultValue={content.title}/>
        <textarea defaultValue={content.content}/>
        <div className="border-t flex items-center justify-center">
            <Button type="default" size="small">保存</Button>
        </div>
    </main>
    )
}