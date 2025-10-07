# Script to add Python and Python Scripts directories to the PATH environment variable

# Get the current PATH
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")

# Python executable directory
$pythonPath = "C:\Users\hp\AppData\Local\Programs\Python\Python313"

# Python Scripts directory
$scriptsPath = "C:\Users\hp\AppData\Local\Programs\Python\Python313\Scripts"

# Check if paths already exist in PATH
$pathsToAdd = @()

if ($currentPath -notlike "*$pythonPath*") {
    $pathsToAdd += $pythonPath
}

if ($currentPath -notlike "*$scriptsPath*") {
    $pathsToAdd += $scriptsPath
}

# If there are paths to add, update the PATH
if ($pathsToAdd.Count -gt 0) {
    $newPath = $currentPath
    foreach ($path in $pathsToAdd) {
        if ($newPath) {
            $newPath = "$newPath;$path"
        } else {
            $newPath = $path
        }
    }
    
    # Set the new PATH
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
    Write-Host "Python paths have been added to your PATH environment variable."
    Write-Host "The following paths were added:"
    foreach ($path in $pathsToAdd) {
        Write-Host "- $path"
    }
    Write-Host "Please restart any open command prompts or PowerShell windows for the changes to take effect."
} else {
    Write-Host "Python paths are already in your PATH environment variable."
}

# Show the current PATH for verification
Write-Host "`nCurrent PATH value:"
[Environment]::GetEnvironmentVariable("PATH", "User")