# A very quick ps script to change the term suffix in the name of each file into
# a different term suffix.

# Ask for term
$term = Read-Host "Enter term to rename"

# Ask for the new term
$newTerm = Read-Host "Enter new term"

# For each file in $term/raw, rename
Get-ChildItem -Path $term/raw -File | ForEach-Object {
    $newName = $_.Name.Replace("_${term}.csv", "_${newTerm}.csv")
    Rename-Item -Path $_.FullName -NewName $newName
}