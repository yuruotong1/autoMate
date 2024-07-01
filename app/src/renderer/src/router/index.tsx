import Config from "@renderer/layouts/Config";
import Home from "@renderer/layouts/Home";
import { createHashRouter } from "react-router-dom";
import {Category} from "@renderer/pages/Category";
import { ContentList } from "@renderer/pages/ContentList";
import CategoryLoader from "@renderer/pages/Category/CategoryLoader";
import ContentListLoader from "@renderer/pages/ContentList/ContentListLoader";
import ContentLoader from "@renderer/pages/Content/ContentLoader";
import { Content } from "@renderer/pages/Content/Content";
import ContentAction from "@renderer/pages/Content/ContentAction";
import { Welcome } from "@renderer/pages/Welcome";
import ContentListAction from "@renderer/pages/ContentList/ContentListAction";
import CategoryAction from "@renderer/pages/Category/CategoryAction";
import { Setting } from "@renderer/pages/Setting";
import Interactive from "@renderer/pages/Interactive";
import SettingAction from "@renderer/pages/Setting/SettingAction";
import SettingLoader from "@renderer/pages/Setting/SettingLoader";

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
        index: true,
        element: <Setting/>,
        loader: SettingLoader,
        action: SettingAction
        
      },
      {
        path: "category",
        // 界面第一次打开时，默认显示的页面
        element: <Category />,
        loader: CategoryLoader,
        action: CategoryAction,
        children: [
          {
            path: "contentList/:cid?",
            loader: ContentListLoader,
            action: ContentListAction,
            element: <ContentList />,
            children: [
              {
                index: true,
                element: <Welcome />
              },
              {
                path: "content/:id",
                loader: ContentLoader,
                action: ContentAction,
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
