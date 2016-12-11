# Authors Brynja Skuladottir, Petur Kristofer and Jon H Juliusson





import os,os.path,shutil,fnmatch, pathlib
from pprint import pprint
import re
import glob
from guessit import guessit


unsorted = {}

JunkFolder = ('EXTRAS', 'extras' , 'sample', 'Sample','.DS_Store')
JunkFiles = ('.nfo','style','par2','PAR2', 'sml','ink', 'ignore', 'part','.dat', '.txt', '.torrent', '.sfv', '.ini', '.jpeg','URL', '.db', '.url', 'jpg','png', 'sample.avi','Sample.avi', 'sample.mkv' , 'Sample.mkv','sample.mp4' , 'Sample.mp4','sample','.gif','rar')
VideoTypes = ('.wmv', '.mov', '.avi', '.divx', '.mpeg', '.mpg', '.m4p', '.3gp', '.amv', '.qt', '.rm', '.swf', '.mp4', '.mkv')
SoundTypes = ('.mp3')
SubTypes = ('.jss', '.smx', '.sup', '.srt', '.ssa', '.fab', '.sst', '.tfa', '.usf')
Deletewords = ('hdtv','xvid','-','ftp', 'x264','xvid-ftp', 'ASAP','FQM','lol','P0W4','AFG','PDTV','HDTV')
# i did this list instead of taking it from imbd 
knownTvShows = [ 'LOUIS THEROUX','BORED TO DEATH','DEXTER','BREAKING BAD' ,'THE BIG BANG THEORY','TOP CHEF', 'TOP GEAR', 'WEED','WOULD I LIE TO YOU', 'TRUE DETECTIVE','MODERN FAMILY', 'NÆTURVAKTIN','NEW GIRL', 'MAD MEN', '30 ROCK', 'MASTERCHEF',' JUST A MINUTE', 'HOUSE OF CARDS','HOUSE','HELL KITCHEN', 'GAME OF THRONES','DRAGON DEN','DESPERATE','DAREDEVIL', 'ADVENTURE TIME', '8 OUT OF 10 CATS', 'SHARK TANK','SPOOKS','THAT 70S SHOW','ITS ALWAYS SUNNY IN PHILADELPHIA','PSYCH','FRASIER','SHAMELESS']

def clean(CleanFolder):
	####This doesnt do so much because i am terrible in regex
	for path, subdirs, files in os.walk(CleanFolder):
		for name in files:
			res = re.compile(r"((hdtv|xvid|'-'|ftp|x264|asap|LOL|FQM|p0w4|afg|pdtv|AFG|XviD-FQM|XviD-LOL|cbm*).)", re.IGNORECASE)		
			new_name = res.sub('', name,re.IGNORECASE)
			new_name = res.sub('\'', new_name,re.IGNORECASE)

			newName = (path.split('/'))
			newName = '/'.join(newName) + '/' + new_name
			pp = os.path.join(path, name)
			try:
				os.rename(pp, newName)
			except:
				pass

def make_movie_folders(CleanFolder,path,Themovie):
	#function that makes new folder and moves the movie to the new folder 
	nonRemovedMovies = {}
	Movies = CleanFolder + '/Movies'
	movie = guessit(Themovie)
	title = movie['title']
	
	pathtitle =  Movies +'/' + title
	subpath = path.split('/')[:-1]
	subpath = ''.join(subpath)	
	
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
	#function that makes new folder and moves the tv shows to the new folder 
	nonRemovedTv = {}
	Tv = CleanFolder + '/TVShows'
	tvshow = guessit(show)	
	try:
		title = tvshow['title']
		sesion =  tvshow['season']
	except:
		pass

	pathtitle =  Tv +'/' + title
	folder = pathtitle + '/sesion ' 
	# this is a dirty mix to get it to  one string
	pathsesion = str(sesion)
	pathsesion = folder + pathsesion
	
	
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

def finding_same_TV_show(tvFolder):
	l = []
	for path, subdirs, files in os.walk(tvFolder):
		for name in files:
			l = name.split(' ')
			if l[0] == 'The':
				l = ' '.join(l[0],l[1])
		
		ls = list(os.listdir(l))
		allFiles = [x for x in mylist if mylist.count(x) > 1]
		pprint(allFiles)

		



def get_tv_shows(CleanFolder):
	CleanFolder = CleanFolder 
	print('Sorting All Tv Shows')

	for path, subdirs, files in os.walk(CleanFolder):
		for name in files:
			thepath = os.path.join(path, name)
			if name.endswith(VideoTypes) or name.endswith(SubTypes):
				g = guessit(name)
				try:
					filename = g['title']
					if re.search(r"((^[Ss][0-9]+([Ee][0-9]+))|[' ']+(Season|seria|Season)[' ']*[0-9]+)|(^[0-9]{2,10}^[' '])|((ser)\D{2}[' ']*[0-9])" , filename ,re.IGNORECASE) or g['type'] == 'movie':
						unsorted.setdefault(filename, set()).add(thepath)
						#print('filename ', filename)
						continue
					if g['type'] == 'episode':
						dst = make_Tv_folders(CleanFolder,thepath,name)
					
					#if g['type'] == 'movie':
					#	dst = make_movie_folders(CleanFolder,thepath,name)
				
				except:
					#pass
					unsorted.setdefault(name, set()).add(thepath)	
			
	return unsorted


