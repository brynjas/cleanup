import os,os.path,shutil,fnmatch, pathlib
from pprint import pprint
import re
import glob
from guessit import *


root = os.getcwd()
directory_files = os.listdir(root)
download = 'downloads'
rootDownloads = root + '/' + 'downloads/'

JunkFolder = ('EXTRAS', 'extras' , 'sample', 'Sample')
JunkFiles = ('.nfo', '.dat', '.txt', '.torrent', '.sfv', '.ini', '.db', '.url', '.rar', '.rev', '.r00', '.r01','sample.avi','Sample.avi', 'sample.mkv' , 'Sample.mkv','sample.mp4' , 'Sample.mp4','sample')
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


def make_movie_folders(path,Themovie):
	#print('make movie folder ',Themovie)
	nonRemovedMovies = {}
	Movies = os.getcwd() + '/downloads/Movies'
	movie = guessit(Themovie)
	title = movie['title']

	pathtitle =  Movies +'/' + title
	path = os.getcwd() + '/downloads/' + path

	try:
		os.makedirs(Movies)
	except:
		pass
	try:
		os.makedirs(pathtitle)
	except:
		print ('MOvei Didnt make : ', pathtitle)
	# now move the file to new folder 
	try:
		shutil.move(path, pathtitle+'/')
	except:
		print ('Movie Didnt Remove : ', path , pathsesion)
		nonRemovedMovies.setdefault(Themovie, set()).add(path)
	return nonRemovedMovies
	

def make_Tv_folders(path,show):
	nonRemovedTv = {}
	Tv = os.getcwd() + '/downloads/TVShows'	
	tvshow = guessit(show)
	title = tvshow['title']
	sesion =  tvshow['season']
	
	pathtitle =  Tv +'/' + title
	folder = pathtitle + '/sesion ' 
	# this is a dirty mix to get it to  one string
	pathsesion = str(sesion)
	pathsesion = folder + pathsesion

	try:
		os.makedirs(Tv)
	except:
		pass
	try:
		os.makedirs(pathtitle)
	except:
		pass
		#print ('Didnt make : ', pathtitle)
	try:
		os.makedirs(pathsesion)
	except:
		print ('Tv Didnt make : ', pathsesion)	
	# now move the file to new folder 
	try:
		shutil.move(path,(pathsesion+'/'))
	except:
		nonRemovedTv.setdefault(show, set()).add(path)
		print ('TV Didnt Remove : ', path , pathsesion)	
	return nonRemovedTv
	

def get_tv_shows():
	unsorted = {}	
	unsorted2 = {}
	for path, subdirs, files in os.walk(download):
		for name in files:
			thepath = os.path.join(path, name)
			if name.endswith(VideoTypes) or name.endswith(SubTypes):
				g = guessit(name)
				try:
					filename = g['title']
					if re.search(r"((^[Ss][0-9]+([Ee][0-9]+))|(Season|seria|Season)[' ']*[0-9]+)|(^[0-9]{2,10}^[' '])|((ser)\D{2}[' ']*[0-9])" , filename ,re.IGNORECASE) or g['type'] == 'movie':
						unsorted.setdefault(filename, set()).add(thepath)
						#print('filename ', filename)
						continue
					if g['type'] == 'episode':
						dst = make_Tv_folders(thepath,name)
				except:
					#pass
					unsorted2.setdefault(name, set()).add(thepath)	

	return unsorted

def get_movies():
	unsorted = {}
	unsorted2 = {}
	for path, subdirs, files in os.walk(download):
		for name in files:
			thepath = os.path.join(path, name) # the src path 	
			if name.endswith(VideoTypes) or name.endswith(SubTypes):
				g = guessit(name)
				try:
					filename = g['title'].title()
					if re.search(r"((^[Ss][0-9]+([Ee][0-9]+))|(Season|seria|Season)[' ']*[0-9]+)|(^[0-9]{3,20})|((ser)\D{2}[' ']*[0-9])" , filename ,re.IGNORECASE):
						unsorted.setdefault(filename, set()).add(thepath)
						print('unsortet movies ', filename)
						continue
					if g['type'] == 'movie':
						dst = make_movie_folders(name,thepath)
						
				except:
					unsorted2.setdefault(name, set()).add(thepath)
					#print('name without title ', name)

	return unsorted

def remove_junk():
	for paths, subdirs, files in os.walk(download):
		for name in files:
			if name.endswith(JunkFiles) or re.search('sample', name, re.IGNORECASE): 
                #(not name.endswith(VideoTypes)) and (not file.endswith(SoundTypes)) and (not file.endswith(SubTypes)):
				#print('removing: ', name)
				os.remove(os.path.join(paths, name))
			
		remove_empty(paths)


def remove_empty(ThePath):
	if os.path.isdir(ThePath):
		folders = os.listdir(ThePath)
		if len(folders) > 0:
			for folder in folders:
			
				if os.path.isdir(os.path.join(ThePath, folder)): 
					
					if re.search('sample', folder, re.IGNORECASE):
						print('folder ',os.path.join(ThePath , folder) )
						os.rmdir(os.path.join(ThePath , folder))

					remove_empty(os.path.join(ThePath , folder))

		if len(os.listdir(ThePath)) == 0:
			print('removing folder ', ThePath)
			os.rmdir(ThePath)

remove_junk()
#get_tv_shows()
#get_movies()

#reference: http://dev.enekoalonso.com/2011/08/06/python-script-remove-empty-folders/







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





