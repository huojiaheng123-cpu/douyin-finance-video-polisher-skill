param(
  [switch]$Json,
  [ValidateSet('minimal','recommended','full')]
  [string]$Require
)

function Find-FirstExisting {
  param([string[]]$Paths)
  foreach ($path in $Paths) {
    if ($path -and (Test-Path -Path $path)) { return $path }
  }
  return $null
}

function Find-CommandOrPath {
  param(
    [string[]]$Names,
    [string[]]$Paths
  )
  foreach ($name in $Names) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
  }
  return Find-FirstExisting $Paths
}

function Try-Command {
  param([string]$Command, [string[]]$CommandArgs)
  if (-not $Command) { return @{ Ok = $false; Detail = 'not found' } }
  try {
    $output = & $Command @CommandArgs 2>&1
    $exitCode = $LASTEXITCODE
    $firstLine = $output | Select-Object -First 1
    return @{ Ok = ($exitCode -eq 0); Detail = [string]$firstLine }
  } catch {
    return @{ Ok = $false; Detail = $_.Exception.Message }
  }
}

function Install-Hint {
  param([string]$Name)
  switch ($Name) {
    'FFmpeg' { 'Install FFmpeg or add a bundled ffmpeg-static path to PATH.' }
    'ffprobe' { 'Install ffprobe with FFmpeg or add @ffprobe-installer/ffprobe-static to PATH.' }
    'Node.js' { 'Install Node.js LTS so HyperFrames and browser tooling can run.' }
    'npm' { 'Install Node.js LTS; npm is normally bundled with it.' }
    'npx' { 'Install Node.js LTS; npx is normally bundled with npm.' }
    'HyperFrames CLI' { 'Install/configure HyperFrames CLI, or use npx hyperframes@latest after network approval.' }
    'Browser/media preview' { 'Install Chrome/Edge or use a Codex/browser preview tool; otherwise generate review clips.' }
    default { 'Install or configure this capability before production.' }
  }
}

function Rank {
  param([string]$Level)
  switch ($Level) {
    'minimal' { 0 }
    'recommended' { 1 }
    'full' { 2 }
  }
}

$cwd = (Get-Location).Path
$homeDirs = @([Environment]::GetFolderPath('UserProfile'))
if ($cwd -match '^[A-Za-z]:\\Users\\[^\\]+') {
  $workspaceHome = $Matches[0]
  if ($homeDirs -notcontains $workspaceHome) { $homeDirs += $workspaceHome }
}

$ffmpegPaths = @(
  "$cwd\node_modules\ffmpeg-static\ffmpeg.exe",
  "$cwd\node_modules\@ffmpeg-installer\win32-x64\ffmpeg.exe"
)
$ffprobePaths = @(
  "$cwd\node_modules\@ffprobe-installer\win32-x64\ffprobe.exe",
  "$cwd\node_modules\ffprobe-static\bin\win32\x64\ffprobe.exe"
)
foreach ($homeDir in $homeDirs) {
  $ffmpegPaths += @(
    "$homeDir\node_modules\ffmpeg-static\ffmpeg.exe",
    "$homeDir\node_modules\@ffmpeg-installer\win32-x64\ffmpeg.exe"
  )
  $ffprobePaths += @(
    "$homeDir\node_modules\@ffprobe-installer\win32-x64\ffprobe.exe",
    "$homeDir\node_modules\ffprobe-static\bin\win32\x64\ffprobe.exe"
  )
}

$ffmpegPath = Find-CommandOrPath -Names @('ffmpeg','ffmpeg.exe') -Paths $ffmpegPaths
$ffprobePath = Find-CommandOrPath -Names @('ffprobe','ffprobe.exe') -Paths $ffprobePaths
$nodePath = Find-CommandOrPath -Names @('node','node.exe') -Paths @()
$npmPath = Find-CommandOrPath -Names @('npm.cmd','npm') -Paths @()
$npxPath = Find-CommandOrPath -Names @('npx.cmd','npx') -Paths @()
$hyperframesPath = Find-CommandOrPath -Names @('hyperframes','hyperframes.cmd') -Paths @(
  "$cwd\node_modules\.bin\hyperframes.cmd",
  "$cwd\node_modules\.bin\hyperframes"
)
$browserPaths = @(
  'C:\Program Files\Google\Chrome\Application\chrome.exe',
  'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
  'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
  'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
)
foreach ($homeDir in $homeDirs) {
  $browserPaths += @(
    "$homeDir\AppData\Local\Google\Chrome\Application\chrome.exe",
    "$homeDir\AppData\Local\Microsoft\Edge\Application\msedge.exe"
  )
}
$browserPath = Find-CommandOrPath -Names @('chrome','msedge','google-chrome','chromium','firefox') -Paths $browserPaths

