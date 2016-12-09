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
knownTvShows = ('Dexter', 'The big bang Theory','Top Chef', 'Top Gear', 'Weed','Would i lie to you', 'True Detective','Modern Family', 'Næturvaktin','New girl', 'mad men', '30 rock', 'masterchef','just a minute', 'house of cards','house','hell kitchen', 'game of thrones','Dragon den','desperate','daredevil', 'advantures time', '8 out of 10 cats')
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
def make_movie_folders(path,Themovie):

	Movies = os.getcwd() + '/downloads/Movies'
	
	#print('path name', path, show)
	movie = guessit(Themovie)
	title = movie['title']

	pathtitle =  Movies +'/' + title
	path = os.getcwd() + '/downloads/' + path

	try:
		os.makedirs(Movies)
		#print ('make : ', Movies)
	except:
		#print ('Didnt make : ', Movies)
		pass

	try:
		os.makedirs(pathtitle)
		print ('make : ', pathtitle)
	except:
		pass
		#print ('Didnt make : ', pathtitle)
	# now remove the file to new folder 
	try:
		#print('trying to move', path , pathtitle+ '/')
		shutil.move(path, pathtitle+'/')
		print ('Remove : ', path , pathsesion)

	except:
		print ('Didnt Remove : ', path , pathsesion)
	
	return None
	

def make_Tv_folders(path,show):

	Tv = os.getcwd() + '/downloads/TVShows'
	
	#print('path name', path, show)
	tvshow = guessit(show)
	title = tvshow['title']
	sesion =  tvshow['season']
	
	pathtitle =  Tv +'/' + title
	folder = pathtitle + '/sesion ' 
	pathsesion = str(sesion)
	pathsesion = folder + pathsesion
	print(pathsesion)

	try:
		os.makedirs(Tv)
		print ('make : ', Tv)
	except:
		print ('Didnt make : ', Tv)

	try:
		os.makedirs(pathtitle)
		print ('make : ', pathtitle)
	except:
		print ('Didnt make : ', pathtitle)
	try:
		os.makedirs(pathsesion)
	except:
		print ('Didnt make : ', pathsesion)
	# now remove the file to new folder 
	try:
		shutil.move(path,(pathsesion+'/'))

	except:
		print ('Didnt Remove : ', path , pathsesion)
	
	return None
	

def get_tv_shows():
	unsorted = {}	
	episode = {}
	for path, subdirs, files in os.walk(download):
		for name in files:
			#paths.append(os.path.join(path, name))
			thepath = os.path.join(path, name)

			
			if name.endswith(VideoTypes):
				g = guessit(name)
				try:
					filename = g['title']
					#print('filename ', filename)

					if re.search(r"((^[Ss][0-9]+([Ee][0-9]+))|(Season|seria|Season)[' ']*[0-9]+)|(^[0-9]{2,10}^[' '])|((ser)\D{2}[' ']*[0-9])" , filename ,re.IGNORECASE) or g['type'] == 'episode':
						unsorted.setdefault(filename, set()).add(pp)
						#print('filename ', filename)
						continue

					if g['type'] == 'episode':
						
						dst = make_Tv_folders(thepath,name)
						
						try:
							episode.setdefault(filename, set()).add(pp)
						except:
							pass
				except:
					pass
					#print('name withour title ',thepath,name)	
	

	return unsorted









def get_movies():
	unsorted = {}
	movie = {}
	for path, subdirs, files in os.walk(download):
		for name in files:
			thepath = os.path.join(path, name) # the src path 	
			if name.endswith(VideoTypes) or name.endswith(SubTypes):
				g = guessit(name)
				try:
					filename = g['title'].title()
					if re.search(r"((^[Ss][0-9]+([Ee][0-9]+))|(Season|seria|Season)[' ']*[0-9]+)|(^[0-9]{3,20})|((ser)\D{2}[' ']*[0-9])" , filename ,re.IGNORECASE):
						unsorted.setdefault(filename, set()).add(thepath)
						#print('filename ', filename)
						continue
					if g['type'] == 'movie':
						pprint(thepath)
						dst = make_movie_folders(name,thepath)
						try:
							movie.setdefault(filename, set()).add(thepath)
						except:
							pass
							#print('ex ',filename)
				except:
					pass
					#print('name without title ', name)

	return movie



			







#print(guessit('Breaking.Bad.S04E01.HDTV.XviD-FQM.Box.Cutter.srt'))	


#get_tv_shows()
get_movies()
#removeInFolders()



			

#subfolders()	
#mkdir()
#removeInFolders()
