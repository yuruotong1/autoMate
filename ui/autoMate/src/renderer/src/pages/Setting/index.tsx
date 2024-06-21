import { Form, useSubmit } from 'react-router-dom'
import styles from './styles.module.scss'

export const Setting = () => {
    const submit = useSubmit()
    return (
        <Form method="POST">
        <main className={styles.settingPage}>
            <h1>Setting</h1>
            <section>
                <h5>快捷键定义</h5>
                <input 
                    type="text"
                    name="shortcut"
                    onKeyUp={(e)=>{
                        submit(e.currentTarget.form, {method: 'POST'})
                    }}
                />
            </section>
            <section>
                <h5>数据库</h5>
                <input type="text" name="databaseDirectory" defaultValue="abc"/>
            </section>
        </main>
        </Form>
    )
}