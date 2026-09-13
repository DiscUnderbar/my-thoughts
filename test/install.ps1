param(
  [Parameter(Mandatory = $true)] [string] $Compiler
)

$Compiler = (Resolve-Path -LiteralPath $Compiler).Path
if (-not (Test-Path -LiteralPath $Compiler -PathType Leaf)) { throw "Compiler not found: $Compiler" }
$installDir = Join-Path $env:LOCALAPPDATA 'Tennin\bin'
New-Item -ItemType Directory -Force -Path $installDir | Out-Null
$installedCompiler = Join-Path $installDir 'tenn.exe'
Copy-Item -LiteralPath $Compiler -Destination $installedCompiler -Force

New-Item -Path 'HKCU:\Software\Classes\.tenn' -Force | Out-Null
Set-ItemProperty -Path 'HKCU:\Software\Classes\.tenn' -Name '(Default)' -Value 'Tennin.File'
New-Item -Path 'HKCU:\Software\Classes\Tennin.File\shell\open\command' -Force | Out-Null
Set-ItemProperty -Path 'HKCU:\Software\Classes\Tennin.File\shell\open\command' -Name '(Default)' -Value ('"{0}" "%1"' -f $installedCompiler)

$userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
if (($userPath -split ';') -notcontains $installDir) {
  [Environment]::SetEnvironmentVariable('Path', (($userPath.TrimEnd(';') + ';' + $installDir)), 'User')
}
$userPathExt = [Environment]::GetEnvironmentVariable('PATHEXT', 'User')
if ([string]::IsNullOrWhiteSpace($userPathExt)) { $userPathExt = $env:PATHEXT }
if (($userPathExt -split ';') -notcontains '.TENN') { [Environment]::SetEnvironmentVariable('PATHEXT', ($userPathExt.TrimEnd(';') + ';.TENN'), 'User') }
$env:Path += ";$installDir"
if (($env:PATHEXT -split ';') -notcontains '.TENN') { $env:PATHEXT += ';.TENN' }
Write-Host 'Installed. Open a new PowerShell window, then run a packed file: hello.tenn'
