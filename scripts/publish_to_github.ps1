param(
    [Parameter(Mandatory = $true)]
    [string]$RepositoryUrl,

    [string]$Branch = "main",

    [string]$RemoteName = "origin",

    [string]$GitExe = "git"
)

$ErrorActionPreference = "Stop"

function Invoke-CheckedGit {
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Arguments
    )

    & $GitExe @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Git command failed: $GitExe $($Arguments -join ' ')"
    }
}

$repoRoot = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")
Push-Location $repoRoot
try {
    Invoke-CheckedGit status --short
    $status = & $GitExe status --porcelain
    if ($LASTEXITCODE -ne 0) {
        throw "Unable to inspect Git status."
    }

    if ($status) {
        throw "Working tree is not clean. Commit or remove local changes before publishing."
    }

    $existingRemote = & $GitExe remote get-url $RemoteName 2>$null
    if ($LASTEXITCODE -eq 0 -and $existingRemote) {
        Invoke-CheckedGit remote set-url $RemoteName $RepositoryUrl
    } else {
        Invoke-CheckedGit remote add $RemoteName $RepositoryUrl
    }

    Invoke-CheckedGit branch -M $Branch
    Invoke-CheckedGit push -u $RemoteName $Branch
}
finally {
    Pop-Location
}
