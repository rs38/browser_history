# Build JupyterLite site and serve it locally for testing
Set-Location $PSScriptRoot

# Activate venv
& "$PSScriptRoot\.venv\Scripts\Activate.ps1"

# Rebuild
Write-Host "Building JupyterLite site..." -ForegroundColor Cyan
jupyter lite build --output-dir docs
if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Serving at http://localhost:8000/lab" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop." -ForegroundColor Yellow
Write-Host ""

python -m http.server 8000 --directory docs
