import { Form, useLoaderData, useRevalidator, useSubmit } from "react-router-dom"
import "./content.scss"
import CodeEditor from "@renderer/components/CodeEditor"
import { Button } from "antd"
import { localServerBaseUrl } from "@renderer/config"
import { useState } from "react"
import { useStore } from "@renderer/store/useStore"

export const Content = () => {
    const { content, categories } = useLoaderData() as {
        content: ContentType
        categories: CategoryType[]
    }
    const revalidator = useRevalidator();
    const submit = useSubmit()
    const [open, setOpen] = useState(false);
    const setChatMessages = useStore(state => state.setChatMessage)
    const chatMessages = useStore(state => state.chatMessages)
    return (
        <Form method="PUT">
            <main className="content-page" key={content.id}>
                <input name="id" type="text" defaultValue={content.id} hidden></input>
                <input autoFocus defaultValue={content.title} name="title" onChange={(e) => {
                    submit(e.target.form)
                }} />
                <div className="flex justify-between">
                    <select name="category_id" value={content.category_id} onChange={(e) =>
                        submit(e.target.form)
                    }>
                        <option value="0">未分类</option>
                        {categories.map((category) => (
                            <option key={category.id} value={category.id}>{category.name}</option>
                        ))}
                    </select>
                    <Button onClick={async () => {
                        revalidator.revalidate()
                        const res = await fetch(localServerBaseUrl + "/execute", {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                code: content.content
                            })
                        });
                        const data = await res.json();
                        setOpen(true)
                        setChatMessages([...chatMessages,
                        { role: "assistant", content: "代码运行结果如下：" + JSON.stringify(data), createAt: new Date().getTime(), updateAt: new Date().getTime(), id: new Date().getTime().toString() }])
                    }}>运行</Button>
                </div>
                <CodeEditor
                    open={open}
                    setOpen={setOpen}
                    id={content.id}
                    defaultValue={content.content}
                    revalidator={() => revalidator.revalidate()}
                />
            </main>
        </Form>
    )
}