param(
    [string]$Destination = "..\mall"
)

$ErrorActionPreference = "Stop"
if (-not (Test-Path (Join-Path $Destination ".git"))) {
    git clone https://github.com/macrozheng/mall.git $Destination
}
Write-Host "Mall cloned to $Destination"
Write-Host "Start the Mall backend using its official documentation, then update MALLTEST_ADMIN_URL if needed."
