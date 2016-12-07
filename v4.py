import os,os.path,shutil,fnmatch, pathlib
from pprint import pprint
import re


root = os.getcwd()
directory_files = os.listdir(root)
download = 'download'




#find_seasons= re.findall(r'S(\d+)|Season\s')



#print('root directory ',root)
#print('directory files ', directory_files)
#print(os.listdir("download")) 

def get_files():
	#get all folders and files in downloads 
	All_folder_files = []
	for path, subdirs, files in os.walk(download):
		for name in files:
			All_folder_files.append(name)
       		#pprint (os.path.join(path, name))
	return All_folder_files

pprint(get_files())

def get_tv_shows():
	All_folder_files = get_files()
	#files =	fnmatch.filter(All_folder_files, '*[Ss]\d{2}[Ee]\d{2}*')
	files = [f for f in All_folder_files if re.search(r'([Ss]|Season)\d{2}([Ee]|Episode)\d{2}', f)]
	#pprint(files)
	return files

pprint(get_tv_shows())












