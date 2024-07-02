import { useStore } from "@renderer/store/useStore";
import { requireAlignmentPrompt, programmerPrompt} from "./prompt";
import useOpenai from "./useOpenai";

export  default ()=>{
  const setIsCodeLoading = useStore(state => state.setIsCodeLoading)

  const getResponse=(chat_messages: Array<any>, id:number, revalidator: () => void)=>{
  const messages = chat_messages.map((m) => {
    return {
      role: m.role, 
      content: m.content
    }
  })

  // 添加 system 消息
  messages.unshift({
    role: 'system',
    content: requireAlignmentPrompt()
  });
  const response = useOpenai(requireAlignmentPrompt(), messages, (allContent)=>{
    const programmerCallBack = (allContent: string) => {  
      allContent = allContent.replace(/^```python/, "").replace(/^```/, "").replace(/```python$/, "").replace(/```$/, "").trim()
      window.api.sql('update contents set content = @content where id = @id', 
      'update', 
      {content: allContent, id})
      // 更新数据
      revalidator()
      // 关闭loading
      setIsCodeLoading(false)
  }
  if (allContent.includes("【自动化方案】")) {
    setIsCodeLoading(true)
    useOpenai(programmerPrompt(), [{
      role: "user",
      content: allContent
    }], (allContent)=>{
      programmerCallBack(allContent)
    })
  } else {
    console.log("Response does not contain '【自动化方案】'");
  }
  })
  return response
  }
  return {getResponse}
  
}

