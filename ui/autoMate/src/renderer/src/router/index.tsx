import Config from "@renderer/pages/Config";
import Home from "@renderer/pages/Home";
import { createHashRouter } from "react-router-dom";
import {Category} from "@renderer/pages/Category";
import { ContentList } from "@renderer/pages/ContentList";
import CategoryLoader from "@renderer/pages/Category/CategoryLoader";
import ContentListLoader from "@renderer/pages/ContentList/ContentListLoader";
import ContentLoader from "@renderer/pages/Content/ContentLoader";
import { Content } from "@renderer/pages/Content/Content";

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
            loader: ContentListLoader,
            element: <ContentList />,
            children: [
              {
                path: "content/:id",
                loader: ContentLoader,
                element: <Content />
              }
            ]
          }
        ]
      }
    ]
  }
])
export default router
