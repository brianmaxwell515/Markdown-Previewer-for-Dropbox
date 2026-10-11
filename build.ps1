# Packages the extension into dist/<name>-<version>.zip for the Chrome Web Store.
# Usage (from the repo root):  powershell -ExecutionPolicy Bypass -File .\build.ps1

$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot

# Only the files the extension needs at runtime.
$files = @(
    'manifest.json',
    'content.js',
    'preview.css',
    'icons/icon16.png',
    'icons/icon48.png',
    'icons/icon128.png'
) + (Get-ChildItem -LiteralPath 'lib' -File | Sort-Object Name | ForEach-Object { "lib/$($_.Name)" })

$missing = $files | Where-Object { -not (Test-Path -LiteralPath $_) }
if ($missing) { throw "Missing files: $($missing -join ', ')" }

# Every file referenced by manifest.json must be packaged.
$manifest = Get-Content -LiteralPath 'manifest.json' -Raw -Encoding UTF8 | ConvertFrom-Json
$referenced = @($manifest.icons.PSObject.Properties.Value) + @($manifest.content_scripts | ForEach-Object { $_.js })
$unpackaged = $referenced | Where-Object { $files -notcontains $_ }
if ($unpackaged) { throw "Referenced in manifest.json but not packaged: $($unpackaged -join ', ')" }

$version = $manifest.version
$out = Join-Path $PSScriptRoot "dist\markdown-previewer-for-dropbox-$version.zip"
New-Item -ItemType Directory -Force -Path (Split-Path $out) | Out-Null
if (Test-Path -LiteralPath $out) { Remove-Item -LiteralPath $out }

# Build the zip with forward-slash entry names; Compress-Archive in Windows
# PowerShell 5.1 writes backslashes, which the Chrome Web Store rejects.
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::Open($out, 'Create')
try {
    foreach ($f in $files) {
        $full = Join-Path $PSScriptRoot $f
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $full, $f, 'Optimal') | Out-Null
    }
} finally {
    $zip.Dispose()
}

$size = [math]::Round((Get-Item -LiteralPath $out).Length / 1KB, 1)
Write-Host "Built $out ($($files.Count) files, $size KB)"
$files | ForEach-Object { Write-Host "  $_" }
