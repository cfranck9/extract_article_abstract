from bs4 import BeautifulSoup as BS
from difflib import SequenceMatcher
from unidecode import unidecode
from selenium import webdriver
from crossref.restful import Works
import time
import urllib.parse

class Article:
    def __init__(self, title = '', doi = '', convert_unicode = False, delay = 5, threshold = 0.9):
        self.title = title
        self.doi = doi
        self.convert_unicode = convert_unicode
        self.delay = delay
        self.threshold = threshold

    def fetch_article_title_with_doi(self, doi):
        works = Works()
        item = works.doi(doi)
        return unidecode(item['title'][0]) if item and 'title' in item and item['title'] else ''

    # retrieve MS-Academic internal ID
    def fetch_article_id_with_title(self, driver, title):
        try:
            parsed_title = urllib.parse.quote_plus(title)
        except TypeError as msg:
            print('Type Error :', str(msg))
            driver.close()
            return -1
        driver.get('https://academic.microsoft.com/search?q=' + parsed_title)
        time.sleep(self.delay)   # until javascripts are fully loaded into DOM
        soup = BS(driver.page_source, 'html.parser')
        try:
            article_id = soup.find('a', {"class":"title au-target"}).attrs['href'].split('/')[1]
        except AttributeError as msg:
            print('Attribute Error :', str(msg))
            driver.close()
            return -1
        return article_id

    def fetch_single_abstract(self, driver, article_id):
        driver.get('https://academic.microsoft.com/paper/' + str(article_id))
        time.sleep(self.delay)
        soup = BS(driver.page_source, 'html.parser')
        try:
            extracted_title = soup.find_all('div', attrs = {'class':'name'})[0].text
            # double check article title : extracted_title may not exactly match title due to punctuation marks
            if SequenceMatcher(None, extracted_title.lower(), self.title.lower()).ratio() > self.threshold:
                abstract = soup.find('p').text
                if abstract.split(' ')[0].lower() == 'abstract':
                    abstract = abstract.replace(abstract.split(' ')[0], '').lstrip()
                # unicode issue - https://stackoverflow.com/a/8087475
                if self.convert_unicode:
                    abstract = unidecode(abstract)
            else:
                print('failed to find matching article')
                abstract = ''
        except IndexError as msg:
            print('Index Error :', str(msg))
            return ''
        return abstract

    def get_abstract(self):
        if not self.doi and not self.title:
            print('Error : article information not provided')
            return ''
        if self.doi:
            self.title = self.fetch_article_title_with_doi(self.doi)
        # update line 70 with your local Chrome Driver location
        driver = webdriver.Chrome(r'C:\Users\Chung Koo\.PyCharmCE2018.3\config\scratches\chromedriver.exe')
        article_id = self.fetch_article_id_with_title(driver, self.title)
        abstract = ''
        if article_id == -1:
            print('Error : article ID fetching failed')
        else:
            abstract = self.fetch_single_abstract(driver, article_id)
        driver.close()
        return abstract
