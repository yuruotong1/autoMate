import Config from "@renderer/pages/Config";
import Home from "@renderer/pages/Home";
import { createHashRouter } from "react-router-dom";
import {Category} from "@renderer/pages/Category";
import { ContentList } from "@renderer/pages/ContentList";
import CategoryLoader from "@renderer/pages/Category/CategoryLoader";

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
        path: "category",
        // 界面第一次打开时，默认显示的页面
        element: <Category />,
        loader: CategoryLoader,
        children: [
          {
            path: "contentList/:cid",
            element: <ContentList />
          }
        ]
      }
    ]
  }
])
export default router
