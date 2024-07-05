import { Button, Form, Input, Select, Space } from 'antd';

const { Option } = Select;

const layout = {
  labelCol: { span: 6 },
  wrapperCol: { span: 16 },
};

const tailLayout = {
  wrapperCol: { offset: 6, span: 16 },
};

export const Setting = () => {
  const [form] = Form.useForm();

  const onModelChange = (value: string) => {
    switch (value) {
      case 'openai':
        form.setFieldsValue({ model: 'gpt-4-turbo', base_url:"https://api.openai.com/v1"});
        
        break;
      case 'ollama':
        form.setFieldsValue({ model: 'ollama/llama2',api_base: "http://localhost:11434" });
        break;
      default:
    }
  };

  const onFinish = (values: any) => {
    console.log(values);
  };

  const onReset = () => {
    form.resetFields();
  };


  return (
    <div className='flex justify-center items-center h-screen'>
    <Form
      {...layout}
      form={form}
      name="control-hooks"
      onFinish={onFinish}
      style={{ maxWidth: 900 }}
    >
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
      
      <Form.Item name="model" label="model" rules={[{ required: true }]}>
        <Input />
      </Form.Item>
      
      <Form.Item
        noStyle
        shouldUpdate={(prevValues, currentValues) => prevValues.format !== currentValues.format}
      >
        {({ getFieldValue }) =>
          getFieldValue('format') === 'openai' ? (
            <div>
            <Form.Item name="api_key" label="api_key" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
            <Form.Item name="base_url" label="base_url" rules={[{ required: false }]}>
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
            <Form.Item name="api_base" label="api_base" rules={[{ required: false }]}>
            <Input />
          </Form.Item>
          ) : null
        }
      </Form.Item>
      <Form.Item {...tailLayout} className='mt-10'>
        <Space>
          <Button type="primary" htmlType="submit" >
            Submit
          </Button>
          <Button htmlType="button" onClick={onReset}>
            Reset
          </Button>
        </Space>
      </Form.Item>
    </Form>
    </div>
  );
};
