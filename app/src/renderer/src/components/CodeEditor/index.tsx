import CodeMirror, { EditorView } from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import { Drawer, FloatButton } from 'antd';
import { QuestionCircleOutlined } from '@ant-design/icons';
import Chat from '@renderer/components/Chat';
import styles from "./styles.module.scss"
import { useEffect, useRef } from 'react';
interface CodeEditorProps {
  id: number;
  defaultValue: string;
  revalidator: () => void;
  open: boolean;
  setOpen: (open: boolean) => void;
  search: string;
}
export default function CodeEditor(props: CodeEditorProps) {
  const { id, defaultValue, revalidator, open, setOpen, search} = props;
  const floatButton = useRef(null)
  function addText() {
    if (floatButton) {
      if (floatButton.current){
        // @ts-ignore
        const html = floatButton.current.innerHTML
        if (html.indexOf('智子助手') < 0) {
          const newHtml = html + '<span style="font-size:10px">智子助手</span>'
          if (floatButton.current) {
            // @ts-ignore
            floatButton.current.innerHTML= newHtml
          }
        }
      }
    }
  }
  useEffect(()=>{
    if (search) {
      setOpen(true)
    }
    addText()
  }, [])
  return (
    <div>
        <FloatButton icon={<QuestionCircleOutlined />} ref={floatButton} type="primary" onClick={() => {
        setOpen(true);
      }} />
      <Drawer
        title="智子"
        onClose={() => {
          setOpen(false);
        }}
        open={open}
        styles={{
          body: {
            padding: 0,
          },
        }}>
           <Chat id={id} revalidator={revalidator} search={search}/>
      </Drawer>
      <CodeMirror
        maxHeight='550px'
        maxWidth='850px'
        value={defaultValue}
        className={styles.codeMirror}
        onChange={async (value) => {
          await window.api.sql(
            `update contents set content=@content where id=@id`,
            "update",
            {
              id,
              content: value
            }
        )
        }}
        extensions={[
          python(),
          EditorView.theme({
          "&.cm-editor.cm-focused": {
            outline: "none !important",
          },
        }),]}
      />
    </div>
  );
};
