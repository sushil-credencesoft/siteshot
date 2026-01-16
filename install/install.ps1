$ErrorActionPreference = "Stop"

Write-Host "Installing SiteShot CLI..."

$InstallDir = "$env:USERPROFILE\\SiteShot"
$BinaryUrl = "https://raw.githubusercontent.com/sushil-credencesoft/siteshot/main/dist/siteshot.exe"
$BinaryPath = "$InstallDir\\siteshot.exe"

if (!(Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir | Out-Null
}

Invoke-WebRequest -Uri $BinaryUrl -OutFile $BinaryPath

$CurrentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($CurrentPath -notlike "*SiteShot*") {
    [Environment]::SetEnvironmentVariable(
        "PATH",
        "$CurrentPath;$InstallDir",
        "User"
    )
}

Write-Host "SiteShot installed successfully."
Write-Host "Restart terminal and run: siteshot --help"
