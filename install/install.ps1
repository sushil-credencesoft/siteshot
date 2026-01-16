$ErrorActionPreference = "Stop"

Write-Host "Installing SiteShot CLI..."

$InstallDir = "$env:USERPROFILE\\SiteShot"
$BinaryUrl  = "https://github.com/sushil-credencesoft/siteshot/releases/download/v1.0.1-stable/siteshot.exe"
$BinaryPath = "$InstallDir\\siteshot.exe"

if (!(Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir | Out-Null
}

Invoke-WebRequest -Uri $BinaryUrl -OutFile $BinaryPath -UseBasicParsing

$CurrentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($CurrentPath -notlike "*SiteShot*") {
    [Environment]::SetEnvironmentVariable(
        "PATH",
        "$CurrentPath;$InstallDir",
        "User"
    )
}

Write-Host "SiteShot installed successfully."
Write-Host "Restart PowerShell and run: siteshot --help"
