# render.py
# Render the minecraft world using mcmap

import hashlib
import os
import re
import shutil
from datetime import date

def is_png_file(filename):
	return re.search("\\.png$", filename)

def md5_file(filename):
	md5 = hashlib.md5()
	with open(filename, "rb") as f:
		for file_chunk in iter(lambda: f.read(8192), ""):
			md5.update(file_chunk)
	return md5.digest()

# Execute world rendering

cwd = os.getcwd()

try:
	# Find minecraft folder and verify contents

	minecraft_folder = os.environ.get("MINECRAFT_FOLDER")
	if minecraft_folder == "":
		raise Exception("Failed to get Minecraft folder, MINECRAFT_FOLDER environment variable not set")
	print "Found Minecraft folder at", minecraft_folder

	mcmap_path = os.path.join(minecraft_folder, "mcmap.exe")
	if os.access(mcmap_path, os.F_OK) == False:
		raise Exception("Minecraft folder does not contain mcmap.exe")
	print "Found mcmap at", mcmap_path

	render_folder = os.path.join(minecraft_folder, "renders")
	if os.access(render_folder, os.F_OK) == False:
		print "Did not find renders folder at", render_folder, "- creating"
		os.mkdir(render_folder)
		if os.access(render_folder, os.F_OK) == False:
			raise Exception("Renders folder was not created successfully")
	else:
		print "Found renders folder at", render_folder

	world_folder = os.path.join(minecraft_folder, "world")
	if os.access(world_folder, os.F_OK) == False:
		raise Exception("World folder (" + world_folder + ") doesn't exist")
	print "Found world folder at", world_folder

	# Check if we already have a render for today
	# TODO: If we do, don't cancel, add suffix and continue

	today = date.today().strftime('%Y-%m-%d')
	render_file = os.path.join(render_folder, today + ".png")
	if os.access(render_file, os.F_OK):
		raise Exception("Destination render file (" + render_file + ") already exists")

	print "Setting cwd to", render_folder
	os.chdir(render_folder)

	# Render the world

	mcmap_flags = "-west -skylight -blendall"
	mcmap_exec_command = mcmap_path + " " + mcmap_flags + " " + world_folder

	print "Executing '" + mcmap_exec_command + "'"
	print "=" * 60
	os.system(mcmap_exec_command)
	print "=" * 60
	print "Render complete"

	output_file = os.path.join(os.getcwd(), "output.png")
	if os.access(output_file, os.F_OK) == False:
		raise Exception("mcmap output file (" + output_file + ") was not generated")

	# Move output file to appropriate name (mcmap doesn't take output filename as an argument)
	# Correction: mcmap can do this through the -file flag
	# TODO: Use -file

	print "Found mcmap-generated output file at", output_file
	print "Moving", output_file, "to", render_file
	shutil.move(output_file, render_file)

	if os.access(render_file, os.F_OK) == False or os.access(output_file, os.F_OK):
		os.remove(output_file)
		raise Exception("Could not move output file to destination file - deleting source")

	# Hash image to compare with last saved image - if hash matches, remove image

	previous_renders = os.listdir(render_folder)
	previous_renders.sort()
	previous_renders = filter(is_png_file, previous_renders)
	print "Found", (len(previous_renders) - 1), "previously rendered files"

	if len(previous_renders) > 1:
		previous_render_file = os.path.join(render_folder, previous_renders[-2])

		try:
			previous_hash = md5_file(previous_render_file)
			new_hash = md5_file(render_file)

			if previous_hash == new_hash:
				print "Newly rendered file hash matches previous file", previous_render_file
				print "Deleting new, redundant render file"
				os.remove(render_file)
				if os.access(render_file, os.F_OK):
					raise Exception("Could not remove identical render file (" + render_file +") - image will be kept")
			else:
				print "Previously rendered files do not match - image will be kept"

		except IOError:
			raise Exception("Could not hash render files - image will be kept")

except Exception as exc:
	print "Error:", exc

print "Resetting cwd back to the original"
os.chdir(cwd)
