#this will be made into exe.
#when you click on the exe, it opens a cmd and runs lyricTerminal.py on it.
import subprocess
import lyricTerminal

subprocess.popen(['cmd .lyricCode.py'])
