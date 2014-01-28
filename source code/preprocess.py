#!/usr/bin/python
import re, csv, sys
from urlparse import urlparse
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.text import TextCollection

#process command line arguments
if len(sys.argv) < 2:
	print "ERROR: arg1: must specify the input file"
	print "       arg2: specify -t to generate test ARFF"
	sys.exit(1)
	
test = False
if len(sys.argv) > 2:
	test = (sys.argv[2] == '-t')

# initialize some variables
stoplist = stopwords.words('english')
stoplist.extend(['.', ',', ':', '?', '!' ';', '"', "'", '-', '--', '(', ')', '/', '\\', 
                 '[', ']', '{', '}', '|', '+', '*', '^'])
emots_pos = [':)', ':D', ':-)', ':-D', '=)', '=D', ':]', ':-]', '=]', 'X)', 'XD', 'X]', 
             'X-)', 'X-D', 'X-]', 'C:', ';)', ';D', ';]', ';-)', ';-D', ';-]', '<3', 
			 ':P', ':-P', '=P', 'XP', 'X-P', ':o)', ':3', ':>', '8)', ':^)', '8-D', '8D',
			 '=3', 'B^D', '\\o/', '<:', '(:', '(-:', '(=', '[:', '[-:', '[=', '(X', '[X',
			 '(-X', '[-X', ':\')', ':\'-)', ':\']', ':\'-]', '=\')', '=\']', ';^)', 
			 '>:P', ':-b', ':b']
emots_pos = [emot.lower() for emot in emots_pos]
emots_neg = [':(', ':[', ':-(', ':-[', 'D:', '=(', '=[', 'D=', 'DX', ':C', '</3',
			'>:[', ':-c', ':-<', ':<', '>:', ':{', ':\'-(', ':\'(', ':\'[', '=\'(', 
			'=\'[', 'D;', 'D\':', 'D:<', 'D8', 'D-\':', '):', ']:', ')-:', ']-:', 
			')=', ']=', ']:<', '>-:']
emots_neg = [emot.lower() for emot in emots_neg]
gaz_pos = []
gaz_neg = []
tweets = []
sentiments = []
emots_count = []
punct_count = []
gaz_count = []
words = []      #will contain all non-stop words that occur >1 times
words1 = []     #will contain all non-stop words that occur 1 time

# generate the gazetteers
gaz_file = open('positive-words.txt', 'r')
for line in gaz_file:
	line = line.strip()
	if line != '' and line[0] != ';':
		gaz_pos.append(line)
gaz_file.close()

gaz_file = open('negative-words.txt', 'r')
for line in gaz_file:
	line = line.strip()
	if line != '' and line[0] != ';':
		gaz_neg.append(line)
gaz_file.close()

# print some information
print 'Number of positive emoticons: ' + str(len(emots_pos))
print 'Number of negative emoticons: ' + str(len(emots_neg))
print '\nNumber of positive gazetteer words: ' + str(len(gaz_pos))
print 'Number of negative gazetteer words: ' + str(len(gaz_neg))

# extract all tweets and words (IN TRAINING)
words_file = []
if not test:
	words_file = open('words-list.txt', 'w')  # COMMENT OUT FOR TESTING
tweet_file = open(sys.argv[1], 'rb')
reader = csv.reader(tweet_file, delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
for line in reader:
	# save tweet data
	tweet = line[4].lower()
	sent = line[1]
	
	# REMOVE THIS SECTION FOR TESTING
	if not test:
		if sent == 'positive':
			sent = 'POS'
		elif sent == 'negative':
			sent = 'NEG'
		else:
			sent = 'OTHER'
	
	sentiments.append(sent)
    
	# standardize URLs
	w = tweet.split()
	for i in range(len(w)):
		r = urlparse(w[i])
		if r[0] != '' and r[1] != '':
			w[i] = 'URL'
	tweet = ' '.join(w)
	tweets.append(tweet)
	
    # count emoticons
	count_pos = 0
	for emot in emots_pos:
		count_pos += tweet.count(emot)
	
	count_neg = 0
	for emot in emots_neg:
		count_neg += tweet.count(emot)
	
	emots_count.append( (count_pos, count_neg) )
	
	# count punctuation
	punct_count.append( (tweet.count('?'), tweet.count('!')) )
	
	# count gazetteer words
	count_pos = 0
	for gw in gaz_pos:
		count_pos += tweet.count(gw)
	
	count_neg = 0
	for gw in gaz_neg:
		count_neg += tweet.count(gw)
	
	gaz_count.append( (count_pos, count_neg) )
	
	# USE THIS SECTION FOR TRAINING 
	# extract only words used >1 times, and ignore stopwords
	if not test :
		tweet_sents = sent_tokenize(tweet)
		for sent in tweet_sents:
			sw = word_tokenize(sent)
			for word in sw:
				if word not in stoplist:
					if word not in words:
						if word in words1:
							words.append(word)
							words_file.write(word + '\n')
						else:
							words1.append(word)
tweet_file.close()
if not test:
	words_file.close() # COMMENT OUT FOR TESTING

# USE THIS SECTION FOR TESTING
# extract all words (IN TESTING)
if test:
	wfile = open('words-list.txt', 'r')
	for line in wfile:
		words.append(line.strip())
	wfile.close()

# print some more information
print '\nNumber of tweets: ' + str(len(tweets))
print 'Number of words occuring >1 time: ' + str(len(words))
print 'Number of words occuring 1 time: ' + str(len(words1))

# create .arff file for Weka
texts = TextCollection(tweets)
arff = open('tweets_sentiment.arff', "w")
wc = 0

# header
arff.write("@relation sentiment_analysis\n\n")
arff.write("@attribute numPosEmots numeric\n")
arff.write("@attribute numNegEmots numeric\n")
arff.write("@attribute numQuest numeric\n")
arff.write("@attribute numExclam numeric\n")
arff.write("@attribute numPosGaz numeric\n")
arff.write("@attribute numNegGaz numeric\n")
for word in words:
	arff.write("@attribute word_")
	sub_w = re.subn('[^a-zA-Z]', 'X', word)
	arff.write(sub_w[0])
	if sub_w[1] > 0:
		arff.write('_' + str(wc))
		wc += 1
	arff.write(" numeric\n")
arff.write("@attribute class {POS, NEG, OTHER}\n\n")
arff.write("@data\n")

# data
for i in xrange(len(tweets)):
	arff.write(str(emots_count[i][0]) + ',' + str(emots_count[i][1]) + ',')
	arff.write(str(punct_count[i][0]) + ',' + str(punct_count[i][1]) + ',')
	arff.write(str(gaz_count[i][0]) + ',' + str(gaz_count[i][1]) + ',')
	
	for j in xrange(len(words)):   #loop through unigrams
		arff.write(str(texts.tf_idf(words[j], tweets[i])) + ',')
	
	arff.write(sentiments[i] + '\n')

arff.close()
print '\nFinished pre-processing! The ARFF file for Weka has been created.'