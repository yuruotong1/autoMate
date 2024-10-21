## 开发用README
### 入口是main.py
- pip install 完直接执行

### 现在两部分还没接起来
- action这边可以添加API KEY， 可以和PM聊天了
- Agent可以看具体交流的框架
- code_utils是run-task的逻辑
- 后端测试：
  ```
  python -m unittest autoMate.tests.test_runner
  python -m unittest autoMate.tests.test_models
  ```

### 需要最后思考确认多智能体合作的细节
- 谁和谁说什么，用什么格式
- 谁做什么
  - 我们写代码替他做，比如agent说这里有Python代码，我们就提取出来写进去
- 需要什么上下文信息

### 目标是先跑通生成代码的流程
- 生成的是垃圾也行
- 还有很多优化没上，现在zero-shot表现不好是正常的
- 先给人用上

