import os,os.path,shutil,fnmatch, pathlib
from pprint import pprint
import re
import glob
from guessit import *


root = os.getcwd()
directory_files = os.listdir(root)
download = 'downloads'
rootDownloads = root + '/' + 'downloads/'


VideoTypes = ('.wmv', '.mov', '.avi', '.divx', '.mpeg', '.mpg', '.m4p', '.3gp', '.amv', '.qt', '.rm', '.swf', '.mp4', '.mkv')
SoundTypes = ('.mp3')
SubTypes = ('.jss', '.smx', '.sup', '.srt', '.ssa', '.fab', '.sst', '.tfa', '.usf')
Deletewords = ('hdtv','xvid','-','ftp', 'x264','xvid-ftp', 'ASAP','FQM','lol','P0W4','AFG','PDTV','HDTV')

				#MatchesDict([('title', 'Would I Lie to You'),
		        #     ('season', 5),
		        #     ('episode', 1),
		        #     ('other', 'WideScreen'),
		        #     ('format', 'DVB'),
		        #     ('release_group', 'SKID'),
		        #     ('container', 'avi'),
		        #     ('mimetype', 'video/x-msvideo'),
		        #     ('type', 'episode')])
def clean():
	for path, subdirs, files in os.walk(rootDownloads):
		#print(path, subdirs)
		for name in files:
			#compiled_re = re.compile(Deletewords)
			res = re.compile(r"((hdtv|xvid|'-'|ftp|x264|asap|LOL|FQM|p0w4|afg|pdtv|AFG|XviD-FQM|XviD-LOL|cbm*).)", re.IGNORECASE)		
			new_name = res.sub('', name,re.IGNORECASE)
			newName = (path.split('/'))
			newName = '/'.join(newName) + '/' + new_name
			pp = os.path.join(path, name)
			try:
				os.rename(pp, newName)
			except:
				pass


clean()	

def check_if_folder_exist_for_show(dst,foldername):
	dirs = [d for d in os.listdir(dst) if os.path.isdir(os.path.join(dst, d))]
	if foldername in dirs:
		return True
	return False


def move_shows(thepath, path , name):
	dst = os.getcwd() + '/downloads/Tvshows'
	try:
		os.makedirs(dst)
	except:
		pass

	subfolder = thepath.split('/')
	title = subfolder[1]
	folder2Remove = ''

	if len(subfolder) == 4:
		pass
		#folder2Remove = subfolder[2]
	if len(subfolder) == 3:
		pass
		#folder2Remove = subfolder + '/'

	folderTitle = re.split('([Ss]\s*[0-9]+\s*[Ee]\s*[0-9]+)|(season|Seria|Seasons|Season|uk|USA)', title ,re.IGNORECASE)
	folderTitle = (re.sub(r'[^\w]', ' ', folderTitle[0])).title()
	#print('foldername ', folderTitle)
	

	if name.endswith(VideoTypes):  # tharf ad laga thegar thad er rar skra
		try:
			os.makedirs(dst +'/' + folderTitle)
		except:
			pass

		
		if check_if_folder_exist_for_show(dst,folderTitle):
			dst = dst + '/' + folderTitle + '/'
				
			try:
				#print('shutil.move ' ,path, dst )
				shutil.move(path,dst)
			except: 
				print('exist EX ', path,dst)

		else:
			dst = dst + '/' + folderTitle + '/'

			try:
					#pass
					#print('else makedir ', dst +'/' + foldername)
				#print('else shutil.move ' ,path,dst)
				shutil.move(path,dst)
			except: 
				print('exist not ', path,dst)



def check_season_folders(thepath, path, name):
	if re.search(r"(([Ss][0-9]+([Ee][0-9]+)?)|(Season|seria|Season)[' ']*[0-9]+)|([/][0-9]+)|((ser)\D{2}[' ']*[0-9])" , path ,re.IGNORECASE):
		e = thepath + '/' + name
		if re.search(r'([/][0-9][/]([0-9]+)|(.[0-9+][x.]*[0-9]+)|((ser)\D{2}[' ']*[0-9]))', e, re.IGNORECASE):
			move_shows(thepath, path, name)
			return True
		if re.search(r"(([Ss][0-9]+([Ee][0-9]+)?)|(Season)[' ']*[0-9]+)" , path ,re.IGNORECASE):
			move_shows(thepath,path , name)
			return True
	return False


def get_tv_shows():

	episode = {}
	for path, subdirs, files in os.walk(download):
		for name in files:
			#paths.append(os.path.join(path, name))
			thepath = os.path.join(path, name)
			if check_season_folders(thepath, path, name):
				continue # færi alla möppuna í check_season...

			if name.endswith(VideoTypes):
				g = guessit(name)
				try:
					filename = g['title']

					if g['type'] == 'episode':
						#dst = make_Tv_folders(filename)
						try:
							episode.setdefault(filename, set()).add(pp)
							#episode[filename] = pp
							print('Get tv shows shutil ', pp, dst)
							#shutil.move(pp, dst)
						except:
							pass
							#print('ex ' ,filename)
				except:
					print('name withour title ',pp,name)	
	return episode









def get_movies():

	movie = {}
	for path, subdirs, files in os.walk(download):
		#print('subdir ', subdirs)
		for name in files:
			pp = os.path.join(path, name) # the src path 	
			if name.endswith(VideoTypes):
				if check_season_folders(pp,path ,name) == True:
					continue

				g = guessit(name)
				try:
					filename = g['title'].title()

					if g['type'] == 'movie':
						dst = make_Movie_folders(filename)
						try:
							movie.setdefault(filename, set()).add(pp)
							shutil.move(pp, dst)

						except:
							print('ex ',filename)
				except:
					print('name without title ', name)

	return movie

def make_Movie_folders(movie):
	Bio = os.getcwd() + '/downloads/Movies'
	try:
		os.makedirs(Bio)
	except:
		pass
	# make folders for all the movies and shows 
	try:
		os.makedirs(Bio+'/'+movie)
	except:
		pass
	MovieFolder = Bio+'/'+movie + '/'
	
	return MovieFolder


def removeInFolders():
	#make_New_Folders()
	
	movies = get_movies()

	for i in movies.keys():
		l = list(movies[i])
		#print(l)
		for path in l:
			movie = path.split('/')
			if len(movie) == 2:
				src = path
				dst =  os.getcwd() + '/downloads/Movies/'+ i + '/'
				#print(src,dst)
				try:
					shutil.move(src,dst)
				except:
					print('cant move', src, dst )

			if len(movie) > 2:
				folder = movie[1]
				folderCheck = folder.split(' ')[0]
				fileCheck = folderCheck.split('.')
				if fileCheck == folderCheck:
					try:
						shutil(src , dst)
					except:
						print('cant move', src, dst )
				







	


get_tv_shows()
removeInFolders()



			

#subfolders()	
#mkdir()
#removeInFolders()
