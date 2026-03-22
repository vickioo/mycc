$principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
Write-Host "Is Admin Token: $isAdmin"

$integrity = whoami /groups | Select-String "Mandatory Label"
Write-Host "Integrity Level: $integrity"

Write-Host "`n--- Firewall 3389 Rules ---"
Get-NetFirewallRule -DisplayGroup "*Remote Desktop*" -ErrorAction SilentlyContinue | Where-Object {$_.Enabled -eq "True"} | Select-Object Name, Profile, Direction, Action | Format-Table -AutoSize
