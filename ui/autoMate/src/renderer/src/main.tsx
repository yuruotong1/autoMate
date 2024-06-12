import React from 'react'
import ReactDOM from 'react-dom/client'
import '@renderer/assets/tailwind.css'
import '@renderer/assets/global.scss'
import { RouterProvider } from 'react-router-dom'
import router from './router'

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
)
