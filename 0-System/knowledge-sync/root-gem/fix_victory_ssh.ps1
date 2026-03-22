# 1. SSH Public Key
$pubKey = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIL/bgvXvA/RnxE7WMG03c6zaIzilN1xB7I/ZZycBmUt8 vicki@Admin.Database'

Write-Host "Starting SSH Permission Fix on Victory..." -ForegroundColor Cyan

# 2. Fix Administrator
try {
    $adminKeyFile = 'C:\ProgramData\ssh\administrators_authorized_keys'
    if (!(Test-Path 'C:\ProgramData\ssh')) { New-Item -Path 'C:\ProgramData\ssh' -ItemType Directory -Force | Out-Null }
    if (!(Test-Path $adminKeyFile)) { New-Item -ItemType File -Path $adminKeyFile -Force | Out-Null }
    
    $content = Get-Content $adminKeyFile
    if ($content -notcontains $pubKey) {
        Add-Content -Path $adminKeyFile -Value $pubKey -Force
    }
    
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
    Write-Host "[!] Admin ACL fix failed (maybe not running as admin): $($_.Exception.Message)" -ForegroundColor Yellow
}

# 3. Fix Standard User
try {
    $userKeyDir = "$env:USERPROFILE\.ssh"
    if (!(Test-Path $userKeyDir)) { New-Item -ItemType Directory -Path $userKeyDir -Force | Out-Null }
    $userKeyFile = "$userKeyDir\authorized_keys"
    if (!(Test-Path $userKeyFile)) { New-Item -ItemType File -Path $userKeyFile -Force | Out-Null }
    
    $content2 = Get-Content $userKeyFile
    if ($content2 -notcontains $pubKey) {
        Add-Content -Path $userKeyFile -Value $pubKey -Force
    }
    
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

Write-Host "Fix completed. You can try SSH without password now." -ForegroundColor Cyan