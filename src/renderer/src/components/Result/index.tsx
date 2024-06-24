
import useSelect from '@renderer/hooks/useSelect'
import styles from './styles.module.scss'
export default function Result() {
    const {data, selectId, select} = useSelect()
    return (
    <main className = {styles.main}>
        {data.map((item) => (
            <div key={item.id} 
            className={item.id == selectId? styles.active : ''}
            onClick={()=>select(item.id)}
            >
                <p>{item.title}</p>
            </div>
        ))}

    </main>
  )
}
