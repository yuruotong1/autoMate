import {
  LockOutlined,
  MobileOutlined,
} from '@ant-design/icons';
import {
  LoginForm,
  ProConfigProvider,
  ProFormCaptcha,
  ProFormCheckbox,
  ProFormText,
} from '@ant-design/pro-components';
import { theme } from 'antd';
import logo from '@renderer/assets/icon.png';
import useLogin from '@renderer/hooks/useLogin';
import AV from 'leancloud-storage' // 使用 import 代替 require
import { useEffect } from 'react';


export const SettingUser = () => {
  const { token } = theme.useToken();
  const { login } = useLogin();
  useEffect(() => {
    
  }, [])
  return (
    <ProConfigProvider hashed={false}>
      <div style={{ backgroundColor: token.colorBgContainer }}>
        <LoginForm
          logo={logo}
          title="autoMate"
          subTitle="全球最大的Agent+RPA平台"
          onFinish={(values) => login(values)} // 使用新的 onFinish 函数
        >
          <ProFormText
            fieldProps={{
              size: 'large',
              prefix: <MobileOutlined className={'prefixIcon'} />,
            }}
            name="mobile"
            placeholder={'手机号'}
            rules={[
              {
                required: true,
                message: '请输入手机号！',
              },
              {
                pattern: /^1\d{10}$/,
                message: '手机号格式错误！',
              },
            ]}
          />
          <ProFormCaptcha
            fieldProps={{
              size: 'large',
              prefix: <LockOutlined className={'prefixIcon'} />,
            }}
            captchaProps={{
              size: 'large',
            }}
            phoneName={"mobile"}
            placeholder={'请输入验证码'}
            captchaTextRender={(timing, count) => {
              if (timing) {
                return `${count} ${'获取验证码'}`;
              }
              return '获取验证码';
            }}
            name="captcha"
            rules={[
              {
                required: true,
                message: '请输入验证码！',
              },
            ]}
            onGetCaptcha={async (mobile) => {
              console.log(mobile)
              AV.User.requestLoginSmsCode(mobile).then(() => {
              }).catch((error) => {
                // 手机号未注册时，自动注册
                if (error.code === 213) {
                  AV.Cloud.requestSmsCode("+8613261993657");
                }
              })
            }
          }
          />

          <div
            style={{
              marginBlockEnd: 24,
            }}
          >
            <ProFormCheckbox noStyle name="autoLogin">
              自动登录
            </ProFormCheckbox>
            <a
              style={{
                float: 'right',
              }}
            >
              忘记密码
            </a>
          </div>
        </LoginForm>
      </div>
    </ProConfigProvider>

  );
};