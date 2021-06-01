import pywikibot
import requests
import json
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Number of pages to process per run
BATCH_SIZE = 2

# Name/path of file to store last processed page
FILE_NAME = "duplicate-files-last.txt"

def getURL():
	"""
	Gets the API URL of the wiki.

	Returns:
		URL (str): API url of the wiki
	"""

	site = pywikibot.getSite()
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
	
	if not os.path.isfile(FILE_NAME):
		last = ''
	else:
		with open(FILE_NAME) as reader :
			last = reader.read()

	print("STARTING AT: " + last)

	PARAMS = {
	"action": "query",
	"generator": "allimages",
	"prop": "duplicatefiles",
	"gailimit": BATCH_SIZE,
	"format": "json",
	"gaicontinue": last
	}

	session = requests.Session()
	request = session.get(url=URL, params=PARAMS, verify=False)
	outputJson = request.json()	

	print(json.dumps(outputJson, indent=2))

	try:
		propContinue = outputJson["continue"]["dfcontinue"]
	except:
		propContinue = ''

	try:
		generatorContinue = outputJson["continue"]["gaicontinue"]
	except:
		generatorContinue = ''

	output = []

	for page in outputJson["query"]["pages"]:
		try:
			duplicate = outputJson["query"]["pages"][page]["duplicatefiles"]
			output.append(outputJson["query"]["pages"][page]["title"])
		except:
			continue

	with open(FILE_NAME, 'w+') as writer:
		try:
			writer.write(outputJson["continue"]["gaicontinue"])
		except:
			writer.write('')
						
	return output

def addTemplate(template, pages):
	"""
	Adds a template to pages in a list.

	Parameters:
		template (str): the template to add
		pages (list): a list of page titles
	"""

	for title in pages:
		page = pywikibot.Page(pywikibot.Site(), title)
		text = page.text
        
		if (text.find(template) != -1):
			print("Template found! Skipping %s..." % (page))
		else:
			print("Template not found on %s! Appending %s..." % (page, template))
			page.text += template
			page.save(u"Add " + template)

if __name__ == "__main__":
	addTemplate("{{Duplicate files}}", getDuplicateFiles(getURL()))
