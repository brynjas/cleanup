import os,os.path,shutil,fnmatch, pathlib
from pprint import pprint
import re
import glob
from guessit import *


root = os.getcwd()
directory_files = os.listdir(root)
download = 'download'


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

def get_tv_shows():
	paths = []
	file = []
	episode = {}
	for path, subdirs, files in os.walk(download):
		for name in files:
			paths.append(os.path.join(path, name))
			pp = os.path.join(path, name)
			if name.endswith(VideoTypes):
				g = guessit(name)
				filename = g['title'].upper()
				if g['type'] == 'episode':
					#episodes.append(pp)
					try:
						episode.setdefault(filename, set()).add(pp)
						#episode[filename] = pp
					except:
						print('ex ' ,filename)
	return episode

def get_movies():
	paths = []
	file = []
	movie = {}
	movies = []

	for path, subdirs, files in os.walk(download):
		for name in files:
			pp = os.path.join(path, name)
			#file.append(name)
			#pprint(name)	
			if name.endswith(VideoTypes):
				
				g = guessit(name)
				filename = g['title'].upper()
				
				if g['type'] == 'movie':
					#movies.append(name)
					try:
						movie.setdefault(filename, set()).add(pp)
						#movie[filename] == pp
					except:
						print('ex ',filename)

	return movie


pprint('movies')
pprint(get_movies())
pprint('tv shows')
pprint(get_tv_shows())










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

	
def mkdir():
	l = subfolders()
	#print(l)
	for folder in l:
		s = 'downloads/'+ folder
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
			p = root +'/downloads/'+s+'/'
			r = root + '/downloads/'+a[0]
			print('p2 er : ', p)
			print('r2 er : ', r)

			
			try:
				shutil.move(r, p )
			except:
				print('Tokst ekki að flytja skrár')			
			
		else:
			p = root +'/downloads/'+s+'/'
			r = root + '/downloads/'+a[0]
			print('p er : ', p)
			print('r er : ', r)
			
			try:
				#pass
				shutil.move(r,p)
			except:
				print('Tokst ekki að flytja skrár')	



			

#subfolders()	
#mkdir()
#removeInFolders()




