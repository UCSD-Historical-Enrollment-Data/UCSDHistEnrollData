$res = ""
$files = Get-ChildItem -Path "$overall" -Recurse
foreach ($file in $files) {
    if ( $file.Extension -ne ".csv" ) {
        continue
    }
    
    $res += $file.Name.Replace(".csv", "") + "`n"
}

$res | Out-File "all_courses.txt"

# =============================================================== #

$res = ""
$files = Get-ChildItem -Path "section" -Recurse
foreach ($file in $files) {
    if ( $file.Extension -ne ".csv" ) {
        continue
    }
    
    $res += $file.Name.Replace(".csv", "") + "`n"
}

$res | Out-File "all_sections.txt"