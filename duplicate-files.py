import pywikibot
import requests
import json
import urllib3
import os


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Number of pages to process per run
BATCH_SIZE = 20

# Name/path of file to store last processed page
FILE_NAME = "duplicate-files-last.txt"

def getURL():
	"""
	Gets the API URL of the wiki.

	Returns:
		URL (str): API url of the wiki
	"""

	site = pywikibot.Site()
	URL = site.protocol() + "://" + site.hostname() + site.apipath()
	return URL

def getDuplicateFiles(URL):
	"""
	Gets a list of all the page titles of files listed on Special:ListDuplicatedFiles.

	Parameters:
		URL (str): the API URL of the wiki
	
	Returns:
		output (list): a list with all files' page title on Special:ListDuplicatedFiles
	"""
	
	#Grabs offset for the query parameters, if none found then defaults to 0
	if not os.path.isfile(FILE_NAME):
		offset = 0
	else:
		with open(FILE_NAME) as reader:
			offset = reader.read()
			if (offset == ''):
				offset = '0'

	print("STARTING WITH OFFSET OF: " + offset)
	
	#Uses query page to grab a batch from Special: ListDuplicatedFiles
	PARAMS = {
	"action": "query",
	"list": "querypage",
	"qppage": "ListDuplicatedFiles",
	"qplimit": BATCH_SIZE,
	"qpoffset": offset,
	"format": "json",
	}

	session = requests.Session()
	request = session.get(url=URL, params=PARAMS, verify=False)
	outputJson = request.json()

	print(json.dumps(outputJson, indent = 2))
	output = []
	
	#Gathering list of pages to send back to main function
	for page in outputJson["query"]["querypage"]["results"]:
		try:
			output.append(page["title"])
		except:
			continue
			
	#Saves the offset so the program knows where to start next time, creating the file if it is not already there
	with open(FILE_NAME, 'w') as writer:
		try:
			writer.write(str(outputJson["continue"]["qpoffset"]))
		except:
			writer.write('0')
					
	return output

def addTemplate(template, pages):
	"""
#	Adds a template to pages in a list.

#	Parameters:
#		template (str): the template to add
#		pages (list): a list of page titles
"""


	for title in pages:
		page = pywikibot.Page(pywikibot.Site(), title)
		text = page.text
        
        #Determines if page already has template, if not then the template is added, if so then the page is skipped
		if (text.find(template) != -1):
			print("Template found! Skipping %s..." % (page))
		else:
			print("Template not found on %s! Appending %s..." % (page, template))
			page.text += template
			page.save(u"Add " + template)

if __name__ == "__main__":
	addTemplate("{{Duplicate files}}", getDuplicateFiles(getURL()))