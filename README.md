# mcserver
Minecraft server config scripts
These are the scripts I used to run a private Minecraft server for 2 years (for around 6 people). They're relatively basic (every user is a trusted user, nothing needed for banning/kicking/rep) but designed to make the server easier to run.

## System
OS: Windows 7 Pro
Script language: Python 2.7
Sync: OneDrive for automatic off-box sync of backups and world renders
World render: mcmap (I tried c10t back in the day but it never really did what I wanted it to do)

## Setup
Simply set the environment variable %MINECRAFT_FOLDER% to point to a folder containing your Minecraft server exe, plus mcmap, and these scripts
Import the xml files under /tasks into your system Scheduled Tasks
