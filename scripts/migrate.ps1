param(
  [string]$Name = 'ManualMigration'
)
$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')
dotnet ef migrations add $Name --project src/Erp.Infrastructure --startup-project src/Erp.UI --output-dir Migrations
