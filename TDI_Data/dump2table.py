# Extract data from dump file.
# import sqlite3
# conn = sqlite3.connect("db.sqlite")

# PATH = '../TDI_dump/tbd.sql'
# PATH_TO_FILE = '../TDI_dump/tbd.sql'
# for line in open(PATH_TO_FILE):
#     conn.cursor.execute(line)

PATH = '../TDI_dump/tbd.sql'
PATH = '../TDI_dump/SGAs.sql'
i = 0
for line in open(PATH, 'r'):
    i += 1
    if i >= 49:
        break
    values = line.split('),(')
    if 'INSERT INTO' in values[0]:
    	#print 'length: {}'.format(len(values))
        #print 'line: {}'.format(i)
        values[-1] = values[-1][:-3]
        tmp = values[0].split('(')
        values[0] = tmp[1]
        for tmp1 in values:
        	print tmp1
