$ErrorActionPreference = 'Stop'

$repoRoot = $PSScriptRoot
Set-Location $repoRoot

$venvDir = Join-Path $repoRoot '.venv'
$venvPython = Join-Path $venvDir 'Scripts\python.exe'

if (-not (Test-Path $venvPython)) {
	Write-Host 'Creating virtual environment in .venv ...'
	python -m venv $venvDir
}

Write-Host 'Installing dependencies from requirements.txt ...'
& $venvPython -m pip install --disable-pip-version-check -r (Join-Path $repoRoot 'requirements.txt')

Write-Host 'Launching python-rpg ...'
& $venvPython (Join-Path $repoRoot 'main.py')
