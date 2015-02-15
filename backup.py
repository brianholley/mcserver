# backup.py
# SMP World Backup Script

import hashlib
import os
import re
import shutil
from datetime import date

try:
	# Find minecraft folder and verify contents

	minecraft_folder = os.environ.get("MINECRAFT_FOLDER")
	if minecraft_folder == "":
		raise Exception("Failed to get Minecraft folder, MINECRAFT_FOLDER environment variable not set")
	print "Found Minecraft folder at", minecraft_folder

	backup_folder = os.path.join(minecraft_folder, "backups")
	if os.access(backup_folder, os.F_OK) == False:
		print "Did not find backups folder at", backup_folder, "- creating"
		os.mkdir(backup_folder)
		if os.access(backup_folder, os.F_OK) == False:
			raise Exception("Backups folder was not created successfully")
	else:
		print "Found backups folder at", backup_folder

	world_folder = os.path.join(minecraft_folder, "world")
	if os.access(world_folder, os.F_OK) == False:
		raise Exception("World folder (" + world_folder + ") doesn't exist")
	print "Found world folder at", world_folder

	# Check if we already have a backup for today

	today = date.today().strftime('%Y-%m-%d')
	backup_file = os.path.join(backup_folder, "world-" + today)
	if os.access(backup_file, os.F_OK):
		raise Exception("Found an existing backup for today:" + backup_file)

	try:
		# Copy the world folder

		shutil.copytree(world_folder, backup_file)

	except Exception as exc:

		# We hit an error, remove what we copied in the backup folder (ignore errors)

		if os.access(backup_file, os.F_OK):
			shutil.rmtree(backup_file, true)
		raise Exception("Backup world copy failed: " + exc)

	print "Backup successful"

except Exception as exc:
	print "Error:", exc
