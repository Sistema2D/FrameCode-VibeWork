# governance/scripts/sync-filesystem.ps1
# PowerShell script to automatically update the ASCII directory tree inside FILESYSTEM.md

$targetFile = "FILESYSTEM.md"
if (-not (Test-Path $targetFile)) {
    Write-Error "FILESYSTEM.md not found!"
    exit 1
}

# Recursive function to generate ASCII directory tree
function Get-DirTree ($path, $indent = "") {
    # Folders to exclude from the visual tree
    $exclude = @(".git", "node_modules", ".gemini")
    
    $items = Get-ChildItem $path | Where-Object { $exclude -notcontains $_.Name } | Sort-Object Name
    $tree = ""
    
    for ($i = 0; $i -lt $items.Count; $i++) {
        $item = $items[$i]
        $isLast = ($i -eq ($items.Count - 1))
        
        $prefix = "|-- "
        if ($isLast) { $prefix = "\-- " }
        
        $tree += "$indent$prefix$($item.Name)`r`n"
        
        if ($item.PSIsContainer) {
            $addition = "|   "
            if ($isLast) { $addition = "    " }
            $nextIndent = $indent + $addition
            $tree += Get-DirTree $item.FullName $nextIndent
        }
    }
    return $tree
}

Write-Host "Scanning workspace directories..." -ForegroundColor Cyan

# Generate tree content
$treeContent = '```text' + "`r`n[project-root]/`r`n" + (Get-DirTree ".") + '```'

# Load current file content
$fileContent = Get-Content $targetFile -Raw

# Regex replace between <!-- START_TREE --> and <!-- END_TREE --> tags
$pattern = '(?s)<!-- START_TREE -->.*?<!-- END_TREE -->'
$replacement = '<!-- START_TREE -->' + "`r`n$treeContent`r`n" + '<!-- END_TREE -->'

if ($fileContent -match $pattern) {
    $newContent = [regex]::Replace($fileContent, $pattern, $replacement)
    Set-Content -Path $targetFile -Value $newContent -NoNewline
    Write-Host "FILESYSTEM.md updated successfully with the actual directory structure!" -ForegroundColor Green
} else {
    Write-Error "Markers <!-- START_TREE --> and <!-- END_TREE --> not found in FILESYSTEM.md!"
    exit 1
}
