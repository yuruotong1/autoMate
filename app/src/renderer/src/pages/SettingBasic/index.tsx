import { localServerBaseUrl } from "@renderer/config"
import { useEffect, useState } from "react";
import { useLoaderData } from "react-router-dom";
import { Button, Form, Input, Select, Space, message } from 'antd';
import styles from './styles.module.scss'

export const SettingBasic = () => {
    const [form] = Form.useForm();
    const config = useLoaderData() as ConfigDataType
    useEffect(() => {
      form.setFieldsValue(config);
    }, [])
    const { Option } = Select;
    const tailLayout = {
    wrapperCol: { offset: 6, span: 16 },
    };

  const [keys, setKeys] = useState<string[]>([])
  const onModelChange = (value: string) => {
    switch (value) {
      case 'openai':
        form.resetFields(['llm'])
        form.setFieldsValue({"llm": {model: 'gpt-4-turbo', base_url:"https://api.openai.com/v1"}});
        break;
      case 'ollama':
        form.resetFields(['llm'])
        form.setFieldsValue({"llm": {model: 'ollama/codeqwen:latest',api_base: "http://localhost:11434" }});
        break;
      default:
    }
  };

  const onFinish = async (values: any) => {
    await window.api.sql(`update config set content=@content where id = 1`,
    'update',
    {
      content: JSON.stringify(values)
    })
    // 注册快捷键
    window.api.shortcut()
     window.close();
  };

  const onClose = () => {
    window.close()
  };

  
    return (
        <div className={styles.settingPage}>
    <Form
      form={form}
      name="control-hooks"
      onFinish={onFinish}
    >
        <section>
        <h5>快捷键定义</h5>
        <Form.Item name="shortcut" label="呼出快捷键" rules={[{ required: true }]}>
            <Input 
              type="text"
              readOnly
              onKeyDown={(e) => {
              if (e.metaKey || e.ctrlKey || e.altKey) {
                const code = e.code.replace(/Left|Right|Key|Digit/, '')
                if (keys.includes(code)) return
                keys.push(code)
                setKeys(keys)
                // 如果以数字或字母或者空格结尾
                if (code.match(/^(\w|\s)$/gi)) {
                  e.currentTarget.value = keys.join('+')
                  form.setFieldsValue({shortcut: e.currentTarget.value})
                  setKeys([])
                }
              }
            }}
            />
       </Form.Item>
       </section>
       <section>
       
       <div className='flex flex-row  justify-between items-center mb-3'>
       <h5>大模型配置信息</h5>
       <Button
              onClick={async () => {
                const hide = message.loading('检测中...', 0);
                const res = await fetch(`${localServerBaseUrl}/llm`,
                  {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(
                      { "messages": [{ "role": "user", "content": "hello" }],
                        "llm_config": JSON.stringify(form.getFieldValue("llm"))}),
                  }
                )
                hide();
                const jsonResponse = await res.json()
                if (jsonResponse.status === 0) {
                  message.success(`连接成功！`)
                } else {
                  message.error( 
                  <span style={{ whiteSpace: 'pre-line' }}>
                  {`连接失败！\n${jsonResponse.content}`}
                </span>)
                }
              
              }}>检查连接</Button>
        </div>
        <Form.Item name="format" label="格式" rules={[{ required: true }]}>
        <Select
          placeholder="选择格式，一般OpenAI格式为万能格式"
          onChange={onModelChange}
          allowClear
        >
          <Option value="openai">OpenAI</Option>
          <Option value="ollama">Ollama</Option>
        </Select>
      </Form.Item>
      
      <Form.Item name={["llm", "model"]} label="model" rules={[{ required: true }]}>
        <Input />
      </Form.Item>
      
      <Form.Item
        noStyle
        shouldUpdate={(prevValues, currentValues) => prevValues.format !== currentValues.format}
      >
        {({ getFieldValue }) =>
          getFieldValue('format') === 'openai' ? (
            <div>
            <Form.Item name={["llm", "api_key"]} label="api_key" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
            <Form.Item name={["llm", "base_url"]} label="base_url" rules={[{ required: false }]}>
            <Input />
          </Form.Item>
          </div>
          ) : null
        }
      </Form.Item>

      <Form.Item
        noStyle
        shouldUpdate={(prevValues, currentValues) => prevValues.format !== currentValues.format}
      >
        {({ getFieldValue }) =>
          getFieldValue('format') === 'ollama' ? (
            <Form.Item name={["llm", "api_base"]} label="api_base" rules={[{ required: false }]}>
            <Input />
          </Form.Item>
          ) : null
        }
      </Form.Item>
      </section>
      <div className='mt-10 flex justify-center items-center'>
      <Form.Item {...tailLayout} >
        <Space>
         <Button htmlType="button" onClick={onClose} className='mr-5'>
            取消
          </Button>
          <Button type="primary" htmlType="submit" >
            保存
          </Button>
          
        </Space>
      </Form.Item>
      </div>
    </Form>
    </div>
    )
}