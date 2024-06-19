import { Form, NavLink, Outlet, useLoaderData, useSubmit} from "react-router-dom"
import "./contentList.scss"
import dayjs from "dayjs"
import { Add, Delete } from "@icon-park/react"
import { useContextMenu } from 'mantine-contextmenu';


export const ContentList = () => {
    const contentList = useLoaderData() as ContentType[]
    const submit = useSubmit()
    const { showContextMenu } = useContextMenu();
    return (<main className="contentList-page">
        <div className="list">
            <Form>
            <div className="border-b px-3 flex justify-between items-center">
            <input 
                name="searchWord"
                type="text" 
                placeholder="搜索..." 
                className="outline-none text-sm font-bold py-2 w-full"
                onChange={(e) => {
                    submit(e.target.form)
                }}
            />
            <Add
                theme="outline"
                size="18"
                fill="#000000"
                strokeWidth={2}
                onClick={()=>{
                    submit({action: 'add'}, {method: 'post'})
                }}
            />
            </div>
            </Form>
            {contentList.map(content => (
                <NavLink 
                   key={content.id} 
                   to={`/config/category/contentList/${content.category_id}/content/${content.id}`}
                   className="flex justify-between items-center"
                   onContextMenu={showContextMenu([
                    {
                      key: 'remove',
                      icon: <Delete theme="outline" size="18" strokeWidth={3} />,
                      title: '删除动作',
                      onClick: () => {
                        submit({id: content.id}, {method: 'DELETE'})
                      },
                    }
                  ],
                  {className: 'contextMenu'})}
                   > 
                   <div className="truncate">{content.title}</div>
                   <div className="text-[10px] opacity-80 ">{dayjs(content.created_at).format("YY/MM/DD")}</div>
                   </NavLink>
            ))}
        </div>
        <div className="content">
            <Outlet />
        </div>
    </main>)
}