import csv
import os
"""
Parsing model sate output file to csv with following headers:
doc source pos typeindex type topic
"""

fread = open("word-weights.txt", "r+")
fwrite = open("csv/word-weights.csv", "w+")

# writer =  csv.writer(fwrite, delimiter = ',', quotechar = '"')
# str = fread.readline()
# str = ','.join(str.replace("#", "").split())

# fwrite.write(str+"\n")
# fread.readline()
# fread.readline()

for line in fread:
    # if "#alpha" in 
    line = ','.join(line.split())
    fwrite.write(line+"\n")

fread.close()
fwrite.close()