$res = ""
$files = Get-ChildItem -Path "overall" -Recurse
foreach ($file in $files) {
    if ( $file.Extension -ne ".csv" ) {
        continue
    }
    
    $res += $file.Name.Replace(".csv", "") + "`n"
}

$Utf8NoBomEncoding = New-Object System.Text.UTF8Encoding $False
[System.IO.File]::WriteAllLines("all_courses.txt", $res, $Utf8NoBomEncoding)

# =============================================================== #

$res = ""
$files = Get-ChildItem -Path "section" -Recurse
foreach ($file in $files) {
    if ( $file.Extension -ne ".csv" ) {
        continue
    }
    
    $res += $file.Name.Replace(".csv", "") + "`n"
}

[System.IO.File]::WriteAllLines("all_sections.txt", $res, $Utf8NoBomEncoding)
