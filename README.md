github-backup
=============

Backup/mirror all public github repos of a user

Usage
-----
`python github-backup.py [-h] [-up] [-s] [-m] user dir`   

Positional arguments   
user: github username   
dir: directory the backup will be saved in (exclude username)   


Optional arguments   
-h, --help: help   
-up, --update: update repo list of user, then update repos   
-s, --stared: backup users started repos   
-m, --mirror: Create mirror of user repos   



Developed with Python 3.4.2