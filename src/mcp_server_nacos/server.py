from unittest import case

from . import nacos_tools
from typing import (
    Any,
    Mapping,
    Optional,
    Union
)
import httpx
import logging
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

logger = logging.getLogger('mcp_server_nacos')
logger.info("Starting Nacos MCP Server")

USER_AGENT = 'Nacos-MCP-Server:v0.1.0'

class Result:
    def __init__(self, code: int, message: str, data: Any):
        self.code = code
        self.message = message
        self.data = data

    def is_success(self) -> bool:
        return self.code == httpx.codes.OK

class NacosServer:
    def __init__(self, host: str, port: int, access_token:str):
        self.host = host
        self.port = port
        self.access_token = access_token

    def get(self, name:str, url: str, params: Any = None) -> str:
        url = f'http://{self.host}:{self.port}{url}'
        logger.debug(f'GET {url} with params {params}')
        result = self._request(url, params=params)
        if result is None:
            return "Unexpected error: None result handled."
        if result.is_success():
            return str(result.data)
        return f'Do {name} failed with message: {result.message}'

    def _request(self, url: str, params: Mapping[str, Optional[Union[str, int, float, bool]]] | None = None) -> Result | None:
        """Make a request to the Nacos API with proper error handling."""
        headers = {
            "User-Agent": USER_AGENT,
            "AccessToken": self.access_token
        }
        with httpx.Client() as client:
            try:
                response = client.get(url, headers=headers, timeout=30.0, params=params)
                if response.status_code == httpx.codes.OK:
                    return Result(response.status_code, response.text, response.json())
                if response.status_code in [httpx.codes.UNAUTHORIZED, httpx.codes.FORBIDDEN]:
                    return Result(response.status_code, "UnAuthorized request to Nacos, please make sure the accessToken is validated.", None)
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                return Result(e.response.status_code, str(e), None)
            except Exception as e:
                return Result(httpx.codes.INTERNAL_SERVER_ERROR, str(e), None)

async def main(host: str, port: int, access_token:str):
    logger.info(f"Starting Nacos MCP Server on {host}:{port} with token {access_token}")
    nacos = NacosServer(host, port, access_token)
    server = Server("mcp-nacos")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools"""
        return [
            nacos_tools.NacosListNamespacesTool(),
            nacos_tools.NacosListServices(),
            nacos_tools.NacosGetService(),
            nacos_tools.NacosListInstances(),
            nacos_tools.NacosListServiceSubscribers(),
            nacos_tools.NacosListConfigs(),
            nacos_tools.NacosGetConfig(),
            nacos_tools.NacosListConfigHistory(),
            nacos_tools.NacosGetConfigHistory(),
            nacos_tools.NacosListConfigListeners(),
            nacos_tools.NacosListListenedConfigs(),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[types.TextContent] | None:
        try:
            match name:
                case nacos_tools.NacosToolNames.LIST_NAMESPACES:
                    url = nacos_tools.NacosListNamespacesTool().url
                    result = nacos.get(name, url, arguments)
                    return [types.TextContent(type="text", text=result)]
                case nacos_tools.NacosToolNames.LIST_SERVICES:
                    url = nacos_tools.NacosListServices().url
                    result = nacos.get(name, url, arguments)
                    return [types.TextContent(type="text", text=result)]
                case nacos_tools.NacosToolNames.GET_SERVICE:
                    url = nacos_tools.NacosGetService().url
                    result = nacos.get(name, url, arguments)
                    return [types.TextContent(type="text", text=result)]
                case nacos_tools.NacosToolNames.LIST_INSTANCES:
                    url = nacos_tools.NacosListInstances().url
                    result = nacos.get(name, url, arguments)
                    return [types.TextContent(type="text", text=result)]
                case nacos_tools.NacosToolNames.LIST_SERVICE_SUBSCRIBERS:
                    url = nacos_tools.NacosListServiceSubscribers().url
                    result = nacos.get(name, url, arguments)
                    return [types.TextContent(type="text", text=result)]
                case nacos_tools.NacosToolNames.LIST_CONFIGS:
                    url = nacos_tools.NacosListConfigs().url
                    result = nacos.get(name, url, arguments)
                    return [types.TextContent(type="text", text=result)]
                case nacos_tools.NacosToolNames.GET_CONFIG:
                    url = nacos_tools.NacosGetConfig().url
                    result = nacos.get(name, url, arguments)
                    return [types.TextContent(type="text", text=result)]
                case nacos_tools.NacosToolNames.LIST_CONFIG_HISTORY:
                    url = nacos_tools.NacosListConfigHistory().url
                    result = nacos.get(name, url, arguments)
                    return [types.TextContent(type="text", text=result)]
                case nacos_tools.NacosToolNames.GET_CONFIG_HISTORY:
                    url = nacos_tools.NacosGetConfigHistory().url
                    result = nacos.get(name, url, arguments)
                    return [types.TextContent(type="text", text=result)]
                case nacos_tools.NacosToolNames.LIST_CONFIG_LISTENERS:
                    url = nacos_tools.NacosListConfigListeners().url
                    result = nacos.get(name, url, arguments)
                    return [types.TextContent(type="text", text=result)]
                case nacos_tools.NacosToolNames.LIST_LISTENED_CONFIGS:
                    url = nacos_tools.NacosListListedConfigs().url
                    result = nacos.get(name, url, arguments)
                    return [types.TextContent(type="text", text=result)]
                case _:
                    raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            return [types.TextContent(type="text", text=str(e))]

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="nacos",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
