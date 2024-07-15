import React  from 'react';
import {
  SettingOutlined,
  UserOutlined,
} from '@ant-design/icons';
import { Menu } from 'antd';
import type { GetProp, MenuProps } from 'antd';
import { Outlet } from 'react-router-dom';


type MenuItem = GetProp<MenuProps, 'items'>[number];

const items: MenuItem[] = [
  {
    key: '1',
    icon: <UserOutlined />,
    label: ' 我的账号',
  },
  {
    key: '2',
    icon: <SettingOutlined />,
    label: '设置',
  }
];

const Setting: React.FC = () => {
 
  return (
    <>
      <Menu
        style={{ width: 150 }}
        defaultSelectedKeys={['1']}
        items={items}
        onSelect={(e)=>{
          console.log(e.key)
        }}
      />
    <div >
          <Outlet></Outlet>
    </div>

    </>
  );
};

export default Setting;