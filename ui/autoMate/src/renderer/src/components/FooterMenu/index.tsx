import { Add, DatabaseConfig } from '@icon-park/react'
import { Link, useSubmit } from 'react-router-dom'

export const FooterMenu = () => {
  const submit = useSubmit()
  return (
    <>
      <div className="nav">
        <Add theme="outline" size="20" fill="#333" onClick={(_e)=>
          submit(null, {method:'POST'})
        }/>
        <Link to="/config">
        <DatabaseConfig theme="outline" size="20" fill="#333"/>
        </Link>
        </div>
    </>
  )
}
