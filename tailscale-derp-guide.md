# Tailscale 私有 DERP 加速部署指南

为了彻底解决跨国中继导致的延迟（几百毫秒）和连接不稳定的问题，我们利用具有公网 IP 的 Gate 节点（113.57.105.174）自建了 DERP 中继服务。

## 一、服务器端（Gate 节点）部署状态

目前在 Gate 节点的 `vicki` 用户下，已经通过以下命令在后台常驻了 `derper` 加速引擎：

```bash
nohup ~/derper -c /tmp/derper.conf -hostname 113.57.105.174 -a :12345 -stun :3478 -http-port -1 -verify-clients=false > /tmp/derper.log 2>&1 &
```

**监听端口：**
*   TCP: 12345 (数据中转)
*   UDP: 3478 (STUN 探测打洞)
*(确保云服务器安全组已放行上述端口)*

## 二、Tailscale 后台接入配置（必需步骤）

你必须在 Tailscale 控制台的 Access Control 页面注入以下 ACL 规则，全网节点才能发现并使用这个私有加速器：

1. 登录 [Tailscale ACL 页面](https://login.tailscale.com/admin/acls)。
2. 在 JSON 配置文件的大括号内（通常在最下方），粘贴以下内容：

```json
  "derpMap": {
    "OmitDefaultRegions": false,
    "Regions": {
      "900": {
        "RegionID": 900,
        "RegionCode": "gate-home",
        "RegionName": "Gate Private DERP",
        "Nodes": [
          {
            "Name": "1a",
            "RegionID": 900,
            "HostName": "113.57.105.174",
            "DERPPort": 12345,
            "STUNPort": 3478,
            "InsecureForTests": true
          }
        ]
      }
    }
  }
```

## 三、效果验证

在连接了 Tailscale 的机器上（如 CC 或手机 Termux）执行：

```bash
tailscale netcheck
```
如果你在 `DERP latency` 列表中看到了 `gate-home` 且延迟极低（通常 <30ms），即表示全局极速互联配置成功。
