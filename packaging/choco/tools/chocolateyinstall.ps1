$ErrorActionPreference = 'Stop'

# Chocolatey installation helper for MINT
# Downloads the repository zip, extracts it to the package directory, and registers the mint shim.

$packageName = 'mint-osint'
$url = 'https://github.com/sayfalse/mint/archive/refs/tags/v1.0.10.zip'
$toolsDir = "$(Split-Path -parent $MyInvocation.MyCommand.Definition)"

# NEW: SHA-256 checksum verification
# Computed via: ./scripts/compute-checksums.sh 1.0.10 zip
# IMPORTANT: update this hash at every release.
$expectedChecksum = '6bf9890b5ed4c09ace531b22e85a8a329912f830023942653e073e3c70af8001'

$packageArgs = @{
  packageName   = $packageName
  unzipLocation = $toolsDir
  url           = $url
  checksum      = $expectedChecksum
  checksumType  = 'sha256'
}

Install-ChocolateyZipPackage @packageArgs

# Locate the extracted directory and set the path to the mint.bat shim
$extractedDir = Join-Path $toolsDir 'mint-1.0.10'
$shimPath = Join-Path $extractedDir 'mint.bat'

# Generate the global executable shim so 'mint' runs globally
Generate-BinFile -Name 'mint' -Path $shimPath
