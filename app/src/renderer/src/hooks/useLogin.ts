import AV from "leancloud-storage";

export default () => {
    const  login = ( values: any) => {
        // 模拟登录请求
        // const AV = require("leancloud-storage");
        AV.User.signUpOrlogInWithMobilePhone(values.mobile, values.captcha).then(
            (user) => {
              // 注册成功
              console.log(`注册成功。objectId：${user.id}`);

            },
            (error) => {
                // 验证码不正确
                console.log(error)
              }
          );
    

    }
    return { login }

}