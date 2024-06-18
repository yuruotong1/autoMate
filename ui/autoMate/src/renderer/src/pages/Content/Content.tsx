import { Form, useLoaderData, useSubmit } from "react-router-dom"
import "./content.scss"
export const Content = () => {
    const content = useLoaderData() as ContentType
    const submit = useSubmit()
    return (
    <Form method="PUT">
    <main className="content-page" key={content.id}>
        <input defaultValue={content.title} name="title" onChange={(e) => {
            submit(e.target.form)
        }}/>
        <textarea defaultValue={content.content} name="content" onChange={(e) => {
            submit(e.target.form)
        }}/>
    </main>
    </Form>
    )
}