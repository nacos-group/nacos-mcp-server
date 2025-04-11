# mcp-server-nacos: A Nacos MCP server

## Overview

[Nacos](https://nacos.io) is an easy-to-use platform designed for dynamic service discovery and configuration and service management. It helps you to build cloud native applications and microservices platform easily.

This MCP(Model Context Protocol) Server is for Nacos interaction and automation. This server provides tools to search and read `namespace`, `service` and `configuration` relative information in Nacos Cluster via Large Language Models.

Please note that `mcp-server-nacos` is currently in early development. The functionality and available tools are subject to change and expansion as we continue to develop and improve the server. And also note that `mcp-server-nacos` only provide read, search and list operation, not support any write operation for current version. Write operation is planning supported in future versions. 

One more note that this `mcp-server-nacos` required Nacos version upper than `3.0.0`, because of depended on the [Nacos Admin API](https://nacos.io/en/swagger/admin/) in 3.x.

### Tools

1. `list_namespaces`
    - Retrieves the list of namespaces in the current Nacos cluster.
    - Input:
      - None
    - Returns: list of namespaces in the current Nacos cluster.
2. `list_services`
    - This tool retrieves the list of services under a specified namespace. The response format depends on the `withInstances` parameter:`withInstances=true`: Returns service details with instances (`ServiceDetailInfo` objects). `withInstances=false`: Returns service metadata without instances (`ServiceView` objects). **NOTE: ** When `withInstances=true`, The API may cost too much memory and networks, If Only want get instance list with little or one service, Suggest use `withInstances=false` with `List Service Instances`.
    - Input:
      - `pageNo`(number): The current page number, default is 1.
      - `pageSize`(number): The size of services in each page, default is 100.
      - `namespaceId`(string, optional): The namespaceId of services, default is `public` if missing.
      - `groupNameParam`(string, optional): The groupName pattern of services, default null means all group if missing.
      - `serviceNameParam`(string, optional): The serviceName pattern of services, default null means all service if missing.
      - `ignoreEmptyService`(bool, optional): Whether ignore the empty service in result, default is true.
      - `withInstances`(bool, optional): Whether contain instances under each services in result, recommend and default is false.
    - Returns: list of services under a specified namespace.
3. `get_service`
   - This tool retrieves detailed information of a specified service, including metadata and clusters, not including instance list.
   - Input:
     - `namespaceId`(string, optional): The namespaceId of services, default is `public` if missing.
     - `groupName`(string, optional): The groupName pattern of services, default is `DEFAULT_GROUP` if missing.
     - `serviceName`(string): The serviceName pattern of services, required.
   - Returns: detailed information of a specified service.
4. `list_service_instances`
   - This tool retrieves the list of instances for a specified service.
   - Input:
     - `namespaceId`(string, optional): The namespaceId of services, default is `public` if missing.
     - `groupName`(string, optional): The groupName pattern of services, default is `DEFAULT_GROUP` if missing.
     - `serviceName`(string): The serviceName pattern of services, required.
     - `clusterName`(string, optional): The cluster name of instances in service, optional and default is null means match all cluster.
   - Returns: list of instances for a specified service.
5. `list_service_subscribers`
   - This tool retrieves the list of subscribers for a specified service.
   - Input:
     - `pageNo`(number): The current page number, default is 1.
     - `pageSize`(number): The size of service subscribers in each page, default is 100.
     - `namespaceId`(string, optional): The namespaceId of services, default is `public` if missing.
     - `groupName`(string, optional): The groupName pattern of services, default is `DEFAULT_GROUP` if missing.
     - `serviceName`(string): The serviceName pattern of services, required.
     - `aggregation`(bool, optional): Whether aggregation from whole cluster.
   - Returns: list of subscribers for a specified service.
6. `list_configs`
   - This tool retrieves the list of configurations under a specified namespace.
   - Input:
     - `pageNo`(number): The current page number, default is 1.
     - `pageSize`(number): The size of configs in each page, default is 100.
     - `namespaceId`(string, optional): The namespaceId of configs, default is `public` if missing.
     - `groupName`(string, optional): The groupName pattern of configs, default null means all group. 
     - `dataId`(string, optional): The dataId pattern of configs, default null means all dataId.
     - `type`(string, optional): The type of configs, default null means all type.
     - `configTags`(string, optional): The tags of configs, default null means all tags.
     - `appName`(string, optional): The appName of configs, default null means all appName.
     - `search`(string, optional): The search way of list configs, default is `blur`, optional value `accurate`.
   - Returns: list of configurations under a specified namespace.
7. `get_config`
   - retrieves the details of the specified configuration.
   - Input:
     - `namespaceId`(string, optional): The namespaceId of configs, default is `public` if missing.
     - `groupName`(string): The groupName of config, Required.
     - `dataId`(string): The dataId of config, Required.
   - Returns: the details of the specified configuration.
8. `list_config_history`
   - This tool retrieves the complete publish history of a configuration.
   - Input:
     - `pageNo`(number): The current page number, default is 1.
     - `pageSize`(number): The size of config history records in each page, default is 100.
     - `namespaceId`(string, optional): The namespaceId of configs, default is `public` if missing.
     - `groupName`(string): The groupName of config, Required.
     - `dataId`(string): The dataId of config, Required.
   - Returns: list of configurations under a specified namespace.
9. `get_config_history`
   - retrieves a specific historical change record of a configuration.
   - Input:
     - `namespaceId`(string, optional): The namespaceId of configs, default is `public` if missing.
     - `groupName`(string): The groupName of config, Required.
     - `dataId`(string): The dataId of config, Required.
     - `nid`(number): the actual id of config history record, Get from list config history tool, `id` field.
   - Returns: historical change record of a configuration.
10. `list_config_listeners`
   - retrieves the list of listeners subscribed to a specific configuration.
   - Input:
     - `namespaceId`(string, optional): The namespaceId of configs, default is `public` if missing.
     - `groupName`(string): The groupName of config, Required.
     - `dataId`(string): The dataId of config, Required.
     - `aggregation`(bool, optional): Whether aggregation from whole cluster.
   - Returns: list of listeners subscribed to a specific configuration.
11. `list_listened_configs`
   - retrieves lists the configurations subscribed to by a specific client IP address.
   - Input:
     - `namespaceId`(string, optional): The namespaceId of configs, default is `public` if missing.
     - `ip`(string): The client ip of config listeners, Required.
     - `aggregation`(bool, optional): Whether aggregation from whole cluster.
   - Returns: lists the configurations subscribed to by a specific client IP address.

## Installation

TODO

## Configuration

TODO

## Development

If you are doing local development, simply follow the steps:

1. Clone this repo into your local environment.
2. Modify codes in `src/mcp_server_nacos` to implement your wanted features.
3. Test using the Claude desktop app. Add the following to your claude_desktop_config.json:

```json
{
"mcpServers": {
  "mcp-server-nacos": {
    "command": "uv",
    "args": [ 
      "--directory",
      "/<path to mcp-server-nacos>/src/mcp_server_nacos",
      "run",
      "mcp-server-nacos"
    ]
  }
}
```

## License

mcp-server-nacos is licensed under the Apache 2.0 License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the Apache 2.0 License. For more details, please see the `LICENSE` file in the project repository.
