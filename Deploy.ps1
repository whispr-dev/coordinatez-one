#Requires -Version 7.2
[CmdletBinding()]
param(
    [Parameter(Mandatory)][ValidatePattern('^[A-Za-z0-9][A-Za-z0-9_.-]*$')][string]$HostAlias,
    [Parameter(Mandatory)][ValidatePattern('^/[A-Za-z0-9_./-]+$')][string]$WebRoot,
    [Parameter(Mandatory)][uri]$Origin
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if ($WebRoot -eq '/' -or $WebRoot -match '(^|/)\.\.(/|$)') { throw 'Use the actual site document root, not / or a parent traversal.' }
if ($Origin.Scheme -ne 'https' -or $Origin.AbsolutePath -ne '/' -or $Origin.Query -or $Origin.Fragment -or $Origin.UserInfo) { throw 'Origin must be a plain HTTPS origin.' }
foreach ($command in @('node','ssh','scp')) { if (-not (Get-Command $command -ErrorAction SilentlyContinue)) { throw "Missing command: $command" } }
Push-Location $PSScriptRoot
try {
    & node scripts/configure-origin.mjs ($Origin.GetLeftPart([System.UriPartial]::Authority))
    if ($LASTEXITCODE -ne 0) { throw 'Metadata configuration failed.' }
    & node scripts/brand-check.mjs
    if ($LASTEXITCODE -ne 0) { throw 'Static file verification failed.' }
    & ssh -- $HostAlias "test -d '$WebRoot' && test -w '$WebRoot'"
    if ($LASTEXITCODE -ne 0) { throw 'The remote web root must already exist and be writable by your SSH user. Check the active server document root.' }
    Write-Host "Uploading to ${HostAlias}:$WebRoot"
    & scp -r -- ./dist/. "${HostAlias}:$WebRoot/"
    if ($LASTEXITCODE -ne 0) { throw 'Upload failed. Existing files are not deleted by this script.' }
    $base = $Origin.GetLeftPart([System.UriPartial]::Authority)
    foreach ($resource in @('sitemap.xml','robots.txt','llms.txt','cookies.txt','README.md')) {
        $response = Invoke-WebRequest -Uri "$base/$resource" -TimeoutSec 25
        if ($response.Content -is [byte[]]) { $body = [Text.Encoding]::UTF8.GetString($response.Content) } else { $body = [string]$response.Content }
        $expected = [IO.File]::ReadAllText((Join-Path $PSScriptRoot "dist/$resource"))
        if ($body.Trim() -cne $expected.Trim()) { throw "Public $resource does not match the uploaded file. Check proxy routes or cache rules for this exact path." }
    }
    Write-Host "Deployed and public text files verified: $base" -ForegroundColor Green
} finally { Pop-Location }
