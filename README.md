github-backup
=============

Backup/mirror all public github repos of a user

Usage
-----
`python github-backup.py user dir [-h] [-up] [-f] [-s] [-m]`   

Positional arguments   
user: github username   
dir: root directory the backup will be saved


Optional arguments   
-h, --help: help   
-up, --update: update repo list of user, then update repos  
-f, --format-dir: creates a custom save path (see below for example)   
-s, --stared: backup users started repos   
-m, --mirror: Create mirror of user repos   


#####Format Dir
Default: `"&user/&repo__&user"`   
`&user`: username of the owner of the repo   
`&repo`: the name of the repo   

   
Developed with Python 3.4.2