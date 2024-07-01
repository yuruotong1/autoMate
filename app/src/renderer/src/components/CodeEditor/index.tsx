import CodeMirror from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import { Drawer, FloatButton } from 'antd';
import { useState } from 'react';
import { QuestionCircleOutlined } from '@ant-design/icons';
import Chat from '@renderer/components/Chat';
import "./codeEditor.scss"
interface CodeEditorProps {
  id: number;
  defaultValue: string;
  revalidator: () => void;

}

export default function CodeEditor(props: CodeEditorProps) {
  const { id, defaultValue, revalidator} = props;
  const [open, setOpen] = useState(false);

  return (
    <div>
        <FloatButton icon={<QuestionCircleOutlined />} type="primary" onClick={() => {
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
           <Chat id={id} revalidator={revalidator}/>
      </Drawer>

      <CodeMirror
        // theme="dark"
        // height="100%"
        maxHeight='550px'
        // width='587px'
        className='code-mirror'
        value={defaultValue}
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
        extensions={[python()]}
      />
       
      {/* </Spin> */}
    </div>
  );
};
