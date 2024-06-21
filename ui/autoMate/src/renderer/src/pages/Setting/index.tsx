import { Form, useLoaderData, useSubmit } from 'react-router-dom'
import styles from './styles.module.scss'
import { useState } from 'react'

export const Setting = () => {
    const config = useLoaderData() as ConfigDataType
    const submit = useSubmit()
    const [keys, setKeys] = useState<string[]>([])
    return (
        <Form method="POST">
            <main className={styles.settingPage}>
                <h1>Setting</h1>
                <section>
                    <h5>快捷键定义</h5>
                    <input
                        type="text"
                        name="shortcut"
                        defaultValue={config.shortCut}
                        readOnly
                        onKeyDown={(e) => {
                            if (e.metaKey || e.ctrlKey || e.altKey) {
                                keys.push(e.code.replace(/Left|Right|Key|Digit/, ''))
                                setKeys(keys)
                                e.currentTarget.value = keys.join('+')
                            }

                        }}
                        onKeyUp={(e) => {
                            submit(e.currentTarget.form, {method: 'POST'})
                            setKeys([])
                        }}
                    />
                </section>
                <section>
                    <h5>数据库</h5>
                    <input type="text" name="databaseDirectory" defaultValue={config.databaseDirectory} />
                </section>
            </main>
        </Form>
    )
}