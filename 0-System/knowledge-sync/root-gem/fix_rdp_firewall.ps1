# 移除 RDP 端口的 LocalSubnet 限制，允许所有 IP 访问
Write-Host "Fixing RDP Firewall Rules..."
Get-NetFirewallRule -DisplayGroup "*Remote Desktop*" | Set-NetFirewallRule -RemoteAddress Any
Get-NetFirewallRule -DisplayName "Remote Desktop - User Mode (TCP-In)" | Set-NetFirewallRule -RemoteAddress Any

# 确保 RDP 端口在所有网络配置文件（公共/专用/域）中都开放
Enable-NetFirewallRule -DisplayGroup "*Remote Desktop*"
Write-Host "RDP port 3389 is now fully open to all IPs (including 192.168.2.x Router network)." -ForegroundColor Green
