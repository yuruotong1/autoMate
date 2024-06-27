import CodeMirror from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
// import { StreamLanguage } from '@codemirror/language';
export default function Code() {  

  return (
    <CodeMirror 
    theme="dark"
    className="w-full h-full fixed overflow-auto"
    height="100%"
    width='400px'
    value={""} 
    extensions={[python()]} 
    />
  );
}
