import { useState } from "react"
import { data as codes } from "@renderer/data"
export default function index() {
    const [data, setData] = useState(codes)
    return (
    <main className='bg-slate-50 rounded-bl-lg rounded-br-lg -mt-[7px] pb-2'>
        {data.map((item, index) => (
            <div key={index} className='text-slate-700 truncate mb-2'>
                <p>{item.content}</p>
            </div>
        ))}

    </main>
  )
}
