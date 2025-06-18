git remote prune origin && git repack && git prune-packed && git reflog expire --expire=2.weeks.ago && git gc --aggressive
