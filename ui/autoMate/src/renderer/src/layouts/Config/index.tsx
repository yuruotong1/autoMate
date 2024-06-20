import { Outlet } from "react-router-dom"
import { MantineProvider } from '@mantine/core';
import { ContextMenuProvider } from 'mantine-contextmenu';
// 右键菜单
import '@mantine/core/styles.layer.css';
import 'mantine-contextmenu/styles.layer.css';
export default function Config() {
  return (
    <MantineProvider defaultColorScheme="light">
      <ContextMenuProvider>
        <main>
          <Outlet />
        </main>
      </ContextMenuProvider>
    </MantineProvider>
  )
}


