def insertfile(infile, outfile, line):
	f1 = open(infile,"r")
	data = f1.read()	
	f2 = open(outfile, 'rw+')
	temp = f2.readlines()

	f2.seek(0)
	f2.truncate()
	temp.insert(line,data)

	f2.write(''.join(temp))

def fileline(report,css):
	linecounter = 0

	with open(report, 'r+') as fh:
		for line in fh:
			linecounter += 1
			if line.startswith('<head>'):
				print(line)
				print(linecounter)				
				break

	insertfile(css,report,linecounter)

