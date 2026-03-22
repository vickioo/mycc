Write-Host "--- RDP Status ---"
$rdp = (Get-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name 'fDenyTSConnections' -ErrorAction SilentlyContinue).fDenyTSConnections
if ($rdp -eq 0) { Write-Host 'RDP is ENABLED (fDenyTSConnections=0)' } else { Write-Host 'RDP is DISABLED (fDenyTSConnections=1)' }
netstat -ano | Select-String "3389"

Write-Host "`n--- WSL Status ---"
wsl --status
wsl --list --verbose

Write-Host "`n--- Git Bash Path ---"
if (Test-Path "C:\Program Files\Git\bin\bash.exe") { Write-Host "Git Bash found at C:\Program Files\Git\bin\bash.exe" }
