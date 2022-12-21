# check if at least one arg is passed
if ( $args.Count -eq 0 ) {
    Write-Host "No arguments passed. Exiting..."
    exit
}

$folder = $args[0]
# Make sure the folder exists
if ( !(Test-Path $folder) ) {
    Write-Host "Term folder $folder does not exist. Exiting..."
    exit
}

$res = ""
$files = Get-ChildItem -Path "$folder/overall" -Recurse
foreach ($file in $files) {
    if ( $file.Extension -ne ".csv" ) {
        continue
    }
    
    $res += $file.Name.Replace(".csv", "") + "`n"
}

$res | Out-File "$folder/all_courses.txt"

# =============================================================== #

$res = ""
$files = Get-ChildItem -Path "$folder/section" -Recurse
foreach ($file in $files) {
    if ( $file.Extension -ne ".csv" ) {
        continue
    }
    
    $res += $file.Name.Replace(".csv", "") + "`n"
}

$res | Out-File "$folder/all_sections.txt"