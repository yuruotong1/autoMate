import { Form, useLoaderData, useRevalidator, useSubmit } from "react-router-dom"
import "./content.scss"
import CodeEditor from "@renderer/components/CodeEditor"
export const Content = () => {
    const {content, categories} = useLoaderData() as {
        content: ContentType
        categories: CategoryType[]
    }
    const revalidator = useRevalidator();
    const submit = useSubmit()
    return (
    <Form method="PUT">
    <main className="content-page" key={content.id}>
        <input name="id" type="text" defaultValue={content.id} hidden></input>
        <input autoFocus defaultValue={content.title} name="title" onChange={(e) => {
            submit(e.target.form)
        }}/>
        <select name="category_id" value={content.category_id} onChange={(e)=>
            submit(e.target.form)
        }>
            <option value="0">未分类</option>
            {categories.map((category) => (
                <option key={category.id} value={category.id}>{category.name}</option>
            ))}
        </select>
        {/* <textarea  defaultValue={content.content} name="content" onChange={(e) => {
            submit(e.target.form)
            setCode(e.target.value)
        }}/> */}
        <CodeEditor id={content.id} defaultValue={content.content} revalidator={()=>revalidator.revalidate()} />
    </main>
    </Form>
    )
}