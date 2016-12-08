import os,os.path,shutil,fnmatch, pathlib
from pprint import pprint
import re
import glob
from guessit import *


root = os.getcwd()
directory_files = os.listdir(root)
download = 'downloads'


VideoTypes = ('.wmv', '.mov', '.avi', '.divx', '.mpeg', '.mpg', '.m4p', '.3gp', '.amv', '.qt', '.rm', '.swf', '.mp4', '.mkv')
SoundTypes = ('.mp3')
SubTypes = ('.jss', '.smx', '.sup', '.srt', '.ssa', '.fab', '.sst', '.tfa', '.usf')

				#MatchesDict([('title', 'Would I Lie to You'),
		        #     ('season', 5),
		        #     ('episode', 1),
		        #     ('other', 'WideScreen'),
		        #     ('format', 'DVB'),
		        #     ('release_group', 'SKID'),
		        #     ('container', 'avi'),
		        #     ('mimetype', 'video/x-msvideo'),
		        #     ('type', 'episode')])

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

def make_Tv_folders(show):
	
	Tv = os.getcwd() + '/downloads/TVShows'
	try:
		os.makedirs(Tv)
	except:
		pass
	# make folders for all the movies and shows 
	try:
		os.makedirs(Tv+'/'+show)
	except:
		pass
	
	TvFolder = Tv+'/'+show + '/'
	return TvFolder
	


def get_tv_shows():
	paths = []
	file = []
	episode = {}
	for path, subdirs, files in os.walk(download):
		#pprint(subdirs)
		for name in files:
			paths.append(os.path.join(path, name))
			pp = os.path.join(path, name)
			if name.endswith(VideoTypes):
				g = guessit(name)
				try:
					filename = g['title'].title()
					if g['type'] == 'episode':
						#episodes.append(pp)
						dst = make_Tv_folders(filename)
						try:
							episode.setdefault(filename, set()).add(pp)
							#episode[filename] = pp
							#shutil.move(pp, dst)
						except:
							print('ex ' ,filename)
				except:
					print('name withour title ',name)

	
	return episode

def get_movies():
	paths = []
	file = []
	movie = {}
	movies = []

	for path, subdirs, files in os.walk(download):
		print('subdir ', subdirs)
		for name in files:
			pp = os.path.join(path, name) # the src path 
			#file.append(name)
			#pprint(name)	
			if name.endswith(VideoTypes):
				
				g = guessit(name)
				try:
					filename = g['title'].title()
					
					
					if g['type'] == 'movie':
					#movies.append(name)
						dst = make_Movie_folders(filename)
						#print(pp, dst)

						try:
							movie.setdefault(filename, set()).add(pp)
							#movie[filename] == pp
							#shutil.move(pp, dst)

						except:
							print('ex ',filename)
				except:
					print('name without title ', name)




	return movie

get_movies()
get_tv_shows()









def removeInFolders():
	#make_New_Folders()
	
	movies = get_movies()
	tvShows = get_tv_shows()

	for i in movies.keys():
		l = list(movies[i])
		#print(l)
		for path in l:
			movie = path.split('/')
			if len(movie) == 2:
				src = path
				dst =  os.getcwd() + '/downloads/Movies/'+ i + '/'
				#print(src,dst)
				shutil.move(src,dst)
			if len(movie) > 2:
				folder = movie[1]
				folderCheck = folder.split(' ')[0]
				fileCheck = file.split('.')
				if fileCheck == folderCheck:
					shutil(src , dst)
				

				print(folder , file)





def subfolders():
	folders = []
	files = []
	paths = get_paths()
	l = []
	for i in paths:
		#print(guessit)	
		#print(i)		
		if '.DS_Store' in str(i):
				continue
		a = (i.split('/')[1:])
		s =  re.split(r'([\d])| -', a[0])[0]
		#pprint(guessit(s))
		#print( guessit(i))
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
		
	return l

	



			

#subfolders()	
#mkdir()
#removeInFolders()
