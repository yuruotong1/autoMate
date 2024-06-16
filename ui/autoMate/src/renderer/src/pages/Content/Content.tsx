import { useLoaderData } from "react-router-dom"

export const Content = () => {
    const content = useLoaderData() as ContentType
    return <div>{content.content}</div>
}