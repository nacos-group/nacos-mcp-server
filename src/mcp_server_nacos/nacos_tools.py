from enum import Enum

import mcp.types as types


class NacosTool(types.Tool):
    url: str


class NacosListNamespacesTool(NacosTool):
    def __init__(self):
        super().__init__(
            name=NacosToolNames.LIST_NAMESPACES,
            description="Retrieves the list of namespaces in the current Nacos cluster.",
            inputSchema={
                "type": "object",
                "properties": {}
            },
            url="/nacos/v3/admin/core/namespace/list"
        )


class NacosListServices(NacosTool):
    def __init__(self):
        super().__init__(
            name=NacosToolNames.LIST_SERVICES,
            description="This interface retrieves the list of services under a specified namespace. The response format depends on the `withInstances` parameter:`withInstances=true`: Returns service details with instances (`ServiceDetailInfo` objects). `withInstances=false`: Returns service metadata without instances (`ServiceView` objects). **NOTE: ** When `withInstances=true`, The API may cost too much memory and networks, If Only want get instance list with little or one service, Suggest use `withInstances=false` with `List Service Instances`.",
            inputSchema={
                "type": "object",
                "properties": {
                    "pageNo": {"type": "int", "description": "The current page number, default is 1."},
                    "pageSize": {"type": "int", "description": "The size of services in each page, default is 100"},
                    "namespaceId": {"type": "string",
                                    "description": "The namespaceId of services, default is `public` if missing"},
                    "groupNameParam": {"type": "string",
                                       "description": "The groupName pattern of services, default null means all group if missing. if not null, server will search all service match groupName both prefix and subfix, such as: input `test`, groupName `test`, `atest`, `testb`, `atestb` will all matched"},
                    "serviceNameParam": {"type": "string",
                                         "description": "The serviceName pattern of services, default null means all service if missing.  if not null, server will search all service match serviceName both prefix and subfix, such as: input `test`, serviceName `test`, `atest`, `testb`, `atestb` will all matched"},
                    "ignoreEmptyService": {"type": "bool",
                                           "description": "Whether ignore the empty service in result, default is true"},
                    "withInstances": {"type": "bool",
                                      "description": "Whether contain instances under each services in result, recommend and default is false"},
                },
                "required": ["pageNo", "pageSize"],
            },
            url="/nacos/v3/admin/ns/service/list"
        )


class NacosListInstances(NacosTool):
    def __init__(self):
        super().__init__(
            name=NacosToolNames.LIST_INSTANCES,
            description="This interface retrieves the list of instances for a specified service.",
            inputSchema={
                "type": "object",
                "properties": {
                    "namespaceId": {"type": "string",
                                    "description": "The namespaceId of services, default is `public` if missing"},
                    "groupName": {"type": "string",
                                  "description": "The groupName pattern of services, default is `DEFAULT_GROUP` if missing"},
                    "serviceName": {"type": "string",
                                    "description": "The serviceName pattern of services, required."},
                    "clusterName": {"type": "string",
                                    "description": "The cluster name of instances in services, optional and default is null means match all cluster. If need match multiple cluster, use `,` to split like `cluster1,cluster2`"},
                },
                "required": ["serviceName"],
            },
            url="/nacos/v3/admin/ns/instance/list"
        )


class NacosListConfigs(NacosTool):
    def __init__(self):
        super().__init__(
            name=NacosToolNames.LIST_CONFIGS,
            description="This interface retrieves the list of configurations under a specified namespace.",
            inputSchema={
                "type": "object",
                "properties": {
                    "pageNo": {"type": "int", "description": "The current page number, default is 1."},
                    "pageSize": {"type": "int", "description": "The size of services in each page, default is 100"},
                    "namespaceId": {"type": "string",
                                    "description": "The namespaceId of configs, default is `public` if missing"},
                    "groupName": {"type": "string",
                                  "description": "The groupName pattern of configs, default null means all group. if not null, server will search all config match groupName. If `search=blur`, this parameter allow use `*` to do blur search, such as `*test` to do prefix and `test*` to do suffix"},
                    "dataId": {"type": "string",
                               "description": "The dataId pattern of configs, default null means all dataId. if not null, server will search all config match dataId. If `search=blur`, this parameter allow use `*` to do blur search, such as `*test` to do prefix and `test*` to do suffix"},
                    "type": {"type": "string",
                             "description": "The type of configs, default null means all type, if not null, server will search all config match type. Multiple type using `,` to split, such as `text,json`"},
                    "configTags": {"type": "string",
                             "description": "The tags of configs, default null means all tags, if not null, server will search all config match tags. Multiple tags using `,` to split, such as `tag1,tag2`"},
                    "appName": {"type": "string",
                                   "description": "The appName of configs, default null means all appName, if not null, server will search all config match appName."},
                    "search": {
                        "type": "string",
                        "description": "The search way of list configs, default is `blur` means blur search groupName and dataId. Or using `accurate` means accurate match with groupName and dataId."
                    }
                },
                "required": ["pageNo", "pageSize"],
            },
            url="/nacos/v3/admin/cs/config/list"
        )

class NacosGetConfig(NacosTool):
    def __init__(self):
        super().__init__(
            name=NacosToolNames.GET_CONFIG,
            description="This interface retrieves the details of the specified configuration.",
            inputSchema={
                "type": "object",
                "properties": {
                    "namespaceId": {"type": "string",
                                    "description": "The namespaceId of configs, default is `public` if missing"},
                    "groupName": {"type": "string",
                                  "description": "The groupName of config, Required."},
                    "dataId": {"type": "string",
                               "description": "The dataId of config, Required."}
                },
                "required": ["groupName", "dataId"],
            },
            url="/nacos/v3/admin/cs/config"
        )

class NacosToolNames(str, Enum):
    LIST_NAMESPACES = "list_namespaces",
    LIST_SERVICES = "list_services",
    LIST_INSTANCES = "list_service_instances",
    LIST_CONFIGS = "list_configs",
    GET_CONFIG = "get_config",
