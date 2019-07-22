# extract_article_abstract

A simplistic Python code to extract abstract of a single journal article using Microsoft Academic API. User can enter either title or DOI of a paper for MS database query (provide at least one of the two). DOI is converted to title through Crossref API. 

First download [Chrome DRIVER](http://chromedriver.chromium.org/) and provide the executable location in the source code where indicated. Don't forget to update Chrome BROWSER first. Chrome driver may not work properly otherwise. Also pip-install required modules.

Usage Example:

```
d = 'doi.org/10.1107/S0108767307043930'
paper1 = Article(doi=d)
print(paper1.get_abstract())
t = 'A short history of SHELX'
paper2 = Article(title=t)
print(paper2.get_abstract())
```

Notes for adjustable parameters -
(1) Explicit delays twice of default 5 seconds each are included in order for the javascripts to be fully loaded. 
(2) The article title may not exactly match that of the MS D. For instance due to case-sensitivity or punctuation marks. The two titles are compared with difflib.SequenceMatcher. Default threshold is set at 0.9.
