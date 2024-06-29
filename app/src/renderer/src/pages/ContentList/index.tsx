import {Outlet, useLoaderData} from "react-router-dom"
import "./contentList.scss"
import { ContentSearch } from "@renderer/components/ContentSearch";
import { ContentItem } from "@renderer/components/ContentItem";


export const ContentList = () => {
    const contentList = useLoaderData() as ContentType[]

    return (<main className="contentList-page">
        <div className="list">
           <ContentSearch/>
            {contentList.map(content => (
                <ContentItem key={content.id} content={content}/>
            ))}
        </div>
        <div className="content">
            <Outlet />
        </div>
    </main>)
}