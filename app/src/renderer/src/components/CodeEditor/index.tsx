import CodeMirror from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import { useStore } from '@renderer/store/useStore';
export default function CodeEditor() {  
  const code = useStore(state=>state.code)
  const setCode = useStore(state=>state.setCode)
  
  return (
    <CodeMirror 
    theme="dark"
    // className="w-full h-full"
    height="500px"
    width='600px'
    value={code}
    onChange={(value)=>{
      setCode(value)
    }}
    extensions={[python()]} 
    />
  );
}
