$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')
dotnet ef database update --project src/Erp.Infrastructure --startup-project src/Erp.UI
