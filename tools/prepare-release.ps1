#prepare for release 

#Activate the python virtual environment
.\.env\Scripts\Activate.ps1

#Minify 
&py process.py -o createstubs_min.py minify

#cross compile to bytecode 
ubuntu run "./tools/mpy-cross -v -X emit=bytecode createstubs.py -o cs.mpy"
ubuntu run "./tools/mpy-cross -v -X emit=bytecode createstubs_min.py -o cs_min.mpy"

#todo: 
# - update minor  version 
# - Add new files to git, 
# - Add git tag 

