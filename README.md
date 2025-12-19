# ProxyPin MCP Server - 传康KK 优化增强版

![Version](https://img.shields.io/badge/version-2.0.0--chuankangkk-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)
![Author](https://img.shields.io/badge/author-传康KK-red)

> 🚀 **高性能HTTP请求捕获与分析工具** - ProxyPin MCP Server的优化增强版本

## 👨‍💻 开发者信息

**二次开发者**: 传康KK  
**GitHub**: [1837620622](https://github.com/1837620622)  
**微信**: 1837620622  
**邮箱**: 2040168455@qq.com  
**平台**: 咸鱼/B站 万能程序员

## ✨ 功能特性

### 🔥 传康KK 增强特性
- **高性能连接池优化** - 支持并发请求处理
- **智能重试机制** - 自动处理网络异常
- **线程安全操作** - 多线程环境下稳定运行
- **详细日志记录** - 完整的操作日志追踪
- **参数验证增强** - 严格的输入参数检查
- **性能监控** - 实时响应时间监控
- **异常分类处理** - 精确的错误信息提示
- **启动横幅显示** - 美观的启动界面

### 🌟 核心功能
- **HTTP请求捕获** - 实时捕获和分析HTTP请求
- **智能请求搜索** - 支持多维度条件过滤
- **代码生成** - 支持Python、JavaScript、cURL等多种语言
- **请求重放** - 一键重放历史请求
- **HAR文件操作** - 导入导出HAR格式文件
- **请求对比分析** - 详细的请求差异对比
- **API端点提取** - 自动识别和分组API端点
- **实时统计** - 请求数量、响应时间等统计信息

## 🚀 快速开始

### 系统要求
- Python 3.8+
- ProxyPin 主程序运行在17777端口

### Mac版本安装使用

#### 方式一：下载可执行文件
1. 从 [Releases](https://github.com/1837620622/proxypin-mcp-server/releases) 下载对应版本
2. 解压文件
```bash
tar -xzf proxypin-mcp-server-macos-arm64.tar.gz
```
3. 给予执行权限
```bash
chmod +x proxypin-mcp-server-macos-arm64
```
4. 运行程序
```bash
./proxypin-mcp-server-macos-arm64
```

#### 方式二：Python源码运行
1. 克隆仓库
```bash
git clone https://github.com/1837620622/proxypin-mcp-server.git
cd proxypin-mcp-server
```
2. 安装依赖
```bash
pip install -r requirements.txt
```
3. 运行服务
```bash
python proxypin_mcp_server.py
```

### Windows版本安装使用

#### 方式一：下载可执行文件
1. 从 [Releases](https://github.com/1837620622/proxypin-mcp-server/releases) 下载Windows版本
2. 解压zip文件
3. 双击运行 `proxypin-mcp-server-windows-x64.exe`

#### 方式二：Python源码运行
1. 确保已安装Python 3.8+
2. 下载项目代码
3. 安装依赖：`pip install -r requirements.txt`
4. 运行：`python proxypin_mcp_server.py`

## 🔧 配置说明

### 环境变量
```bash
# ProxyPin服务地址配置
export PROXYPIN_HOST=127.0.0.1    # 默认本机
export PROXYPIN_PORT=17777         # 默认端口
```

### 配置文件
程序会自动生成日志文件 `proxypin_mcp.log`，包含详细的运行日志。

## 📚 API文档

### 工具函数列表

#### 🔍 搜索相关
- `search_requests()` - 高级HTTP请求搜索
- `get_request_details()` - 获取请求详细信息
- `find_similar_requests()` - 查找相似请求

#### 🎯 操作相关
- `replay_request()` - 重放指定请求
- `generate_code()` - 生成多语言代码
- `get_curl()` - 生成cURL命令

#### 📊 分析相关
- `get_statistics()` - 获取统计信息
- `compare_requests()` - 请求对比分析
- `extract_api_endpoints()` - API端点提取

#### 🛠️ 配置相关
- `start_proxy()` - 启动代理服务
- `stop_proxy()` - 停止代理服务
- `set_config()` - 配置代理设置
- `get_system_info()` - 获取系统信息（传康KK专属）

## 💻 使用示例

### 基础搜索
```python
# 搜索包含特定关键词的请求
search_requests(query="api/user", limit=10)

# 按HTTP方法过滤
search_requests(method="POST", status_code="200")

# 按域名搜索
search_requests(domain="example.com")
```

### 代码生成
```python
# 生成Python代码
generate_code(request_id="12345", language="python")

# 生成cURL命令
get_curl(request_id="12345")
```

### 请求分析
```python
# 获取统计信息
get_statistics()

# 对比两个请求
compare_requests(request_id_1="123", request_id_2="456")
```

## 🎨 界面预览

启动时显示传康KK专属横幅：
```
╔══════════════════════════════════════════════════════════════════════╗
║                    ProxyPin MCP Server 传康KK 增强版                    ║
║                                                                      ║
║  版本: 2.0.0-chuankangkk     作者: 传康KK (GitHub)                    ║
║  微信: 1837620622              邮箱: 2040168455@qq.com        ║
║  平台: 咸鱼/B站 万能程序员      GitHub: 1837620622             ║
║                                                                      ║
║  功能特性:                                                           ║
║  • 高性能HTTP请求捕获与分析    • 智能请求过滤与搜索               ║
║  • 代码生成与重放功能          • HAR文件导入导出                 ║
║  • 请求对比分析               • API端点智能提取                 ║
║  • 增强错误处理与日志记录      • 连接池优化                     ║
║  • 线程安全操作               • 异步处理支持                   ║
║                                                                      ║
║  启动中...                                                          ║
╚══════════════════════════════════════════════════════════════════════╝
```

## 🚨 常见问题

### Q: macOS提示"无法验证开发者"
A: 在系统偏好设置 → 安全性与隐私 → 通用中，选择"允许从任何来源下载的应用"，或使用命令：
```bash
sudo spctl --master-disable
```

### Q: 连接ProxyPin失败
A: 请确保：
1. ProxyPin主程序正在运行
2. 监听端口为17777
3. 防火墙未阻止连接

### Q: Python依赖安装失败
A: 尝试使用以下命令：
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 🔄 更新日志

### v2.0.0-chuankangkk (2024-12)
- 🎉 **传康KK 优化增强版发布**
- ✨ 添加连接池优化和智能重试机制
- 🚀 实现线程安全操作
- 📊 增加详细的性能监控和日志记录
- 🛡️ 加强参数验证和异常处理
- 🎨 添加启动横幅和系统信息功能
- 📱 支持多平台自动构建发布

### v1.0.0 (原版)
- 基础MCP工具功能
- HTTP请求捕获
- 简单搜索功能

## 🤝 贡献指南

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 开源协议

本项目基于 MIT 协议开源 - 详见 [LICENSE](LICENSE) 文件

## 💬 联系方式

- **作者**: 传康KK
- **GitHub**: [1837620622](https://github.com/1837620622)
- **微信**: 1837620622
- **邮箱**: 2040168455@qq.com
- **咸鱼**: 万能程序员
- **B站**: 万能程序员

## ⭐ 支持项目

如果这个项目对你有帮助，请给个Star⭐支持一下！

---

<div align="center">

**ProxyPin MCP Server 传康KK 优化增强版**

*让HTTP请求分析更简单、更高效*

[![GitHub stars](https://img.shields.io/github/stars/1837620622/proxypin-mcp-server.svg?style=social&label=Star)](https://github.com/1837620622/proxypin-mcp-server/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/1837620622/proxypin-mcp-server.svg?style=social&label=Fork)](https://github.com/1837620622/proxypin-mcp-server/network/members)

</div>
