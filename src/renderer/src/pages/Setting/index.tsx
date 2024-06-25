import { Form } from 'react-router-dom'
import styles from './styles.module.scss'
import { useState } from 'react'
import { useStore } from '@renderer/store/useStore'

export const Setting = () => {
    // const config = useLoaderData() as ConfigDataType
    const [keys, setKeys] = useState<string[]>([])
    const config = useStore(state => state.config)
    const setConfig = useStore(state => state.setConfig)
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
                                    setConfig({...config, shortCut: e.currentTarget.value})
                                    window.api.shortCut(e.currentTarget.value)
                                }
                            }

                        }}
                    />
                </section>
                <section>
                    <h5>数据库</h5>
                    <input 
                      type="text" 
                      name="databaseDirectory" 
                      readOnly
                      defaultValue={config.databaseDirectory} 
                      onClick={
                        async (e)=>{
                          const path = await window.api.selectDatabaseDirectory()
                          setConfig({...config, databaseDirectory: path})
                          e.currentTarget.value = path
                        }
                      }
                      
                      />
                </section>

                <section>
                    <h5>大模型配置信息</h5>
                    <input 
                      type="text" 
                      name="llm-model" 
                      defaultValue={JSON.stringify(config.llm)}
                      onChange={(e)=>{
                        const value = JSON.parse(e.target.value)
                        setConfig({...config, llm: value})
                      }}
                      />
                </section>
            </main>
        </Form>
    )
}