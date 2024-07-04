import { MutableRefObject } from "react"

export default() => {
    const setIgnoreMouseEvents = <T extends HTMLElement>(el: MutableRefObject<T>) => {
        el.current?.addEventListener('mouseover', ()=>{
            window.api.setIgnoreMouseEvents(false)
          })
      
        document.body.addEventListener('mouseover', (e: MouseEvent)=>{
        // if (e.target === document.body) {
        //     window.api.setIgnoreMouseEvents(true, {forward: true})
        // }
        })
    }
    return {setIgnoreMouseEvents}
}

