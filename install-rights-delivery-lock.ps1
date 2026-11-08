param(
    [string]$CodexRoot = (Join-Path $HOME '.codex')
)

$source = Join-Path $PSScriptRoot 'plugins\rights-delivery-lock\hooks\stop_delivery_lock.py'
$hooksDirectory = Join-Path $CodexRoot 'hooks'
$destination = Join-Path $hooksDirectory 'rights-delivery-lock.py'
$configuration = Join-Path $CodexRoot 'hooks.json'

if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
    throw "Missing delivery-lock hook source: $source"
}
if (Test-Path -LiteralPath $configuration -PathType Leaf) {
    throw "Refusing to overwrite an existing hooks configuration: $configuration"
}

New-Item -ItemType Directory -Force -Path $hooksDirectory | Out-Null
Copy-Item -LiteralPath $source -Destination $destination -Force

$escapedDestination = $destination.Replace('\', '\\')
$hooksJson = @"
{
  "description": "User-level Rights and Inequalities DOCX delivery lock.",
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$escapedDestination\"",
            "commandWindows": "py -3 \"$escapedDestination\"",
            "timeout": 3,
            "statusMessage": "Verifying Rights delivery lock"
          }
        ]
      }
    ]
  }
}
"@
[System.IO.File]::WriteAllText($configuration, $hooksJson, [System.Text.UTF8Encoding]::new($false))
Write-Output "Installed user-level delivery hook: $configuration"
