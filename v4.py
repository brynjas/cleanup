import os,os.path,shutil,fnmatch, pathlib
from pprint import pprint
import re
import glob


root = os.getcwd()
directory_files = os.listdir(root)
download = 'download'

#AllPaths = glob.glob("*/*/*")
#pprint(AllPaths)

#for file in globPaths
#def get_subfolders():
#l = []
#for path in AllPaths:

#	l.append(path.split('/')[1:])
#pprint(l)




#find_seasons= re.findall(r'S(\d+)|Season\s')

def get_paths():
	#get all folders and files in downloads 
	paths = []
	for path, subdirs, files in os.walk(download):
		#print( subdirs)
		for name in files:
			#pprint (os.path.join(path, name))
			paths.append(os.path.join(path, name))
	
	return paths #All_folder_files

pprint(get_paths())


def get_files():
	#get all folders and files in downloads 
	All_files = []
	all_folders = []
	for path, subdirs, files in os.walk(download):
		#print( subdirs)
		for name in files:
			All_files.append(name)
       		#pprint (os.path.join(path, name))
	return All_files #All_folder_files
	#return all_folders

#pprint(get_files())

def get_tv_shows():
	All_folder_files = get_files()
	#files =	fnmatch.filter(All_folder_files, '*[Ss]\d{2}[Ee]\d{2}*')
	files = [f for f in All_folder_files if re.search(r'([Ss]|Season)\d{2}([Ee]|Episode)\d{2}', f)]
	#pprint(files)
	return files

#pprint(get_tv_shows())
#pprint(get_files())