$ffmpeg = Try-Command $ffmpegPath @('-version')
$ffprobe = Try-Command $ffprobePath @('-version')
$node = Try-Command $nodePath @('--version')
$npm = Try-Command $npmPath @('--version')
$npx = Try-Command $npxPath @('--version')
$hyperframes = Try-Command $hyperframesPath @('--version')

$checks = @(
  @{ Name='FFmpeg'; Ok=$ffmpeg.Ok; Purpose='mux audio, extract motion strips, check media streams'; Detail=$ffmpeg.Detail },
  @{ Name='ffprobe'; Ok=$ffprobe.Ok; Purpose='inspect duration and audio/video streams'; Detail=$ffprobe.Detail },
  @{ Name='Node.js'; Ok=$node.Ok; Purpose='run HyperFrames and browser tooling'; Detail=$node.Detail },
  @{ Name='npm'; Ok=$npm.Ok; Purpose='install or execute HyperFrames CLI'; Detail=$npm.Detail },
  @{ Name='npx'; Ok=$npx.Ok; Purpose='run HyperFrames without global install'; Detail=$npx.Detail },
  @{ Name='HyperFrames CLI'; Ok=$hyperframes.Ok; Purpose='render HTML video and inspect layouts'; Detail=$hyperframes.Detail },
  @{ Name='Browser/media preview'; Ok=[bool]$browserPath; Purpose='watch motion and audio-video sync'; Detail=($(if ($browserPath) { $browserPath } else { 'not found' })) }
)

$hasRenderer = [bool]$hyperframes.Ok
$hasMotionReview = [bool]$ffmpeg.Ok
$hasPreview = [bool]$browserPath
if ($hasRenderer -and $hasMotionReview -and $ffprobe.Ok -and $hasPreview) {
  $level = 'full'
} elseif ($hasMotionReview -and $ffprobe.Ok -and $hasRenderer) {
  $level = 'recommended'
} else {
  $level = 'minimal'
}

if (-not $ffmpeg.Ok) {
  $nextStep = 'Install/configure FFmpeg first; it gives the biggest quality gain for muxing and motion review.'
} elseif (-not $ffprobe.Ok) {
  $nextStep = 'Install/configure ffprobe so durations and audio/video streams can be verified.'
} elseif (-not $hyperframes.Ok) {
  $nextStep = 'Configure HyperFrames CLI next so HTML compositions can be rendered and inspected.'
} elseif (-not $hasPreview) {
  $nextStep = 'Add a browser/media preview path or generate short MP4 review clips for the user.'
} else {
  $nextStep = 'Add transcription/word timestamps if precise semantic sync is needed.'
}

if ($level -eq 'full') {
  $impact = 'This machine can render, mux, and dynamically review video.'
} elseif ($level -eq 'recommended') {
  $impact = 'This machine can produce video and motion-review artifacts, but may still need direct playback or transcription for best sync review.'
} else {
  $impact = 'This machine cannot reliably render or dynamically verify final video yet.'
}

$meets = (-not $Require) -or ((Rank $level) -ge (Rank $Require))
$result = [ordered]@{
  capabilityLevel = $level
  meetsRequiredLevel = $meets
  requiredLevel = $Require
  checks = @($checks | ForEach-Object {
    [ordered]@{
      name = $_.Name
      ok = $_.Ok
      purpose = $_.Purpose
      detail = $_.Detail
      fix = $(if ($_.Ok) { $null } else { Install-Hint $_.Name })
    }
  })
  unconfirmed = @([ordered]@{
    name = 'Transcription timestamps'
    purpose = 'precise semantic scene boundaries'
    detail = 'manual check: Whisper/ElevenLabs/audio-transcribe skill may be environment-specific'
  })
  impact = $impact
  suggestedNextStep = $nextStep
}

if ($Json) {
  $result | ConvertTo-Json -Depth 5
} else {
  "Current capability level: $level"
  'Available:'
  $checks | Where-Object { $_.Ok } | ForEach-Object { "- $($_.Name)" }
  'Missing or unconfirmed:'
  $checks | Where-Object { -not $_.Ok } | ForEach-Object { "- $($_.Name): needed for $($_.Purpose). Fix: $(Install-Hint $_.Name)" }
  '- Transcription timestamps: needed for precise semantic scene boundaries. manual check: Whisper/ElevenLabs/audio-transcribe skill may be environment-specific.'
  'Impact:'
  "- $impact"
  'Suggested next step:'
  "- $nextStep"
  if (-not $meets) { "Gate: required level '$Require' was not met." }
}

if (-not $meets) { exit 2 }
exit 0
