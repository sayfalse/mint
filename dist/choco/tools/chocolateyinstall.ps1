$ErrorActionPreference = 'Stop'

# Chocolatey installation helper for MINT
# Downloads the repository zip, extracts it to the package directory, and registers the mint shim.

$packageName = 'mint-osint'
$url = 'https://github.com/sayfalse/mint/archive/refs/heads/main.zip'
$toolsDir = "$(Split-Path -parent $MyInvocation.MyCommand.Definition)"

$packageArgs = @{
  packageName   = $packageName
  unzipLocation = $toolsDir
  url           = $url
}

Install-ChocolateyZipPackage @packageArgs

# Locate the extracted directory and set the path to the mint.bat shim
$extractedDir = Join-Path $toolsDir 'mint-main'
$shimPath = Join-Path $extractedDir 'mint.bat'

# Generate the global executable shim so 'mint' runs globally
Generate-BinFile -Name 'mint' -Path $shimPath
