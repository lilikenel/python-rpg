$ErrorActionPreference = 'Stop'

$repoRoot = $PSScriptRoot
Set-Location $repoRoot

$sourceDir = Join-Path $repoRoot 'src\main\java'
$outputDir = Join-Path $repoRoot 'out'

Write-Host "Compiling sources from $sourceDir into $outputDir ..."
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

$sourceFiles = Get-ChildItem -Path $sourceDir -Filter '*.java' -Recurse | ForEach-Object { $_.FullName }
javac -d $outputDir $sourceFiles

if ($LASTEXITCODE -ne 0) {
	throw "Build failed with exit code $LASTEXITCODE."
}

Write-Host "Build complete. Classes are in $outputDir"
