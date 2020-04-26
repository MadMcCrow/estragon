#Copyright (c) 2020 Noé Perard-Gayot. All rights reserved.
# This work is licensed under the terms of the MIT license. 
# For a copy, see <https://opensource.org/licenses/MIT>.

# useful modules
from estragon_log	import log
from git 			import repo

#
# a class representing a git repo
#
class git(object)   :
	
	_Path = str()
	

	def __init__(self, path) :
		super().__init__()

#
# another git 
#
class dependancy(git):

		def __init__(self, path) :
			super().__init__(path)
 
