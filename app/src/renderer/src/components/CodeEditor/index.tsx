import CodeMirror from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import { useStore } from '@renderer/store/useStore';
export default function CodeEditor() {  
  const code = useStore(state=>state.code)
  
  return (
    <CodeMirror 
    theme="dark"
    className="w-full h-full fixed overflow-auto"
    height="100%"
    width='400px'
    value={code} 
    extensions={[python()]} 
    />
  );
}
