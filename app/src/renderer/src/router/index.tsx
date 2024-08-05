import Home from "@renderer/layouts/Home";
import { createHashRouter } from "react-router-dom";
import SettingBasicAction from "@renderer/pages/SettingBasic/SettingBasicAction";
import SettingBasicLoader from "@renderer/pages/SettingBasic/SettingBasicLoader";
import Setting from "@renderer/pages/Setting/index";
import About from "@renderer/layouts/About";
import { SettingBasic } from "@renderer/pages/SettingBasic";
import { SettingUser } from "@renderer/pages/SettingUser";

const router = createHashRouter([
  {
    path: "/",
    element: <Home />
  },
  {
    path: "about",
    element: <About />
  },
  {
    path: "setting",
    element: <Setting/>,
    children: [
      {
        index: true,
        path: "settingUser",
        element: <SettingUser />,
      },
      {
        path: "settingBasic",
        element: <SettingBasic />,
        loader: SettingBasicLoader,
        action: SettingBasicAction
      }
    ]
  }
])
export default router
