import pywikibot
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def getURL():
	"""
	Gets the API URL of the wiki.

	Returns:
		URL (str): API url of the wiki
	"""

	site = pywikibot.getSite()
	URL = site.protocol() + "://" + site.hostname() + site.scriptpath() + "/api.php"
	return URL

def getAllDuplicateFiles(URL):
	"""
	Gets a list of all the page titles of files listed on Special:ListDuplicatedFiles.

	Parameters:
		URL (str): the API URL of the wiki
	
	Returns:
		output (list): a list with all files' page title on Special:ListDuplicatedFiles
	"""

	PARAMS = {
	"action": "query",
	"generator": "allimages",
	"prop": "duplicatefiles",
	"format": "json"
	}

	session = requests.Session()
	request = session.get(url=URL, params=PARAMS, verify=False)
	outputJson = request.json()

	output = []

	for page in outputJson["query"]["pages"]:
		output.append(outputJson["query"]["pages"][page]["title"])
			
	try:
		DFCONTINUE = outputJson["continue"]["gaicontinue"]
	except:
		DFCONTINUE = ''

	while (DFCONTINUE):
		PARAMS = {
		"action": "query",
		"generator": "allimages",
		"prop": "duplicatefiles",
		"format": "json",
		"gaicontinue": DFCONTINUE
		}

		request = session.get(url=URL, params=PARAMS, verify=False)
		outputJson = request.json()

		for page in outputJson["query"]["pages"]:
			output.append(outputJson["query"]["pages"][page]["title"])
		
		try:
			DFCONTINUE = outputJson["continue"]["gaicontinue"]
		except:
			DFCONTINUE = ''
		
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
	addTemplate("{{Duplicate files}}", getAllDuplicateFiles(getURL()))
