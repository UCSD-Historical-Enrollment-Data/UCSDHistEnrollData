# A helper script to commit all datasets to git.
git add .
git commit -m (Get-Date -UFormat "%B %d, %Y - update (datasets)")
git push