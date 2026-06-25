支持的事件（8 种）
事件 触发时机 能否阻止操作
PreToolUse 工具执行前 ✅
PostToolUse 工具执行后 ❌
Stop Agent 完成响应时 ✅
UserPromptSubmit 你发送消息时 ✅
SubagentStop 子代理完成时 ✅
SessionStart 会话启动/恢复 ❌
SessionEnd 会话结束 ❌
PreCompact 上下文压缩前 ❌
