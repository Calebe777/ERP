#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
NAME=${1:-ManualMigration}
dotnet ef migrations add "$NAME" --project src/Erp.Infrastructure --startup-project src/Erp.UI --output-dir Migrations
