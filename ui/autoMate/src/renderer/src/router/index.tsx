import Config from "@renderer/pages/Config";
import Home from "@renderer/pages/Home";
import { createHashRouter } from "react-router-dom";
import {Category} from "@renderer/pages/Category";
import { Content } from "@renderer/pages/Content";

const router = createHashRouter([
  {
    path: "/",
    element: <Home />
  },
  {
    path: "config",
    element: <Config />,
    children: [
      {
        path: "",
        // 界面第一次打开时，默认显示的页面
        element: <Category />,
        children: [
          {
            index: true,
            element: <Content />
          }
        ]
      }
    ]
  }
])
export default router
