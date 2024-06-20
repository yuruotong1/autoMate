import styles from './styles.module.scss'

export const Setting = () => {
    return (
        <main className={styles.settingPage}>
            <h1>Setting</h1>
            <section>
                <h5>快捷键定义</h5>
                <input type="text"/>
            </section>
            <section>
                <h5>数据库</h5>
                <input type="text"/>
            </section>
        </main>
    )
}