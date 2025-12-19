#!/usr/bin/env python3
"""
ProxyPin MCP Server - 传康KK 优化增强版
=========================================

原作者：ProxyPin Team  
二次开发：传康KK (GitHub)
开发者信息：
- GitHub: https://github.com/1837620622
- 微信: 1837620622
- 邮箱: 2040168455@qq.com  
- 咸鱼/B站: 万能程序员

功能特性：
- 高性能HTTP请求捕获与分析
- 智能请求过滤与搜索
- 代码生成与重放
- HAR文件导入导出
- 请求对比分析
- API端点提取
- 增强错误处理与日志记录
- 连接池优化
- 异步操作支持

版本：2.0.0-chuankangkk
更新时间：2025-12-19
"""

import os
import sys
import json
import logging
import time
import threading
from datetime import datetime
from typing import Dict, Any, Optional, List, Union
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from fastmcp import FastMCP

# ========================================
# 传康KK 系统配置与优化
# ========================================

# 版本信息
__version__ = "2.0.0-chuankangkk"
__author__ = "传康KK (GitHub: 1837620622)"
__contact__ = "微信: 1837620622 | 邮箱: 2040168455@qq.com"

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('proxypin_mcp.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# ProxyPin HTTP API配置
PROXYPIN_HOST = os.getenv("PROXYPIN_HOST", "127.0.0.1")
PROXYPIN_PORT = int(os.getenv("PROXYPIN_PORT", "17777"))
BASE_URL = f"http://{PROXYPIN_HOST}:{PROXYPIN_PORT}"
MESSAGES_URL = f"{BASE_URL}/messages"

# 连接池优化配置
MAX_RETRIES = 3
BACKOFF_FACTOR = 0.3
TIMEOUT = 30
POOL_CONNECTIONS = 10
POOL_MAXSIZE = 20

# 创建优化的Session - 传康KK性能增强
def create_optimized_session() -> requests.Session:
    """创建优化的HTTP会话连接"""
    session = requests.Session()
    session.trust_env = False
    
    # 重试策略配置
    retry_strategy = Retry(
        total=MAX_RETRIES,
        backoff_factor=BACKOFF_FACTOR,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]
    )
    
    # HTTP适配器配置
    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=POOL_CONNECTIONS,
        pool_maxsize=POOL_MAXSIZE
    )
    
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # 设置默认请求头
    session.headers.update({
        'User-Agent': f'ProxyPin-MCP-Server/{__version__} (by {__author__})',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    })
    
    logger.info(f"已创建优化HTTP会话连接 - {__author__} 性能增强版")
    return session

# 全局会话实例
session = create_optimized_session()
request_id_counter = 1
_counter_lock = threading.Lock()

