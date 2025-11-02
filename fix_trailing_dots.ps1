# PowerShell script to fix files with trailing dots in their names
# This is needed because Windows doesn't support files ending with dots

param(
    [string]$RootPath = ".\temp_repo"
)

Write-Host "Starting to fix files with trailing dots in: $RootPath" -ForegroundColor Green

# Check if path exists
if (-not (Test-Path $RootPath)) {
    Write-Host "Error: Path '$RootPath' does not exist!" -ForegroundColor Red
    exit 1
}

# Find all files with trailing dots
$filesWithTrailingDots = Get-ChildItem -Path $RootPath -Recurse -File -ErrorAction SilentlyContinue | 
    Where-Object { $_.Name -match '\.$' }

if ($filesWithTrailingDots.Count -eq 0) {
    Write-Host "No files with trailing dots found." -ForegroundColor Yellow
    exit 0
}

Write-Host "Found $($filesWithTrailingDots.Count) files with trailing dots" -ForegroundColor Cyan

$successCount = 0
$failCount = 0

foreach ($file in $filesWithTrailingDots) {
    try {
        # Get the new name by removing the trailing dot
        $newName = $file.Name.TrimEnd('.')
        $newPath = Join-Path $file.DirectoryName $newName
        
        Write-Host "Renaming: $($file.Name) -> $newName" -ForegroundColor White
        
        # Check if target file already exists
        if (Test-Path $newPath) {
            Write-Host "  Warning: Target file already exists, skipping..." -ForegroundColor Yellow
            $failCount++
            continue
        }
        
        # Rename the file
        Rename-Item -Path $file.FullName -NewName $newName -Force
        $successCount++
        Write-Host "  ✓ Success" -ForegroundColor Green
        
    } catch {
        Write-Host "  ✗ Failed: $($_.Exception.Message)" -ForegroundColor Red
        $failCount++
    }
}

Write-Host "`nSummary:" -ForegroundColor Cyan
Write-Host "  Successfully renamed: $successCount files" -ForegroundColor Green
Write-Host "  Failed: $failCount files" -ForegroundColor Red
Write-Host "`nDone!" -ForegroundColor Green
