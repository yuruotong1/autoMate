import CodeMirror from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import { Drawer, FloatButton, Spin } from 'antd';
import { QuestionCircleOutlined } from '@ant-design/icons';
import Chat from '@renderer/components/Chat';
import "./codeEditor.scss"
import { useStore } from '@renderer/store/useStore';
interface CodeEditorProps {
  id: number;
  defaultValue: string;
  revalidator: () => void;
  open: boolean;
  setOpen: (open: boolean) => void;

}
export default function CodeEditor(props: CodeEditorProps) {
  const { id, defaultValue, revalidator, open, setOpen} = props;
  const isCodeLoading = useStore(state => state.isCodeLoading)
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
      <Spin spinning={isCodeLoading} tip="根据自动化方案生成代码中，请稍等...">
      <CodeMirror
        maxHeight='550px'
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
      </Spin>
    </div>
  );
};