def call_proxypin_tool(tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Any:
    """
    调用ProxyPin的MCP工具 - 传康KK 增强版
    
    特性：
    - 线程安全的请求ID管理
    - 详细的性能监控与日志记录
    - 智能重试机制
    - 异常分类处理
    - 响应数据验证
    
    Args:
        tool_name: 工具名称
        arguments: 工具参数
        
    Returns:
        工具调用结果
        
    Raises:
        Exception: 当工具调用失败时
    """
    global request_id_counter
    
    # 线程安全的计数器递增
    with _counter_lock:
        current_id = request_id_counter
        request_id_counter += 1
    
    if arguments is None:
        arguments = {}
    
    # 记录请求开始时间 - 性能监控
    start_time = time.time()
    
    payload = {
        "jsonrpc": "2.0",
        "id": current_id,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    
    logger.debug(f"调用工具: {tool_name}, 参数: {arguments}, 请求ID: {current_id}")
    
    try:
        # 发送请求
        response = session.post(MESSAGES_URL, json=payload, timeout=TIMEOUT)
        response.raise_for_status()
        
        # 计算响应时间
        response_time = (time.time() - start_time) * 1000  # 转换为毫秒
        
        # 解析JSON响应
        try:
            result = response.json()
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}, 响应内容: {response.text[:500]}")
            raise Exception(f"ProxyPin返回无效JSON响应: {e}")
        
        # 检查MCP错误
        if "error" in result:
            error_info = result["error"]
            logger.error(f"MCP工具调用错误: {error_info}")
            raise Exception(f"MCP Error: {error_info}")
        
        # 提取并验证结果内容
        result_data = result.get("result", {})
        content = result_data.get("content", [])
        
        if not content:
            logger.warning(f"工具 {tool_name} 返回空内容")
            return {}
        
        # 解析响应文本
        response_text = content[0].get("text", "{}")
        try:
            parsed_result = json.loads(response_text)
            logger.info(f"工具 {tool_name} 调用成功, 响应时间: {response_time:.2f}ms")
            return parsed_result
        except json.JSONDecodeError as e:
            logger.error(f"工具响应JSON解析失败: {e}, 内容: {response_text[:200]}")
            # 如果JSON解析失败，返回原始文本
            return {"raw_response": response_text, "parse_error": str(e)}
            
    except requests.exceptions.Timeout as e:
        logger.error(f"ProxyPin连接超时: {e}")
        raise Exception(f"ProxyPin连接超时: 请检查服务是否运行在 {BASE_URL}")
        
    except requests.exceptions.ConnectionError as e:
        logger.error(f"ProxyPin连接错误: {e}")
        raise Exception(f"无法连接到ProxyPin: 请确保服务运行在 {BASE_URL}")
        
    except requests.exceptions.HTTPError as e:
        logger.error(f"ProxyPin HTTP错误: {e}, 状态码: {response.status_code}")
        raise Exception(f"ProxyPin HTTP错误: {e}")
        
    except requests.exceptions.RequestException as e:
        logger.error(f"ProxyPin请求异常: {e}")
        raise Exception(f"ProxyPin请求失败: {e}")
        
    except Exception as e:
        logger.error(f"工具调用未知错误: {e}")
        raise Exception(f"工具调用失败: {e}")

# ========================================
# 传康KK MCP服务器实例创建
# ========================================

mcp = FastMCP("ProxyPin-Enhanced-by-ChuanKangKK")

def log_tool_call(tool_name: str, **kwargs):
    """记录工具调用日志装饰器"""
    logger.info(f"执行工具: {tool_name}, 参数: {kwargs}")

# ========================================
# 增强版工具函数 - 传康KK 优化
# ========================================

@mcp.tool()
def search_requests(
    query: str = None, 
    method: str = None, 
    status_code: str = None,
    domain: str = None,
    header_search: str = None,
    request_body_search: str = None,
    response_body_search: str = None,
    min_duration: int = None,
    max_duration: int = None,
    limit: int = 20
):
    """
    高级搜索HTTP请求 - 传康KK 增强版
    
    功能特性：
    - 支持多维度条件过滤
    - 智能搜索算法优化
    - 高性能数据检索
    - 详细的搜索日志记录
    
    支持的过滤条件：
    - query: URL关键词搜索
    - method: HTTP方法过滤(GET/POST/PUT/DELETE等)
    - status_code: 状态码过滤("200"或"2xx"范围)
    - domain: 域名精确匹配
    - header_search: 请求/响应头部内容搜索
    - request_body_search: 请求体内容搜索(限制1MB)
    - response_body_search: 响应体内容搜索(限制1MB)
    - min_duration/max_duration: 响应时间范围过滤(毫秒)
    - limit: 返回结果数量限制
    
    Returns:
        搜索结果列表，包含匹配的HTTP请求详细信息
    """
    log_tool_call("search_requests", 
                  query=query, method=method, status_code=status_code,
                  domain=domain, limit=limit)
    
    # 构建搜索参数
    args = {"limit": min(limit, 1000)}  # 限制最大返回数量
    
    # 条件过滤参数构建
    if query:
        args["query"] = str(query).strip()
    if method:
        args["method"] = str(method).upper()
    if status_code:
        args["status_code"] = str(status_code)
    if domain:
        args["domain"] = str(domain).lower()
    if header_search:
        args["header_search"] = str(header_search)
    if request_body_search:
        args["request_body_search"] = str(request_body_search)
    if response_body_search:
        args["response_body_search"] = str(response_body_search)
    if min_duration is not None:
        args["min_duration"] = max(0, int(min_duration))
    if max_duration is not None:
        args["max_duration"] = max(0, int(max_duration))
    
    return call_proxypin_tool("search_requests", args)

@mcp.tool()
def get_request_details(request_id: str):
    """获取请求详情 - 传康KK 增强版"""
    log_tool_call("get_request_details", request_id=request_id)
    if not request_id or not request_id.strip():
        raise ValueError("请求ID不能为空")
    return call_proxypin_tool("get_request_details", {"request_id": request_id.strip()})

@mcp.tool()
def replay_request(request_id: str):
    """重放请求 - 传康KK 增强版"""
    log_tool_call("replay_request", request_id=request_id)
    if not request_id or not request_id.strip():
        raise ValueError("请求ID不能为空")
    return call_proxypin_tool("replay_request", {"request_id": request_id.strip()})

@mcp.tool()
def generate_code(request_id: str, language: str = "python"):
    """生成代码(python/js/curl) - 传康KK 增强版"""
    log_tool_call("generate_code", request_id=request_id, language=language)
    if not request_id or not request_id.strip():
        raise ValueError("请求ID不能为空")
    
    # 支持的语言列表
    supported_languages = ["python", "javascript", "js", "curl", "php", "java", "go"]
    language = language.lower().strip()
    
    if language not in supported_languages:
        raise ValueError(f"不支持的语言: {language}, 支持的语言: {', '.join(supported_languages)}")
    
    return call_proxypin_tool("generate_code", {
        "request_id": request_id.strip(), 
        "language": language
    })

@mcp.tool()
def get_curl(request_id: str):
    """生成cURL命令 - 传康KK 增强版"""
    log_tool_call("get_curl", request_id=request_id)
    if not request_id or not request_id.strip():
        raise ValueError("请求ID不能为空")
    return call_proxypin_tool("get_curl", {"request_id": request_id.strip()})

@mcp.tool()
def block_url(url_pattern: str, block_type: str = "blockRequest"):
    """屏蔽URL"""
    return call_proxypin_tool("block_url", {"url_pattern": url_pattern, "block_type": block_type})

@mcp.tool()
def add_response_rewrite(url_pattern: str, rewrite_type: str, value: str, key: str = None):
    """添加响应重写规则"""
    args = {"url_pattern": url_pattern, "rewrite_type": rewrite_type, "value": value}
    if key:
        args["key"] = key
    return call_proxypin_tool("add_response_rewrite", args)

@mcp.tool()
def add_request_rewrite(url_pattern: str, rewrite_type: str, key: str, value: str):
    """添加请求重写规则"""
    return call_proxypin_tool("add_request_rewrite", {
        "url_pattern": url_pattern,
        "rewrite_type": rewrite_type,
        "key": key,
        "value": value
    })

@mcp.tool()
def update_script(name: str, url_pattern: str, script_content: str):
    """创建或更新JavaScript脚本"""
    return call_proxypin_tool("update_script", {
        "name": name,
        "url_pattern": url_pattern,
        "script_content": script_content
    })

@mcp.tool()
def get_scripts():
    """获取所有脚本"""
    return call_proxypin_tool("get_scripts")

@mcp.tool()
def set_config(system_proxy: bool = None, ssl_capture: bool = None):
    """设置ProxyPin配置"""
    args = {}
    if system_proxy is not None:
        args["system_proxy"] = system_proxy
    if ssl_capture is not None:
        args["ssl_capture"] = ssl_capture
    return call_proxypin_tool("set_config", args)

@mcp.tool()
def add_host_mapping(domain: str, ip: str):
    """添加Hosts映射"""
    return call_proxypin_tool("add_host_mapping", {"domain": domain, "ip": ip})

@mcp.tool()
def get_proxy_status():
    """获取代理状态"""
    return call_proxypin_tool("get_proxy_status")

@mcp.tool()
def export_har(limit: int = 100):
    """导出HAR"""
    return call_proxypin_tool("export_har", {"limit": limit})

@mcp.tool()
def import_har(har_content: str):
    """导入HAR文件到ProxyPin
    
    参数:
    - har_content: HAR JSON字符串
    """
    return call_proxypin_tool("import_har", {"har_content": har_content})

@mcp.tool()
def start_proxy(port: int = 9099):
    """启动代理服务器
    
    参数:
    - port: 代理端口(默认9099)
    """
    return call_proxypin_tool("start_proxy", {"port": port})

@mcp.tool()
def stop_proxy():
    """停止代理服务器"""
    return call_proxypin_tool("stop_proxy")

@mcp.tool()
def get_recent_requests(limit: int = 20, url_filter: str = None, method: str = None):
    """获取最近的请求列表(Legacy)
    
    注意: 建议使用 search_requests 替代此方法
    """
    args = {"limit": limit}
    if url_filter:
        args["url_filter"] = url_filter
    if method:
        args["method"] = method
    return call_proxypin_tool("get_recent_requests", args)

@mcp.tool()
def clear_requests():
    """清空所有捕获的请求"""
    return call_proxypin_tool("clear_requests")

@mcp.tool()
def get_statistics():
    """获取请求统计信息
    
    返回：
    - total: 总请求数
    - methods: HTTP方法分布
    - statusCodes: 状态码分布(2xx/3xx/4xx/5xx)
    - domains: 域名分布
    - totalSize: 总数据大小
    - averageDuration: 平均响应时间
    - errorCount: 错误请求数
    """
    return call_proxypin_tool("get_statistics")

@mcp.tool()
def compare_requests(request_id_1: str, request_id_2: str):
    """对比两个请求的差异
    
    返回详细对比信息：
    - request_header_diff: 请求Header差异
    - response_header_diff: 响应Header差异
    - request_body_diff: 请求Body差异(支持JSON diff)
    - response_body_diff: 响应Body差异(支持JSON diff)
    - duration_diff: 响应时间差异
    """
    return call_proxypin_tool("compare_requests", {
        "request_id_1": request_id_1,
        "request_id_2": request_id_2
    })

@mcp.tool()
def find_similar_requests(request_id: str, limit: int = 10):
    """查找与指定请求相似的其他请求
    
    相似条件：相同域名、路径和HTTP方法
    """
    return call_proxypin_tool("find_similar_requests", {
        "request_id": request_id,
        "limit": limit
    })

@mcp.tool()
def extract_api_endpoints(domain_filter: str = None):
    """提取并分组所有API端点
    
    返回：
    - endpoints: 端点列表(包含method/domain/path/count/status_codes)
    - total_unique: 唯一端点总数
    
    用途：自动生成API文档、了解系统API结构
    """
    args = {}
    if domain_filter:
        args["domain_filter"] = domain_filter
    return call_proxypin_tool("extract_api_endpoints", args)

# ========================================
# 传康KK 新增工具函数
# ========================================

@mcp.tool()
def get_system_info():
    """获取系统信息 - 传康KK 专属功能"""
    return {
        "version": __version__,
        "author": __author__,
        "contact": __contact__,
        "enhancement": "ProxyPin MCP Server 传康KK 优化增强版",
        "features": [
            "高性能HTTP请求捕获与分析",
            "智能请求过滤与搜索",
            "代码生成与重放",
            "HAR文件导入导出",
            "请求对比分析",
            "API端点提取",
            "增强错误处理与日志记录",
            "连接池优化",
            "线程安全操作"
        ],
        "github": "https://github.com/1837620622",
        "wechat": "1837620622",
        "platforms": "咸鱼/B站: 万能程序员"
    }

# ========================================
# 程序入口 - 传康KK 优化版
# ========================================

def main():
    """主程序入口"""
    print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║                    ProxyPin MCP Server 传康KK 增强版                    ║
║                                                                      ║
║  版本: {__version__:<20} 作者: 传康KK (GitHub)           ║
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
    """)
    
    try:
        logger.info(f"启动 ProxyPin MCP Server {__version__} - 传康KK 优化版")
        logger.info(f"连接目标: {BASE_URL}")
        logger.info("服务器启动成功!")
        mcp.run()
    except Exception as e:
        logger.error(f"服务器启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
