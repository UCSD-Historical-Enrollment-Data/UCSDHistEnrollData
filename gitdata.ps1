# A helper script to commit all datasets to git.
./separate_grad_courses.exe _holding WI23 WI23G
git add .
git commit -m (Get-Date -UFormat "%B %d, %Y - update (datasets)")
git push