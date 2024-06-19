import { Add } from "@icon-park/react"
import { Form, useSubmit } from "react-router-dom"

export const ContentSearch = () => {
  const submit = useSubmit()
  return (
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
  )
}
