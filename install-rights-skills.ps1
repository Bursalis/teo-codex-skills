param(
    [Parameter(Mandatory = $true)]
    [string]$SkillsRoot
)

$packageRoot = $PSScriptRoot
$requiredFolders = @(
    'dikaiomata-kai-anisotites-docx',
    'dikaiomata-kai-anisotites-pptx',
    'rights-and-inequalities-common'
)

if (-not (Test-Path -LiteralPath $SkillsRoot -PathType Container)) {
    throw "Skills root does not exist: $SkillsRoot"
}

foreach ($folder in $requiredFolders) {
    $source = Join-Path $packageRoot $folder
    $destination = Join-Path $SkillsRoot $folder
    if (-not (Test-Path -LiteralPath $source -PathType Container)) {
        throw "Missing package folder: $source"
    }
    if (Test-Path -LiteralPath $destination) {
        throw "Destination already exists: $destination"
    }
}

foreach ($folder in $requiredFolders) {
    Copy-Item -Recurse -LiteralPath (Join-Path $packageRoot $folder) -Destination (Join-Path $SkillsRoot $folder)
}

Write-Output 'Installed the Rights and Inequalities skill package.'
