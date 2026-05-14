param(
  [Parameter(Mandatory = $true)]
  [string]$OutDir,
  [string]$Template = 'finance-narration-standard',
  [switch]$Force
)

$ErrorActionPreference = 'Stop'
$skillRoot = Split-Path -Parent $PSScriptRoot
$templatesRoot = Join-Path $skillRoot 'assets\templates'
$scaffoldDir = Join-Path $templatesRoot 'finance-narration-standard'
$templateDir = Join-Path $templatesRoot $Template

if (-not (Test-Path -Path $templateDir)) {
  throw "Template not found: $templateDir"
}
if (-not (Test-Path -Path $scaffoldDir)) {
  throw "Scaffold template not found: $scaffoldDir"
}

if (Test-Path -Path $OutDir) {
  $existing = Get-ChildItem -Path $OutDir -Force -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($existing -and -not $Force) {
    throw "Output directory is not empty. Rerun with -Force or choose a new directory: $OutDir"
  }
} else {
  New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
}

if ($Template -eq 'finance-narration-standard') {
  Copy-Item -Path (Join-Path $scaffoldDir '*') -Destination $OutDir -Recurse -Force
} else {
  Copy-Item -Path (Join-Path $scaffoldDir '*') -Destination $OutDir -Recurse -Force
  $referenceDir = Join-Path $OutDir 'template-reference'
  New-Item -ItemType Directory -Force -Path $referenceDir | Out-Null
  Copy-Item -Path (Join-Path $templateDir '*') -Destination $referenceDir -Recurse -Force
}

$assetDir = Join-Path $OutDir 'assets'
New-Item -ItemType Directory -Force -Path $assetDir | Out-Null

$notes = @(
  "Selected template: $Template",
  'Replace assets\voiceover.wav with the real narration.',
  'Replace assets\book-cover.png with the real book/product cover when the CTA uses one.',
  'Create cover.png for every template. Both template 1 and template 2 require a cover.',
  'After rendering the narration video, prepend cover.png with scripts\prepend_cover.ps1 so final MP4 starts with a 0.6s cover first frame.',
  'If template-reference exists, use its template.profile.json and contact-sheet.jpg as the visual matching target.',
  'Edit video-spec.template.json into video-spec.json after transcription and timing.',
  'Keep DESIGN.md unless the user intentionally changes the house style.',
  'Run the skill doctor before rendering: scripts\check_capabilities.ps1 -Require recommended'
)

$notes | Set-Content -Path (Join-Path $OutDir 'NEXT_STEPS.txt') -Encoding UTF8

[PSCustomObject]@{
  Template = $Template
  Output = (Resolve-Path -Path $OutDir).Path
  Created = $true
  Next = 'Add voiceover/book-cover, create timed video-spec.json, render with HyperFrames, verify with ffprobe and motion review.'
}
