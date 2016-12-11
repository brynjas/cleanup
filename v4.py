import os,os.path,shutil,fnmatch, pathlib
from pprint import pprint
import re
import glob
from guessit import *


root = os.getcwd()

JunkFolder = ('EXTRAS', 'extras' , 'sample', 'Sample','.DS_Store')
JunkFiles = ('.nfo', '.dat', '.txt', '.torrent', '.sfv', '.ini', '.jpeg','URL', '.db', '.url', 'jpg','png', 'sample.avi','Sample.avi', 'sample.mkv' , 'Sample.mkv','sample.mp4' , 'Sample.mp4','sample','.gif','rar')
VideoTypes = ('.wmv', '.mov', '.avi', '.divx', '.mpeg', '.mpg', '.m4p', '.3gp', '.amv', '.qt', '.rm', '.swf', '.mp4', '.mkv')
SoundTypes = ('.mp3')
SubTypes = ('.jss', '.smx', '.sup', '.srt', '.ssa', '.fab', '.sst', '.tfa', '.usf')
Deletewords = ('hdtv','xvid','-','ftp', 'x264','xvid-ftp', 'ASAP','FQM','lol','P0W4','AFG','PDTV','HDTV')
knownTvShows = ['BORED TO DEATH','DEXTER','BREAKING BAD' ,'THE BIG BANG THEORY','TOP CHEF', 'TOP GEAR', 'WEED','WOULD I LIE TO YOU', 'TRUE DETECTIVE','MODERN FAMILY', 'NÆTURVAKTIN','NEW GIRL', 'MAD MEN', '30 ROCK', 'MASTERCHEF',' JUST A MINUTE', 'HOUSE OF CARDS','HOUSE','HELL KITCHEN', 'GAME OF THRONES','DRAGON DEN','DESPERATE','DAREDEVIL', 'ADVENTURE TIME', '8 OUT OF 10 CATS', 'SHARK TANK','SPOOKS','THAT 70S SHOW','ITS ALWAYS SUNNY IN PHILADELPHIA','PSYCH','FRASiER']

def clean(CleanFolder):
	####This doesnt do so much because i am terrible in regex
	print('clean()')
	for path, subdirs, files in os.walk(CleanFolder):
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

def make_movie_folders(CleanFolder,path,Themovie):
	nonRemovedMovies = {}
	Movies = CleanFolder + '/Movies'
	movie = guessit(Themovie)
	title = movie['title']
	
	pathtitle =  Movies +'/' + title
	subpath = path.split('/')[:-1]
	subpath = ''.join(subpath)	
	try:
		os.makedirs(Movies)
	except:
		pass
	try:
		os.makedirs(pathtitle)
	except:
		pass
	try:
		shutil.move(path, pathtitle+'/' )
	except:
		nonRemovedMovies.setdefault(Themovie, set()).add(path)
	return nonRemovedMovies	

def make_Tv_folders(CleanFolder,path,show):
	nonRemovedTv = {}
	Tv = CleanFolder + '/TVShows'
	tvshow = guessit(show)
	title = tvshow['title']
	sesion =  tvshow['season']
	sesion = 'unknown'
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
	try:
		os.makedirs(pathsesion)
	except:
		pass

	try:
		shutil.move(path,(pathsesion))
	except:
		nonRemovedTv.setdefault(show, set()).add(path)
		#print ('TV Didnt Remove : ', path , pathsesion + '/')	
	return nonRemovedTv
	

def get_tv_shows(CleanFolder):
	CleanFolder = CleanFolder 
	print('get tv shows()')
	unsorted = {}	
	unsorted2 = {}
	for path, subdirs, files in os.walk(CleanFolder):
		for name in files:
			thepath = os.path.join(path, name)
			if name.endswith(VideoTypes):# or name.endswith(SubTypes):
				g = guessit(name)
				try:
					filename = g['title']
					if re.search(r"((^[Ss][0-9]+([Ee][0-9]+))|(Season|seria|Season)[' ']*[0-9]+)|(^[0-9]{2,10}^[' '])|((ser)\D{2}[' ']*[0-9])" , filename ,re.IGNORECASE) or g['type'] == 'movie':
						unsorted.setdefault(filename, set()).add(thepath)
						#print('filename ', filename)
						continue
					if g['type'] == 'episode':
						dst = make_Tv_folders(CleanFolder,thepath,name)
				except:
					#pass
					unsorted.setdefault(name, set()).add(thepath)	
			if name.endswith(SubTypes):
				subtitles = CleanFolder + '/Subs_Tv_shows'
				try:
					os.makedirs(subtitles)
				except:
					print('sub ' , subtitles)
				try:
					shutil.move(thepath,(subtitles + '/'))
				except:
					print( 'move sub ', subtitles + '/')


	return unsorted

