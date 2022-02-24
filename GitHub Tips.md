# GitHub Tips
just in case y'all want something to refer to for how to do common things in git (in the terminal since there's already one in vsc)

### **Grabbing files**
git pull

### **Creating a branch**
git checkout -b branch-name

### **Opening a branch**
git checkout branch-name

### _**Sending changes to git**_
## FIRST make sure you're on the branch you want to be on
there could be merge conflicts otherwise ://  
### **To add all changes**
git add .

### **To add specific files**
git add file_name.py

### **To make a commit with a comment**
git commit -am "Added git instructions"

### **To send these changes online**
git push

## If you happen to run into a merging issue, you can try and *rebase*

### **Rebase**
I got these instructions from my software engineering class and haven't actually had to use them yet?\
\
git checkout main\
git pull\
git checkout branch-name\
git rebase -i main\
* this will open vim when you do it, its a cmd line text editor
* rewrite history to rebase your commits onto the latest version of main
* pick (p) or rename (r) the first commit that shows up
* pick (p) or fix (f, it squashes) the other commits
* type :wq to exit vim and leave the rebase
  * now resolve your conflicts (look for <<<<< and =====)

git rebase -continue\
git push -f origin\
\
if theres anything else that's common that i'm forgetting let me know! :)