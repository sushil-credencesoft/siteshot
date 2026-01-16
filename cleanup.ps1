Write-Host "Cleaning Python cache and log files..."

# Remove __pycache__ directories
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
ForEach-Object {
    Write-Host "Removing directory:" $_.FullName
    Remove-Item $_.FullName -Recurse -Force
}

# Remove .pyc and .pyo files
Get-ChildItem -Path . -Recurse -Include *.pyc,*.pyo -File -ErrorAction SilentlyContinue |
ForEach-Object {
    Write-Host "Removing file:" $_.FullName
    Remove-Item $_.FullName -Force
}

# Remove .log files
Get-ChildItem -Path . -Recurse -Include *.log -File -ErrorAction SilentlyContinue |
ForEach-Object {
    Write-Host "Removing file:" $_.FullName
    Remove-Item $_.FullName -Force
}

Write-Host "Cleanup completed successfully."
