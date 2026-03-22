# Windows OpenSSH 免密登录故障排查与修复指南

## 常见问题与原因

在从 Linux/macOS 跨平台尝试使用 SSH 公钥免密登录 Windows 主机时，最常遇到以下问题，即使公钥已经正确添加到 `authorized_keys` 依然会提示输入密码：

1. **变态的目录权限 (ACL) 机制**
   - Windows 的 OpenSSH 守护进程对授权文件的权限要求极高。
   - **对于管理员组 (Administrators)**，必须使用 `C:\ProgramData\ssh\administrators_authorized_keys`。该文件的权限（ACL）必须且只能包含 `SYSTEM` 和 `Administrators` 组的完全控制权。如果继承了 `Authenticated Users` 等其他组的权限，文件会被判定为不安全，从而被 SSHD 拒绝。
   - **对于普通用户**，使用的是 `~/.ssh/authorized_keys`。同理，权限必须仅限 `SYSTEM` 和 `该用户自身`。

2. **跨平台脚本执行的编码陷阱**
   - 当从 Linux (通常为 UTF-8) 传输 PowerShell 脚本到 Windows 执行时，由于 Windows PowerShell 默认可能采用 GBK 等本地编码，脚本中的中文字符会导致解析错位（例如“吃掉”双引号），引发 `MissingExpressionAfterOperator` (缺少表达式) 等语法错误。
   - **解决办法**：跨平台运维脚本应尽量使用纯英文字符 (ASCII)，或确保在跨平台执行时显式声明正确的 UTF-8 编码。

3. **SSH 客户端未指定正确的私钥**
   - 当使用非默认名称的私钥（如 `id_ed25519_vi`）时，SSH 客户端不会主动发送它。
   - **解决办法**：使用 `-i` 参数指定，或在 `~/.ssh/config` 中绑定 `IdentityFile`。

---

## 终极一键修复脚本 (纯英文防乱码版)

将以下代码保存为 `fix_ssh.ps1`，推送到 Windows 机器上使用管理员权限运行：

```powershell
# 1. SSH Public Key (Replace with your actual public key)
$pubKey = 'ssh-ed25519 AAAAC3NzaC... your_pub_key_here user@host'

Write-Host "Starting SSH Permission Fix on Windows..." -ForegroundColor Cyan

# 2. Fix Administrator
try {
    $adminKeyFile = 'C:\ProgramData\ssh\administrators_authorized_keys'
    if (!(Test-Path 'C:\ProgramData\ssh')) { New-Item -Path 'C:\ProgramData\ssh' -ItemType Directory -Force | Out-Null }
    if (!(Test-Path $adminKeyFile)) { New-Item -ItemType File -Path $adminKeyFile -Force | Out-Null }
    
    $content = Get-Content $adminKeyFile
    if ($content -notcontains $pubKey) { Add-Content -Path $adminKeyFile -Value $pubKey -Force }
    
    $acl = Get-Acl $adminKeyFile
    $acl.SetAccessRuleProtection($true, $false)
    $acl.Access | ForEach-Object { $acl.RemoveAccessRule($_) } | Out-Null
    $rule1 = New-Object System.Security.AccessControl.FileSystemAccessRule('SYSTEM', 'FullControl', 'Allow')
    $rule2 = New-Object System.Security.AccessControl.FileSystemAccessRule('Administrators', 'FullControl', 'Allow')
    $acl.SetAccessRule($rule1)
    $acl.SetAccessRule($rule2)
    Set-Acl -Path $adminKeyFile -AclObject $acl
    Write-Host "[OK] Admin authorized_keys ACL fixed." -ForegroundColor Green
} catch {
    Write-Host "[!] Admin ACL fix failed: $($_.Exception.Message)" -ForegroundColor Yellow
}

# 3. Fix Standard User
try {
    $userKeyDir = "$env:USERPROFILE\.ssh"
    if (!(Test-Path $userKeyDir)) { New-Item -ItemType Directory -Path $userKeyDir -Force | Out-Null }
    $userKeyFile = "$userKeyDir\authorized_keys"
    if (!(Test-Path $userKeyFile)) { New-Item -ItemType File -Path $userKeyFile -Force | Out-Null }
    
    $content2 = Get-Content $userKeyFile
    if ($content2 -notcontains $pubKey) { Add-Content -Path $userKeyFile -Value $pubKey -Force }
    
    $acl2 = Get-Acl $userKeyFile
    $acl2.SetAccessRuleProtection($true, $false)
    $acl2.Access | ForEach-Object { $acl2.RemoveAccessRule($_) } | Out-Null
    $rule1 = New-Object System.Security.AccessControl.FileSystemAccessRule('SYSTEM', 'FullControl', 'Allow')
    $rule2 = New-Object System.Security.AccessControl.FileSystemAccessRule($env:USERNAME, 'FullControl', 'Allow')
    $acl2.SetAccessRule($rule1)
    $acl2.SetAccessRule($rule2)
    Set-Acl -Path $userKeyFile -AclObject $acl2
    Write-Host "[OK] User authorized_keys ACL fixed." -ForegroundColor Green
} catch {
    Write-Host "[X] User ACL fix failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "Fix completed. Restarting sshd service..." -ForegroundColor Cyan
Restart-Service sshd
```

## 客户端最佳实践配置 (~/.ssh/config)

为了实现无缝跳转连接内网的 Windows 机器，可以利用 `ProxyJump` 特性。

```ssh-config
Host target-win
    HostName 192.168.x.x
    User windows_user
    ProxyJump jump-server-alias
    IdentityFile ~/.ssh/id_ed25519_custom
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    LogLevel ERROR
```
这样只需执行 `ssh target-win`，即可全自动经跳板机免密穿透至内网 Windows 主机。
