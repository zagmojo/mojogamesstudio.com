# Renders the Steam creator page art (group avatar + page background) from
# tools/steam_creator_art.html into img/steam-creator/. Headless Edge, no window.
$ErrorActionPreference = 'Stop'
$site = Split-Path $PSScriptRoot -Parent
$out = Join-Path $site 'img\steam-creator'
New-Item -ItemType Directory -Force $out | Out-Null
$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$port = 8766
$server = Start-Process python -ArgumentList '-I', '-m', 'http.server', $port, '--bind', '127.0.0.1' -WorkingDirectory $site -WindowStyle Hidden -PassThru
try {
  Start-Sleep -Milliseconds 800
  $jobs = @(
    @{ q = 'avatar'; w = 512;  h = 512; file = 'avatar.png' },
    @{ q = 'banner'; w = 1500; h = 220; file = 'background.png' }
  )
  foreach ($j in $jobs) {
    $dest = Join-Path $out $j.file
    $profileDir = Join-Path $env:TEMP "edge-shot-$($j.q)"
    # Start-Process: Edge writes harmless log lines to stderr, which would stop the script.
    Start-Process $edge -Wait -WindowStyle Hidden -ArgumentList @(
      '--headless=new', '--disable-gpu', '--hide-scrollbars', "--user-data-dir=`"$profileDir`"",
      "--window-size=$($j.w),$($j.h)", '--virtual-time-budget=4000',
      "--screenshot=`"$dest`"", "http://127.0.0.1:$port/tools/steam_creator_art.html?$($j.q)")
    Add-Type -AssemblyName System.Drawing
    $img = [System.Drawing.Image]::FromFile($dest); "$($j.file): $($img.Width)x$($img.Height)"; $img.Dispose()
  }
} finally {
  Stop-Process -Id $server.Id -Confirm:$false -ErrorAction SilentlyContinue
}
