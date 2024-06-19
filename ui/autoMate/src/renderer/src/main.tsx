import React from 'react'
import ReactDOM from 'react-dom/client'
import '@renderer/assets/tailwind.css'
import '@renderer/assets/global.scss'
import { RouterProvider } from 'react-router-dom'
import router from './router'
// 右键菜单
import {MantineProvider } from '@mantine/core';
import { ContextMenuProvider } from 'mantine-contextmenu';
import '@mantine/core/styles.layer.css';
import 'mantine-contextmenu/styles.layer.css';
ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
      <MantineProvider defaultColorScheme="light">
          <ContextMenuProvider>
           <RouterProvider router={router} />
          </ContextMenuProvider>
        </MantineProvider>
   
  </React.StrictMode>
)
