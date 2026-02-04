#Requires -RunAsAdministrator

Write-Host "[*] MAD Windows setup starting..." -ForegroundColor Cyan

# --------------------------------------------------
# Execution policy
# --------------------------------------------------
Set-ExecutionPolicy Bypass -Scope Process -Force

# --------------------------------------------------
# Chocolatey
# --------------------------------------------------
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "[*] Installing Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
}

# --------------------------------------------------
# Core tools
# --------------------------------------------------
Write-Host "[*] Installing core tools..."
choco install -y git python3 curl wget

# --------------------------------------------------
# VirtualBox
# --------------------------------------------------
Write-Host "[*] Installing VirtualBox..."
choco install -y virtualbox virtualbox-extension-pack

# --------------------------------------------------
# Vagrant
# --------------------------------------------------
Write-Host "[*] Installing Vagrant..."
choco install -y vagrant

# --------------------------------------------------
# Python libraries
# --------------------------------------------------
Write-Host "[*] Installing Python libraries..."
pip install --upgrade pip
pip install pyyaml wcwidth

# --------------------------------------------------
# Enable WinRM (for MAD Windows boxes)
# --------------------------------------------------
Write-Host "[*] Configuring WinRM..."
Enable-PSRemoting -Force
winrm quickconfig -q

# --------------------------------------------------
# Firewall rules
# --------------------------------------------------
Write-Host "[*] Allowing WinRM through firewall..."
New-NetFirewallRule -Name "WinRM-HTTP" -Protocol TCP -LocalPort 5985 -Action Allow -Profile Any -ErrorAction SilentlyContinue

# --------------------------------------------------
# Vagrant plugins
# --------------------------------------------------
Write-Host "[*] Installing Vagrant plugins..."
vagrant plugin install vagrant-reload
vagrant plugin install vagrant-vbguest

# --------------------------------------------------
# Done
# --------------------------------------------------
Write-Host "[✓] Windows setup complete" -ForegroundColor Green
Write-Host "[i] Reboot recommended before starting MAD" -ForegroundColor Yellow
