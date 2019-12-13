import os
import hashlib
import exif
from exif import Image

################
Starting point of directory, if you use Windows System, please enable the WINDOWS_FS=True, and also remember to 
use \\ for windows directory separation mark. For Unix/Linux, then use / of course.
################
STARTING_DIR="C:\\SOME_DIR" 
WINDOWS_FS=True

################
Check the file duplication in the whole subdirectories tree, not only in the same sub-directory.
For example, if CHECK_FULL_SUBDIR==True, then the duplicateion between /a/b/c/xxx.jpg /e/f/g/h/ooo.jpg will be found.
If not, then it will only find the /a/b/c/ooo.jpg and /a/b/c/xxx.jpg
################
CHECK_FULL_SUBDIR=True



################
my_file_map = {}
total_count=0
duplicate_count=0

for root, dirs, files in os.walk(STARTING_DIR):
		for file in files:
			total_count += 1
			path = "{}{}{}".format(root, os.sep, file)
      if WINDOWS_FS:
			  path = path.replace('\\','\\\\')
			if ".DSC" == file[-4:]:	
				os.remove(path)
			else:
				delete_flag=False
				with open(path, 'rb') as image_file:
					filehash = hashlib.md5(image_file.read()).hexdigest()
					if not filehash in my_file_map:
						my_file_map[filehash]=path
						myfile = Image(image_file)
						if myfile.has_exif:
							print((myfile.datetime_original).split(" ")[0].replace(':','_'))
					else:
						duplicate_count+=1
						print("file duplicate - {} \n{}\n{}".format(filehash,path,my_file_map[filehash]))
            root_path=root
            if WINDOWS_FS:
              root_path=root.replace('\\','\\\\')
						if root_path in my_file_map[filehash] or not:
							delete_flag=True
				if delete_flag:			
					os.remove(path)
					print("file removed {}\n".format(duplicate_count))
					
print("total:{}, duplicate:{}".format(total_count, duplicate_count))					
