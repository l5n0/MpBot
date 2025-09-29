Write-Host "Installing ffmpeg on Windows..."

# Download Link für ffmpeg (aktuelle statische Version)
$ffmpegUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
$outputPath = "$env:TEMP\ffmpeg.zip"
$installPath = "C:\ffmpeg"

# Datei herunterladen
Invoke-WebRequest -Uri $ffmpegUrl -OutFile $outputPath

# Zip entpacken
Expand-Archive -Path $outputPath -DestinationPath $installPath -Force

# Pfad zum ffmpeg/bin hinzufügen
$folder = Get-ChildItem $installPath | Where-Object { $_.PSIsContainer } | Select-Object -First 1
$ffmpegBin = Join-Path $installPath $folder.Name | Join-Path -ChildPath "bin"

# Systemweite PATH Variable anpassen
$currentPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::Machine)
if (-not $currentPath.Contains($ffmpegBin)) {
    $newPath = "$currentPath;$ffmpegBin"
    [Environment]::SetEnvironmentVariable("Path", $newPath, [EnvironmentVariableTarget]::Machine)
    Write-Host "ffmpeg wurde installiert und zum PATH hinzugefügt. Bitte starte dein System neu."
} else {
    Write-Host "ffmpeg Pfad ist bereits im PATH."
}
