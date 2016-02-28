#! C:\python27
from bs4 import BeautifulSoup
from threading import Thread

import re, urllib2, lxml, os, difflib

links = []


def scrape():
	myurl = 'http://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=the-simpsons'
	for i in re.findall('''href=["'](.[^"']+)["']''', urllib2.urlopen(myurl).read(), re.I):
		if i.startswith("view_episode_scripts"):
			links.append(i)
			
def search(searchQuote):
	num = 0
	episode = []
	print '\n'
	quote = searchQuote.lower().replace("'",'').replace('.','').replace(',','').replace('"','').replace('!','').replace('?','').replace('-','')
	for filename in os.listdir("Scripts"):
		with open("Scripts/" + filename) as currentFile:
			text = currentFile.read()
			
			if quote in text:

				for x in re.findall(quote, text):
					num = num + 1
				
				currentFile.seek(0)
				print filename.replace(".txt", "") + " - " + currentFile.readline()
				currentFile.close()
	
	if num == 0:
		print 'Unable to find the Simpsons Quote: "' + searchQuote + '"\n'
	else:
		print 'Your Quote "' + searchQuote + '" appears ' + str(num) + ' time(s) in the episode(s) listed' + '\n'
	
	main()
				
				
			
			
def build():
	scrape()
	
	for i in links:
		link = urllib2.urlopen("http://www.springfieldspringfield.co.uk/" + i).read()
		print 'Opening ' + i
		soup = BeautifulSoup(link, "lxml")
		quote = soup.find('div',{'class':'scrolling-script-container'})
		script = str(quote).lower().replace("'",'').replace('.','').replace(',','').replace('"','').replace('!','').replace('?','').replace('-','')
		heading = soup.find('h3')
		title = str(heading).replace('N/A - ', '').replace('<h3>','').replace('</h3>','')
		
		
		filename = i.replace('view_episode_scripts.php?tv-show=the-simpsons&episode=', '')+ '.txt'
		file = open("Scripts/" + filename, 'w')
		file.write(title + "\n")
		file.write(script)
		file.close()
		
def test():
	with open('Scripts/s01e01 - Copy.txt') as file:

		text = file.read()
		text = text.replace("<br/>", "\n")
		print text
		print 'Done!'
		file.close()
		main()

def main():		
	print "######################################################"
	print "#        WELCOME TO THE SIMPSONS QUOTE FINDER        #"
	print "######################################################"
	print 'Enter your quote to start the search'
	userQuote = raw_input('Enter your Quote: ')
	#build()
	if userQuote == '!build':
		build()
		
	if userQuote == '':
		main()
		
	if userQuote == '!quit':
		exit()
		
	if userQuote == '!test':
		test()
		
	search(userQuote)

if __name__ == "__main__":
	main()
