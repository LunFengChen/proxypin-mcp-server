# ProxyPin MCP Server

ProxyPin 的 MCP 服务器，作用通俗点说就是 **抓包软件有啥功能，ai都能调用啥功能**；

功能特性
- 请求管理: 高级搜索、获取请求详情、重放请求、最近请求、清空请求
- 代码/命令生成: 生成 Python/JS/cURL 代码或 cURL 命令
- 重写与拦截: 屏蔽 URL、添加请求/响应重写规则
- 脚本管理: 创建/更新/列出 JavaScript 脚本用于请求处理
- 代理控制: 启动/停止代理、获取代理状态、Hosts 映射
- HAR 导入导出: 导出 HAR、导入 HAR
- 分析统计: 请求统计、对比请求、提取 API 端点
- 其它: 设置 ProxyPin 配置、导出统计信息等

环境要求
- Python 3.10+
- ProxyPin: 默认本机监听17777作为mcp通信端口， `http://127.0.0.1:17777`（不要和抓包工具的9099端口搞混，这是两个概念）
- 如果需要手机抓包，随便找一个能转发手机请求的软件就行，然后局域网挂代理到电脑的17777端口；这里推荐proxypin的app版本，appproxy等等；
- Python 依赖: `fastmcp`, `requests`

安装
```bash
git clone https://your-repo/proxypin-mcp-server.git
cd proxypin-mcp-server
pip install fastmcp requests
```

使用
1. 启动 ProxyPin 然后能正常抓包；默认端口是9099
    > 这一步是你本来就要做的，跟mcp没关系

2. 启动 mcp 服务，并设置监听端口 17777
    > 这一步是为了proxypin监听ai的mcp工具调用请求

3. 问你的ai连上没有 或者 手动测试
```bash
python proxypin_mcp_server.py
```

在 IDE 中配置 MCP（示例）：
```json
"proxypin-mcp": {
	"command": "python",
	"args": ["path/to/proxypin_mcp_server.py"],
	"disabled": false,
	"autoApprove": [
		"search_requests", "get_request_details", "replay_request", "generate_code", "get_curl",
		"block_url", "add_response_rewrite", "add_request_rewrite", "update_script", "get_scripts",
		"set_config", "add_host_mapping", "get_proxy_status", "start_proxy", "stop_proxy",
		"export_har", "import_har", "get_recent_requests", "clear_requests", "get_statistics",
		"compare_requests", "find_similar_requests", "extract_api_endpoints"
	]
}
```

工具列表（主要）

请求与搜索 (5)
- `search_requests` - 高级搜索 HTTP 请求
- `get_request_details` - 获取请求详细信息
- `replay_request` - 重放请求
- `get_recent_requests` - 获取最近请求列表（Legacy）
- `clear_requests` - 清空捕获的请求

代码与命令 (2)
- `generate_code` - 生成示例代码（python/js/curl）
- `get_curl` - 生成 cURL 命令

重写与拦截 (3)
- `block_url` - 屏蔽 URL
- `add_response_rewrite` - 添加响应重写规则
- `add_request_rewrite` - 添加请求重写规则

脚本管理 (2)
- `update_script` - 创建或更新 JavaScript 脚本
- `get_scripts` - 列出所有脚本

代理与网络 (4)
- `start_proxy` - 启动代理服务器
- `stop_proxy` - 停止代理服务器
- `get_proxy_status` - 获取代理状态
- `add_host_mapping` - 添加 Hosts 映射

HAR 与导入导出 (2)
- `export_har` - 导出 HAR
- `import_har` - 导入 HAR

分析与统计 (3)
- `get_statistics` - 获取请求统计信息
- `compare_requests` - 对比两个请求
- `extract_api_endpoints` - 提取并分组 API 端点

其它 (2)
- `set_config` - 设置 ProxyPin 配置（例如 system_proxy, ssl_capture）
- `find_similar_requests` - 查找相似请求

常见问题
- ProxyPin 连接失败:  配不上一般都是整个通信过程没搞懂导致端口配的乱七八糟；
- 请求为空: 检查是否正确启用了proxypin代理并已捕获流量

贡献
欢迎提交 issue 或 PR 来补充更多工具、增强稳定性或完善文档。

License
MIT
