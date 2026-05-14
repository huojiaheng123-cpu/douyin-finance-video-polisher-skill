param(
  [Parameter(Mandatory=$true)]
  [string]$Input,

  [Parameter(Mandatory=$true)]
  [string]$OutDir,

  [ValidateSet("all", "every-n")]
  [string]$Mode = "all",

  [int]$Every = 2,

  [double]$Start = -1,

  [double]$Duration = -1,

  [string]$Ffmpeg = "ffmpeg"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $Input)) {
  throw "Input video not found: $Input"
}

if ($Mode -eq "every-n" -and $Every -lt 1) {
  throw "-Every must be >= 1"
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$args = @("-y")
if ($Start -ge 0) {
  $args += @("-ss", [string]$Start)
}
if ($Duration -gt 0) {
  $args += @("-t", [string]$Duration)
}
$args += @("-i", $Input)

if ($Mode -eq "all") {
  $vf = "showinfo"
} else {
  $vf = "select='not(mod(n\,$Every))',showinfo"
  $args += @("-vsync", "vfr")
}

$args += @("-vf", $vf, (Join-Path $OutDir "frame_%06d.png"))

& $Ffmpeg @args
if ($LASTEXITCODE -ne 0) {
  throw "ffmpeg failed with exit code $LASTEXITCODE"
}

$count = (Get-ChildItem -LiteralPath $OutDir -Filter "frame_*.png" -File | Measure-Object).Count
Write-Host "Exported $count review frame(s) to $OutDir"
