import { Form, useLoaderData, useSubmit } from 'react-router-dom'
import styles from './styles.module.scss'
import { useState } from 'react'
import { Button, Select, message } from 'antd'
import { localServerBaseUrl } from '@renderer/config'

export const Setting = () => {
  // const config = useLoaderData() as ConfigDataType
  const [keys, setKeys] = useState<string[]>([])
  const config = useLoaderData() as ConfigDataType
  const submit = useSubmit()
  return (
    <Form method="POST">
      <main className={styles.settingPage}>
        <h1>Setting</h1>
        <section>
          <h5>快捷键定义</h5>
          <input
            type="text"
            name="shortCut"
            defaultValue={config.shortCut}
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
                  setKeys([])
                  config.shortCut = e.currentTarget.value
                  // 注册快捷键
                  window.api.shortCut()
                }
              }

            }}
          />
        </section>
        <section>
          <div className='flex flex-row  justify-between items-center mb-3'>
            <h5>大模型配置信息</h5>
            <Button
              onClick={async () => {
                const hide = message.loading('检测中...', 0);
                try {
                  const res = await fetch(`${localServerBaseUrl}/llm`,
                    {
                      method: 'POST',
                      headers: {
                        'Content-Type': 'application/json'
                      },
                      body: JSON.stringify({ "messages": [{ "role": "user", "content": "hello" }] }),
                    }
                  )
                  hide();
                  if (res.ok) {
                    message.success('连接成功')
                  } else {
                    message.error(`连接失败，请检查配置信息是否正确：\n${res.statusText}`)
                  }
                } catch (error) {
                  hide();
                  message.error(`连接失败，请检查配置信息是否正确：\n${error}`)
                }
              }}>检查连接</Button>
          </div>
          <input
            type="text"
            name="llm"
            defaultValue={JSON.stringify(config.llm)}
            onChange={(e) => {
              config.llm = JSON.parse(e.currentTarget.value)
            }}
          />
           {/* <Select
        value={""}
        style={{ width: 80, margin: '0 8px' }}
        onChange={(e) => {
          config.llm.model = e.Symbol
        }}
      >
        <Option value="rmb">RMB</Option>
        <Option value="dollar">Dollar</Option>
      </Select> */}
        </section>
        <div className='flex justify-center items-center'>
          <Button className='mr-8' onClick={() => {
            window.close();
          }}>取消</Button>
          <Button type="primary" onClick={
            async () => {
              await window.api.sql(`update config set content=@content where id = 1`,
                'update',
                {
                  content: JSON.stringify(config)
                })
              window.close();
            }
          }
          >保存</Button>
        </div>
      </main>
    </Form>
  )
}