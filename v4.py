import os,os.path,shutil,fnmatch, pathlib
from pprint import pprint
import re
import glob


root = os.getcwd()
directory_files = os.listdir(root)
download = 'download'


def get_paths():
	#get all folders and files in downloads 
	paths = []
	for path, subdirs, files in os.walk(download):
		#print( subdirs)
		for name in files:
			#pprint (os.path.join(path, name))
			paths.append(os.path.join(path, name))
	return paths #All_folder_files

#pprint(get_paths())


def get_files():
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

def subfolders():
	folders = []
	files = []
	paths = get_paths()
	l = []
	for i in paths:
		if '.DS_Store' in str(i):
				continue
		a = (i.split('/')[1:])
		s =  re.split(r'([\d])| -', a[0])[0]
		if len(a) > 1:
			folders.append(a)
			#print('a[0]: ' ,a[0])		
			if s not in l:
				s =  re.split(r'([\d])| -', a[0])[0]
				#print('s: ',str(s))
				l.append(s)
		else:
			files.append(a)
			#print('a er: ',a)
			if s not in l:
				l.append(s)
	print(l)
	return l

	
def mkdir():
	l = subfolders()
	print(l)
	for folder in l:
		s = 'download/'+ folder
		print(s)
		try:
			os.makedirs(s)
		except:
			print('Gat ekki búið til möppuna ', s)

	#pprint(l)
	

def removeInFolders():
	folders = []
	files = []
	paths = get_paths()
	l = subfolders()
	for i in paths:
		if '.DS_Store' in str(i):
				continue
		a = (i.split('/')[1:])
		s =  re.split(r'([\d])| -', a[0])[0]
		
		if len(a) > 1:
			p = root +'/download/'+s+'/'
			r = root + '/download/'+a[0]
			print('p2 er : ', p)
			print('r2 er : ', r)

			
			try:
				shutil.move(r, p )
			except:
				print('Tokst ekki að flytja skrár')			
			
		else:
			p = root +'/download/'+s+'/'
			r = root + '/download/'+a[0]
			print('p er : ', p)
			print('r er : ', r)
			
			try:
				#pass
				shutil.move(r,p)
			except:
				print('Tokst ekki að flytja skrár')	
			
			
subfolders()	
mkdir()
removeInFolders()




