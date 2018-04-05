import sys
import os
import re
import pyperclip

undoStack = []
redoStack = []
current = []

def undoFunc(name):
	if len(undoStack) == 0:
		print "NO changes yet"
	else:
		element = undoStack.pop()
		global current
		redoStack.append(current)
		current = element
		f = open(name, "w")
		f.writelines(current)
		f.close


def redoFunc(name):
	if len(redoStack) == 0:
		print "Nothing undone yet..Please Undo first"
	else:
		element = redoStack.pop()
		f = open(name, "w")
		f.writelines(element)
		f.close


def display(name):
	fh = open(name, "r")
	print fh.read()

def displayLine(name, start, end):
	fh = open(name, "r")
	lines = []
	for i in fh:
		lines.append(i)

	for i in range(int(start)-1, int(end)):
		print lines[i],

def insertLines(name, num, text):
	f = open(name, "r")
	contents = f.readlines()
	f.close()

	f1 = open(name, "r")
	t1 = f1.readlines()
	undoStack.append(t1)
	f1.close()
	
	text = text + "\n"
	if num > len(contents):
		for i in range(1, num - len(contents)):
			text = "\n" + text
	else:
		pass

	if num == 0:
		num = 1

	contents.insert(num-1, text)
	f = open(name, "w")
	contents = "".join(contents)
	f.write(contents)
	global current
	current = contents
	f.close()


def deleteLine(name, num):
	f = open(name, "r")
	contents = f.readlines()
	f.close()

	f2 = open(name, "r")
	t2 = f2.readlines()
	undoStack.append(t2)
	f2.close()
	
	if int(num) == 0:
		print "Nothing at line 0"
	elif int(num) > len(contents):
		print "No content at given line number"
	else:
		del contents[int(num)-1]
		f = open(name, "w")
		f.writelines(contents)
		global current
		current = contents
		f.close
		# print current

def deleteManyLines(name, start, end):
	f = open(name, "r")
	contents = f.readlines()
	f.close()
	
	f3 = open(name, "r")
	t3 = f3.readlines()
	undoStack.append(t3)
	f3.close()

	if int(start) == 0:
		print "No Line starting at 0"
	elif int(end) > len(contents):
		print "No content at given line number"
	else:
		del contents[int(start)-1 : int(end)]
		f = open(name, "w")
		f.writelines(contents)
		global current
		current = contents
		f.close

def copyLines(name, start, end):
	f = open(name,"r")
	lines=[]
	linescopy=""
	for i in f:
		lines.append(i)

	if int(start) == 0:
		print "No Line starting at 0"
	elif int(end) > len(lines):
		print "NO line at given line number"
	else:
		for i in range(int(start)-1, int(end)):
				linescopy = linescopy + lines[i]

	pyperclip.copy(linescopy)

	# print pyperclip.paste()

def pasteLines(name, num):
	# print pyperclip.paste()
	text = pyperclip.paste()

	f = open(name, "r")
	contents = f.readlines()
	f.close()

	f4 = open(name, "r")
	t4 = f4.readlines()
	undoStack.append(t4)
	f4.close()

	if int(num) > len(contents):
		for i in range(0, int(num) - len(contents)):
			text = "\n" + text
	else:
		pass

	if num == 0:
		print "No Line starting at 0"
	else:
		contents.insert(int(num)-1, text)
		f = open(name, "w")
		contents = "".join(contents)
		f.write(contents)
		global current
		current = contents
		f.close()

if __name__ == '__main__':
	if sys.argv >= 2:
		name = sys.argv[1]
		print "\n"
		
		print "		HELLO...BELOW IS THE TEXT EDITOR.\n"

		print "                             | COMMANDS |"
		print " -------------------------------------------------------------------------------"
		print " | Display contents (d)           : Show contents of the file"
		print " | Display Specific lines (d.n.m) : Show contents of line numbers n to m"
		print " | Insert line (i.n.<text>)       : Insert the <text> at line number n"
		print " | Delete line (dd.n)             : Delete line number n"
		print " | Delete lines (dd.n.m)          : Delete lines from n to m"
		print " | Copy lines (yy.n.m)            : Copy lines from line number n to m"
		print " | Paste (p.n)                    : Paste the clipboard contents at line number n"
		print " | Undo (z)                       : Undo the last command"
		print " | Redo (zz)                      : Redo the last undone command"
		print " | Exit (exit)                    : To exit the Text Editor"

		print "\n"
		while(True):
			k = raw_input("==> ")

			if k == "d":
				display(name)

			elif re.match('d.[0-9].[0-9]', k):
				a, start, end = k.split(".")
				if int(end) > int(start):
					displayLine(name, start, end)
				else:
					print "Error: Please enter correct numbers"

			elif re.match('i.([0-9][^a-zA-Z]).[a-zA-Z0-9_]*', k):
				a, num, text = k.split(".")
				insertLines(name, int(num), text)

			elif re.match('dd.[0-9]', k):
				if k.count(".") == 1:
					a, num = k.split(".")
					deleteLine(name, num)
				else:
					a, start, end = k.split(".")
					if int(end) > int(start):
						deleteManyLines(name, start, end)
					else:
						print "Error: Please enter correct numbers"

			elif re.match('yy.[0-9].[0-9]', k):
				a, start, end = k.split(".")
				if int(end) > int(start):
					copyLines(name, start, end)
				else:
					print "Error: Please enter correct numbers"

			elif re.match('p.[0-9]', k):
				a, num = k.split(".")
				pasteLines(name, num)

			elif k == "z":
				undoFunc(name)

			elif k == "zz":
				redoFunc(name)

			elif k == "exit":
				print "Thank You for using Text Editor"
				exit()

			else:
				print "Invalid Command, Please try Again..."