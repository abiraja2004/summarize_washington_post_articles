# to have secure connection
import certifi
# library for http connections
import urllib3
from bs4 import BeautifulSoup

# create a function that will connect to webpages. it takes as input a URL and returning some text.
def scrapeArticle(url, tag):
    # boilerplate code to help beautiful soup to connect to a URL securely using urllib3 and certifi
    # setting up the urllib authentification to httppage variable
    httppage = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    # saving the response as a httpage GET request
    response = httppage.request('GET', url)
    # initializing beautiful soup and sending the data from our response to it. setting parameter to html.parser
    soup = BeautifulSoup(response.data,"html.parser")
    # finding all the SPECIFIC tags of our webpage, getting the TEXT of it, and joining it. Must understand the webpage and figuring out which part of the tags we want from the webpage by inspecting it.
    text = ' '.join(map(lambda p: p.text, soup.find_all(tag)))
    return text