def get_movies(CleanFolder):
	CleanFolder = CleanFolder 
	#os.getcwd() + '/downloads/TVShows'
	print('get  movies()')
	unsorted = {}
	unsorted2 = {}
	for path, subdirs, files in os.walk(CleanFolder):
		for name in files:
			thepath = os.path.join(path, name) # the src path 	
			if name.endswith(VideoTypes) or name.endswith(SubTypes):
				g = guessit(name)
				try:
					filename = g['title']
					if re.search(r"((^[Ss][0-9]+([Ee][0-9]+))|(Season|seria|Season)[' ']*[0-9]+)|(^[0-9]{1,20})|((ser)\D{2}[' ']*[0-9])" , filename ,re.IGNORECASE):
						unsorted.setdefault(filename, set()).add(thepath)
						#print('unsortet movies ', filename)
						continue
					if g['type'] == 'movie':
						dst = make_movie_folders(CleanFolder,thepath,name)
						
				except:
					unsorted.setdefault(name, set()).add(thepath)
					#print('name without title ', name)
			
				
	#unsorted_files(unsorted)
	return unsorted

#This is a Test function
def dicts(CleanFolder):
	CleanFolder = CleanFolder 
	unsorted = {}	
	for path, subdirs, files in os.walk(CleanFolder):
		for name in files:
			thepath = os.path.join(path, name)			
			unsorted.setdefault(name, set()).add(thepath)	

	return unsorted





def unsorted_files(CleanFolder):
	#CleanFolder = '/Users/orcbygg/Documents/python/cleanup/downloads/'
	files = dicts(CleanFolder) 
	for key in files.keys():
		file = list(files[key])
		# i er hvert stak i listanum
		#filepath er path i lista 
		for path in file:
			filepath = path.split('/')
			for show in filepath:
				a = re.sub('[^A-Za-z0-9\.]*', '', show)
								#print('a ',a)
				if show.upper() in knownTvShows or a.upper() in knownTvShows:
					r = '/'.join(filepath[0:-2])

					try:
						shutil.move(r, CleanFolder + '/TVShows')
					except:
						pass
				if show.endswith(SoundTypes):

					r = '/'.join(filepath[0:-1])
					try:
						os.makedirs(CleanFolder + '/Music')
					except:
						pass

					try:
						shutil.move(r, CleanFolder + '/Music/')
					except:
						pass


	return None

def remove_junk(CleanFolder, mybool):
	print('remove junk()')
	for paths, subdirs, files in os.walk(CleanFolder):
		for name in files:
			if (not name.endswith(VideoTypes)) and (not name.endswith(SoundTypes)) and (not name.endswith(SubTypes)):

			#if name.endswith(JunkFiles):# or re.search((r'($[r][0-9]{2})'), name, re.IGNORECASE): 
				os.remove(os.path.join(paths, name))
			
		remove_empty(paths, mybool)



def remove_empty(ThePath , mybool):
	if os.path.isdir(ThePath):
		folders = os.listdir(ThePath)
		if len(folders) > 0:
			for folder in folders:
				if os.path.isdir(os.path.join(ThePath, folder)):

					if re.search(r'(sample|extras|extra|samples)', folder, re.IGNORECASE) and bool == 1:
						shutil.rmtree(os.path.join(ThePath , folder), ignore_errors=True)
						os.rmdir(os.path.join(ThePath , folder))
					remove_empty(os.path.join(ThePath , folder), mybool)
		if len(os.listdir(ThePath)) == 0:
			print('removing folder ', ThePath)
			os.rmdir(ThePath)


def remove_empty_folders(CleanFolder):
	# dirty mix for removing empty folders in downloads dir
	folders = list(os.listdir(CleanFolder))
	#pprint(folders)
	for files in os.listdir(CleanFolder):
		if os.path.isdir(os.path.join(CleanFolder,files)):
			r = (os.path.join(CleanFolder,files))
			ls = list(os.listdir(r))
			allFiles = [x for x in ls if not x.startswith(JunkFolder)]
			if len(allFiles) == 0:
				shutil.rmtree(r, ignore_errors=True)



def main():
	#CleanFolder = '/Users/orcbygg/Documents/python/cleanup/downloads'
	CleanFolder = input('Enter or drag (MAKE SURE its not space in the END!!!) the folder you want to clean: ')
	os.chdir(CleanFolder)
	myBool = 0
	samples = input('If you want to delete all sample files and Extra press 1 if not press 0')
	if samples == '1':
		myBool = 1

	clean(CleanFolder)
	get_tv_shows(CleanFolder)
	get_movies(CleanFolder)	
	unsorted_files(CleanFolder)



	print('Allmost done!! ')
	remove_junk(CleanFolder, myBool)
	remove_empty_folders(CleanFolder)


	

if __name__ == "__main__":

	main()




'''def check_if_folder_exist_for_show(dst,foldername):
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
	return False'''





