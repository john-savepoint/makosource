$tempDir = [System.IO.Path]::GetTempPath()
$output = Join-Path $tempDir 'cmake-installer.msi'

Write-Host "Downloading CMake to $output"
Invoke-WebRequest -Uri 'https://github.com/Kitware/CMake/releases/download/v3.27.8/cmake-3.27.8-windows-x86_64.msi' -OutFile $output -TimeoutSec 300

Write-Host "Installing from $output"
Start-Process -FilePath 'msiexec' -ArgumentList "/i `"$output`" /quiet /norestart" -Wait

Write-Host 'Waiting for CMake to be available...'
Start-Sleep -Seconds 5

# Verify installation
Get-Command cmake -ErrorAction SilentlyContinue | ForEach-Object { Write-Host 'CMake installed at:' $_.Source }
