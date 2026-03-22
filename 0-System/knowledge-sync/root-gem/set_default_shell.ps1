Write-Host "Setting Git Bash as the default OpenSSH shell..." -ForegroundColor Cyan
try {
    $bashPath = "C:\Program Files\Git\bin\bash.exe"
    if (Test-Path $bashPath) {
        New-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShell -Value $bashPath -PropertyType String -Force | Out-Null
        Write-Host "[OK] Default shell is now set to Git Bash." -ForegroundColor Green
    } else {
        Write-Host "[X] Git Bash not found at expected path." -ForegroundColor Red
    }
} catch {
    Write-Host "[!] Failed to set registry. Ensure you have Admin privileges." -ForegroundColor Red
}