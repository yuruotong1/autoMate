
import useCodeSelect from '@renderer/hooks/useCodeSelect'
import styles from './styles.module.scss'
export default function Result() {
    const {data, id} = useCodeSelect()
    return (
    <main className = {styles.main}>
        {data.map((item) => (
            <div key={item.id} className={item.id == id? styles.active : ''}>
                <p>{item.content}</p>
            </div>
        ))}

    </main>
  )
}
