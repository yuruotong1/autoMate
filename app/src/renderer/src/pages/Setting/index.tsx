import React, { useEffect } from 'react';
import {
  SettingOutlined,
  UserOutlined,
} from '@ant-design/icons';
import { Menu } from 'antd';
import type { GetProp, MenuProps } from 'antd';
import { Outlet, useNavigate } from 'react-router-dom';
import styles from './styles.module.scss'



const Setting: React.FC = () => {
  
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
  const navigate = useNavigate()

  useEffect(() => {
    navigate('/setting/settingUser');
  }, [navigate]);

  return (
    <main className={styles.setting}>
      <div className={styles.menu}>
      <Menu
        defaultSelectedKeys={['1']}
        items={items}
        onSelect={(e)=>{
          if(e.key === '1'){
            navigate('/setting/settingUser')
          }else if(e.key === '2'){
            navigate('/setting/settingBasic')
          }
        }}
      />
      </div>
    <div className={styles.content}>
          <Outlet/>
    </div>
    </main>
  );
};

export default Setting;