def get_movies(CleanFolder):
	#os.getcwd() + '/downloads/TVShows'
	print('Sorting All Movies')

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
				
	return unsorted



def unsorted_files(CleanFolder):
	#CleanFolder = '/Users/orcbygg/Documents/python/cleanup/downloads/'
	files = unsorted 
	for key in files.keys():
		file = list(files[key])
		# i er hvert stak i listanum
		#filepath er path i lista 
		for path in file:
			filepath = path.split('/')
			WorkingFolder = CleanFolder.split('/')[-1]
			for show in filepath:

				thelength = path.split(WorkingFolder)[-1]
				Thelength = len(thelength.split('/'))
				thepath = thelength.split('/')
				mainFolder = CleanFolder + '/' + thepath[1]
				
				
				# ugly way to get the leftovers
				a = re.sub('[-\.]', ' ', show).upper()
				a = re.sub('[\']', '', a).upper()
				a = re.sub(' UK', '', a).upper()								
				toSplit = re.split(r'((^[Ss][0-9]+([Ee][0-9]+))|.(Season|seria|Season))' ,a)[0]
				toSplit = re.split(r'[(),]' ,toSplit)[0]

				#print('tosplit ', toSplit)				#print('a ',a)				
				if show.upper() in knownTvShows or a in knownTvShows or toSplit in knownTvShows:
					#pprint(mainFolder)
					newname = mainFolder.split('/')[-1]
					try:
						shutil.move(mainFolder, CleanFolder + '/TVShows/')
					except:
						newpath = CleanFolder + '/TVShows/' + newname
					try:
						shutil.move(mainFolder, newpath)
					except:
						pass
					
	return None

def remove_junk(CleanFolder):

	for paths, subdirs, files in os.walk(CleanFolder):
		for name in files:
			if (not name.endswith(VideoTypes)) and (not name.endswith(SoundTypes)) and (not name.endswith(SubTypes)):
			#if name.endswith(JunkFiles) or re.search((r'([r]\s*[0-9]{2}$)'), name, re.IGNORECASE): 
				os.remove(os.path.join(paths, name))
			
		remove_empty(paths)

def remove_empty(ThePath):
	if os.path.isdir(ThePath):
		folders = os.listdir(ThePath)
		if len(folders) > 0:
			for folder in folders:
				if os.path.isdir(os.path.join(ThePath, folder)):
					#if re.search(r'(^(sample|extras|extra|samples))', folder, re.IGNORECASE):
					#	shutil.rmtree(os.path.join(ThePath , folder), ignore_errors=True)
					#	os.rmdir(os.path.join(ThePath , folder))

					remove_empty(os.path.join(ThePath , folder))
		if len(os.listdir(ThePath)) == 0:
			os.rmdir(ThePath)


def remove_empty_folders(CleanFolder):
	# dirty mix for removing empty folders in downloads dir
	folders = list(os.listdir(CleanFolder))
	for files in os.listdir(CleanFolder):
		if os.path.isdir(os.path.join(CleanFolder,files)):
			r = (os.path.join(CleanFolder,files))
			ls = list(os.listdir(r))
			allFiles = [x for x in ls if not ((x.startswith(JunkFolder) or x.endswith(SubTypes)))]
			if len(allFiles) == 0:
				shutil.rmtree(r, ignore_errors=True)


def make_folders(CleanFolder):
	try:
		os.makedirs(CleanFolder+'/TVShows')
		os.makedirs(CleanFolder+'/Movies')
	except:
		pass
	return None



def finding_same_TV_show(tvFolder):
	shows = []
	ls = list(os.listdir(tvFolder))
	for name in ls:
		l = name.split(' ')
		tv = ""
		for n in l:
			tv = tv + ' ' + n
			if tv.upper() in knownTvShows:
				print(tv)


		
		
	allFiles = [x for x in shows if shows.count(x) > 1]
	pprint(allFiles)


def main():
	
	#CleanFolder = '/Users/orcbygg/Documents/python/cleanup/downloads'
	
	print('\x1b[6;30;43m' + 'Enter or drag the folder you want to clean '+ '\x1b[0m' + '\x1b[7;31;40m' + ' MAKE SURE ITS NO SPACE IN THE END!' + '\x1b[0m'  )
	CleanFolder = input('')
	try:
		os.chdir(CleanFolder)
	except:
		print('\x1b[7;31;40m' + 'Not VALID FOLDER!!!' + '\x1b[0m')
		os.chdir(CleanFolder)


	
	
	make_folders(CleanFolder)
	clean(CleanFolder)
	get_tv_shows(CleanFolder)
	get_movies(CleanFolder)	
	unsorted_files(CleanFolder)


	print('\x1b[6;30;42m' + 'ALLMOST DONE.......' + '\x1b[0m')
	print('Allmost done!! ')
	remove_junk(CleanFolder)
	remove_empty_folders(CleanFolder)
	print('\x1b[6;30;42m' + 'DONE ITS  AS GOOD AS IT GETS' + '\x1b[0m')
	#finding_same_TV_show(CleanFolder+'/TVShows')

	

if __name__ == "__main__":

	main()











