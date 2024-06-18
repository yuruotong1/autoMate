import { Form, useLoaderData } from "react-router-dom"
import "./content.scss"
export const Content = () => {
    const content = useLoaderData() as ContentType
    return (
    <Form method="PUT">
    <main className="content-page">
        <input defaultValue={content.title} name="title"/>
        <textarea defaultValue={content.content} name="content"/>
        <div className="border-t flex items-center justify-center">
            <button>保存</button>
        </div>
    </main>
    </Form>
    )
}