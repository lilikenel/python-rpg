$ErrorActionPreference = 'Stop'

$repoRoot = $PSScriptRoot
Set-Location $repoRoot

$outputDir = Join-Path $repoRoot 'out'
$mainClass = 'rpg.Main'

& (Join-Path $repoRoot 'build.ps1')

Write-Host "Launching $mainClass ..."
java -cp $outputDir $mainClass
