# 开发者文档

## ProxyPin MCP Server 传康KK 优化增强版 - 开发者指南

### 📋 项目概述

本项目是对原版 ProxyPin MCP Server 的深度优化和功能增强，由传康KK进行二次开发。主要提升了系统的性能、稳定性和易用性。

### 👨‍💻 开发者信息

- **二次开发者**: 传康KK
- **GitHub**: [1837620622](https://github.com/1837620622)
- **微信**: 1837620622
- **邮箱**: 2040168455@qq.com
- **平台**: 咸鱼/B站 万能程序员

### 🚀 核心优化特性

#### 1. 连接池优化
- 使用 `requests.Session` 实现连接复用
- 配置重试策略和超时机制
- 支持并发请求处理

#### 2. 线程安全
- 使用 `threading.Lock` 保护共享资源
- 原子操作确保计数器安全
- 多线程环境稳定运行

#### 3. 异常处理增强
- 分类异常处理机制
- 详细错误信息输出
- 自动重试网络请求

#### 4. 性能监控
- 实时响应时间统计
- 详细的调用日志记录
- 系统资源使用监控

#### 5. 参数验证
- 严格的输入参数检查
- 数据类型转换和清理
- 边界条件处理

### 🔧 技术架构

#### 依赖项
```python
fastmcp>=1.0.0      # MCP框架
requests>=2.31.0    # HTTP请求库
urllib3>=1.26.0     # HTTP客户端
```

#### 核心模块

1. **连接管理模块**
   ```python
   def create_optimized_session() -> requests.Session
   ```
   - 创建优化的HTTP会话
   - 配置重试策略
   - 设置连接池参数

2. **工具调用模块**
   ```python
   def call_proxypin_tool(tool_name: str, arguments: dict) -> Any
   ```
   - 线程安全的工具调用
   - 性能监控和日志记录
   - 异常分类处理

3. **MCP工具函数**
   - 30+ 个优化的工具函数
   - 参数验证和错误处理
   - 详细的文档注释

### 📁 项目结构

```
proxypin-mcp-server-1.0.0/
├── proxypin_mcp_server.py    # 主程序文件
├── requirements.txt          # 依赖配置
├── setup.py                 # 安装配置
├── README.md               # 用户文档
├── DEVELOPER.md            # 开发者文档
├── LICENSE                 # 开源协议
├── .gitignore             # Git忽略文件
├── proxypin_mcp_server.spec # PyInstaller配置
└── .github/workflows/
    └── release.yml         # CI/CD配置
```

### 🔨 开发环境搭建

#### 1. 环境要求
- Python 3.8+
- Git
- ProxyPin 主程序

#### 2. 本地开发
```bash
# 克隆仓库
git clone https://github.com/1837620622/proxypin-mcp-server.git
cd proxypin-mcp-server

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 运行测试
python proxypin_mcp_server.py
```

#### 3. 开发调试
```bash
# 设置调试环境变量
export PROXYPIN_HOST=127.0.0.1
export PROXYPIN_PORT=17777

# 启用调试日志
export PYTHONPATH=.
python -c "import logging; logging.getLogger().setLevel(logging.DEBUG)"
```

### 🔄 发布流程

#### 1. 版本管理
```bash
# 更新版本号
# 编辑 proxypin_mcp_server.py 中的 __version__ 变量
# 编辑 setup.py 中的 version 参数
```

#### 2. 自动构建
本项目使用 GitHub Actions 进行自动构建和发布：

- **Windows版本**: x64 和 x86 架构
- **macOS版本**: Intel (x64) 和 Apple Silicon (arm64) 架构
- **Python包**: 源码和wheel格式

#### 3. 发布命令
```bash
# 创建发布标签
git tag -a v2.0.0-chuankangkk -m "传康KK 优化增强版 v2.0.0"
git push origin v2.0.0-chuankangkk

# GitHub Actions 将自动构建和发布
```

### 🧪 测试指南

#### 1. 单元测试
```bash
# 安装测试依赖
pip install pytest pytest-cov

# 运行测试
pytest tests/ -v

# 测试覆盖率
pytest --cov=proxypin_mcp_server tests/
```

#### 2. 集成测试
```bash
# 确保ProxyPin服务运行
# 启动测试服务器
python proxypin_mcp_server.py &

# 运行集成测试
python -m pytest tests/integration/ -v
```

#### 3. 性能测试
```bash
# 压力测试
python tests/performance_test.py

# 内存泄漏检测
python -m memory_profiler proxypin_mcp_server.py
```

### 📊 代码质量

#### 1. 代码规范
- **PEP 8**: Python代码风格指南
- **类型提示**: 使用 typing 模块
- **文档字符串**: 详细的函数说明

#### 2. 质量检查
```bash
# 代码格式化
black proxypin_mcp_server.py

# 代码检查
flake8 proxypin_mcp_server.py

# 类型检查
mypy proxypin_mcp_server.py
```

#### 3. 性能优化
- 连接池复用减少TCP握手
- 异步操作提升响应速度
- 内存管理避免泄漏
- 日志级别动态调整

### 🔐 安全考虑

#### 1. 输入验证
- 严格的参数类型检查
- SQL注入防护
- XSS攻击防护

#### 2. 网络安全
- HTTPS支持
- 证书验证
- 超时设置

#### 3. 日志安全
- 敏感信息脱敏
- 日志文件权限控制
- 审计日志记录

### 🐛 调试指南

#### 1. 常见问题
- **连接失败**: 检查ProxyPin服务状态
- **权限错误**: 确认文件访问权限
- **性能问题**: 查看性能监控日志

#### 2. 日志分析
```bash
# 查看详细日志
tail -f proxypin_mcp.log

# 按级别过滤
grep "ERROR" proxypin_mcp.log
grep "INFO" proxypin_mcp.log
```

#### 3. 调试工具
```python
# 启用调试模式
import logging
logging.getLogger().setLevel(logging.DEBUG)

# 性能分析
import cProfile
cProfile.run('main()')
```

### 📈 性能优化建议

#### 1. 连接优化
- 合理设置连接池大小
- 启用HTTP keep-alive
- 使用HTTP/2协议

#### 2. 内存优化
- 及时释放大对象
- 使用生成器减少内存占用
- 定期垃圾回收

#### 3. CPU优化
- 避免不必要的序列化
- 使用缓存减少重复计算
- 异步处理I/O操作

### 📝 贡献指南

#### 1. 提交规范
```bash
# 提交格式
git commit -m "feat: 添加新功能描述"
git commit -m "fix: 修复bug描述"
git commit -m "docs: 更新文档"
git commit -m "style: 代码格式化"
git commit -m "refactor: 代码重构"
git commit -m "test: 添加测试"
```

#### 2. 分支策略
- `main`: 主分支，稳定版本
- `develop`: 开发分支
- `feature/*`: 功能分支
- `hotfix/*`: 紧急修复分支

#### 3. Pull Request
- 详细描述修改内容
- 包含测试用例
- 更新相关文档
- 通过代码审查

### 📞 技术支持

如有技术问题，请联系开发者：

- **GitHub Issues**: [提交问题](https://github.com/1837620622/proxypin-mcp-server/issues)
- **微信**: 1837620622
- **邮箱**: 2040168455@qq.com
- **平台**: 咸鱼/B站 万能程序员

### 📜 版权声明

本项目基于MIT协议开源，欢迎使用和贡献代码。

---

**ProxyPin MCP Server 传康KK 优化增强版**  
*让HTTP请求分析更简单、更高效*

作者：传康KK  
版本：2.0.0-chuankangkk  
更新时间：2025-12-19
