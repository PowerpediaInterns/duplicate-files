# duplicate-files
Script that adds Template:Duplicate files to any file listed on Special:ListDuplicatedFiles. Also contains a reusable function for adding templates to a list of pages.
## BATCH_SIZE
Number of pages to process per run. The MediaWiki API only returns a maximum of 500 results per response (for bot accounts or those with the apihighlimits right).
## FILE_NAME
Name/path of the file containing the last processed page. Defaults to the pywikibot directory.
