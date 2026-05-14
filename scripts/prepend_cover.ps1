param(
  [Parameter(Mandatory = $true)]
  [string]$Cover,
  [Parameter(Mandatory = $true)]
  [string]$Video,
  [Parameter(Mandatory = $true)]
  [string]$Output,
  [double]$CoverSeconds = 0.6,
  [int]$Width = 1080,
  [int]$Height = 1920
)

$ErrorActionPreference = 'Stop'

function Find-FirstExisting {
  param([string[]]$Paths)
  foreach ($path in $Paths) {
    if ($path -and (Test-Path -Path $path)) { return $path }
  }
  return $null
}

function Find-FFmpeg {
  $cwd = (Get-Location).Path
  $homeDirs = @([Environment]::GetFolderPath('UserProfile'))
  if ($cwd -match '^[A-Za-z]:\\Users\\[^\\]+') {
    $workspaceHome = $Matches[0]
    if ($homeDirs -notcontains $workspaceHome) { $homeDirs += $workspaceHome }
  }

  $cmd = Get-Command ffmpeg -ErrorAction SilentlyContinue
  if ($cmd) { return $cmd.Source }

  $paths = @("$cwd\node_modules\ffmpeg-static\ffmpeg.exe")
  foreach ($home in $homeDirs) {
    $paths += @(
      "$home\node_modules\ffmpeg-static\ffmpeg.exe",
      "$home\node_modules\@ffmpeg-installer\win32-x64\ffmpeg.exe"
    )
  }
  return Find-FirstExisting $paths
}

$ffmpeg = Find-FFmpeg
if (-not $ffmpeg) { throw 'FFmpeg not found. Run check_capabilities first.' }
if (-not (Test-Path -Path $Cover)) { throw "Cover not found: $Cover" }
if (-not (Test-Path -Path $Video)) { throw "Video not found: $Video" }

$outputDir = Split-Path -Parent $Output
if ($outputDir) { New-Item -ItemType Directory -Force -Path $outputDir | Out-Null }

$scaleFilter = "scale=${Width}:${Height}:force_original_aspect_ratio=increase,crop=${Width}:${Height},setsar=1,fps=30,format=yuv420p"
$filter = "[0:v]$scaleFilter[v0];[1:v]scale=${Width}:${Height}:force_original_aspect_ratio=increase,crop=${Width}:${Height},setsar=1,fps=30,format=yuv420p[v1];[v0][0:a][v1][1:a]concat=n=2:v=1:a=1[v][a]"

& $ffmpeg -y -hide_banner `
  -loop 1 -t $CoverSeconds -i $Cover `
  -f lavfi -t $CoverSeconds -i anullsrc=channel_layout=stereo:sample_rate=48000 `
  -i $Video `
  -filter_complex $filter `
  -map "[v]" -map "[a]" `
  -c:v libx264 -preset veryfast -crf 23 -pix_fmt yuv420p `
  -c:a aac -b:a 128k -movflags +faststart `
  $Output

if ($LASTEXITCODE -ne 0) { throw "FFmpeg failed while prepending cover." }

[PSCustomObject]@{
  Cover = (Resolve-Path -Path $Cover).Path
  Video = (Resolve-Path -Path $Video).Path
  Output = (Resolve-Path -Path $Output).Path
  CoverSeconds = $CoverSeconds
  Width = $Width
  Height = $Height
}
