import ipaddress
import re
import requests
import bs4
import urllib.request

def get_id_having_address(url):
    try:
        ipaddress.ip_address(url)
        # print (ipaddress.ip_address(url))
        return 1
    except:
        return -1

def SubmitInfoToEmail(response):
    # Submitting_to_email
    # return 1

    if response == "":
        return -1
    if re.findall(r"[mail\(\)|mailto:?]", response.text):
        return 1
    else:
        return -1
def AbnormalFormAction(response):
    # Abnormal_URL
    if response.text == "":
        return 1
    else:
        return -1

def RightClickDisable(response):
    # RightClick
    if re.findall(r"event.button ?== ?2", response.text):
        return 1
    else:
        return -1

def PopUpWindow(response):
    # popUpWidnow
    if re.findall(r"alert\(", response.text):
        return 1
    else:
        return -1
def IframeOrFrame(response):
    # Iframe
    if re.findall(r"[<iframe>|<frameBorder>]", response.text):
        return 1
    else:
        return -1

def imagesOnlyInForm(soup):
    list_image_form = soup.findAll('input')
    for link in list_image_form:
        # print (link)
        destination = link.get('type')
        if destination != "image":
            return 0
    return 1

def Preprocess(url):
    urlRE = 'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    # print (1)
    try:
        html_page = requests.get(url).text
        # print (1)
    except Exception as e:
        return 0, 0, 0, 0, 0, 0, 0
    # print (1)
    soup = bs4.BeautifulSoup(html_page, features="html.parser")
    a = soup.findAll(href=re.compile(r'/.a\w+'))
    b = ''
    for i in a:
        strre=re.compile('shortcut icon', re.IGNORECASE)
        m=strre.search(str(i))
        if m:
            b = i["href"]
    favicon = 0
    if b != '':
        favicon = 1

    num_links_meta = soup.findAll("meta")
    num_links_script = soup.findAll("script")
    num_links_link = soup.findAll("link")

    num_MetaScriptLink = len(num_links_meta) + len(num_links_link) + len(num_links_script)

    hyperlinkList = soup.findAll('a')
    TotalHyperlink = len(hyperlinkList)
    TotalExternal = 0
    TotalURL = 0
    TotalNullLink = 0
    curURL = url
    for link in hyperlinkList:
        destination = link.get('href')
        if destination != None:
            if destination.startswith(('http', 'ftp', 'www', '/')):
                TotalExternal += 1
            if re.match(urlRE, destination):
                TotalURL += 1
            else :
                TotalNullLink += 1
    # print (TotalHyperlink)
    # print (TotalExternal)
    # print (TotalURL)
    # print (TotalNullLink)
    # print (favicon)
    # print (num_MetaScriptLink)
    return TotalHyperlink, TotalExternal, TotalURL, TotalNullLink, soup, favicon, num_MetaScriptLink
    
def PctExtHyperlinks(TotalExternal, TotalHyperlink):
    if TotalHyperlink != 0:
        return (TotalExternal / TotalHyperlink)
    return 0

def PctExtResourceUrls(TotalURL, TotalHyperlink):
    if TotalHyperlink != 0:
        return (TotalURL / TotalHyperlink)
    return 0

def PctNullSelfRedirectHyperlinks(TotalNullLink, TotalHyperlink):
    if TotalHyperlink!= 0:
        return TotalNullLink/TotalHyperlink
    return 0

def MissingTitle(url, soup):
    # Preprocess(url)
    value = len(soup.findAll('title')) == 0
    # print (value)
    if value == False:
        return 0
    return 1

def pctExtNullSelfRedirectHyperlinksRT(TotalNullLink):
    if TotalNullLink < 31:
        return 1
    if TotalNullLink <= 67:
        return 0
    return -1

def PctExtResourceUrlsRT(TotalURL):
    if TotalURL < 22:
        return 1
    if TotalURL < 61:
        return 0
    return -1

def extMetaScriptLinkRT(num_MetaScriptLink):
    if num_MetaScriptLink < 17:
        return 1
    if num_MetaScriptLink < 81:
        return 0
    return -1


def generate(url):
    # Converts the given URL into standard format
    # url = "https://viblo.asia/p/tim-hieu-ve-url-va-cach-nhan-biet-link-url-an-toan-3P0lPOonZox"
    if not re.match(r"^https?", url):
        url= "http://" + url
    # print (url)
    # return 0
    # Stores the response of the given URL
    try:
        response = requests.get(url)
    except:
        response = ""
    # print (response.text)
    # print (requests.get(url))
    domain = re.findall(r"://([^/]+)/?", url)[0]
    features = []
    if response == "":
        features.append(-1)
        features.append(-1)
        features.append(-1)
        features.append(-1)
        features.append(-1)
    else :
        features.append(SubmitInfoToEmail(response))
        features.append(AbnormalFormAction(response))
        features.append(RightClickDisable(response))
        features.append(PopUpWindow(response))
        features.append(IframeOrFrame(response))
    TotalHyperlink, TotalExternal, TotalURL, TotalNullLink, soup, favicon, num_MetaScriptLink= Preprocess(url)
    features.append(favicon)
    # print (1)
    if TotalExternal == 0 and TotalURL == 0 and TotalHyperlink == 0:
        features.append(-1)
        features.append(-1)
        features.append(-1)
        features.append(-1)
        features.append(-1)
        features.append(-1)
        features.append(-1)
    else :
        features.append(PctExtHyperlinks(TotalExternal, TotalHyperlink))
        features.append(PctExtResourceUrls(TotalURL, TotalHyperlink))
        features.append(PctNullSelfRedirectHyperlinks(TotalNullLink, TotalHyperlink))
        features.append(MissingTitle(url, soup))
        features.append(pctExtNullSelfRedirectHyperlinksRT(TotalNullLink))
        features.append(PctExtResourceUrlsRT(TotalURL))
        features.append(extMetaScriptLinkRT(num_MetaScriptLink))
    return (features)
# generate("https://www.facebook.com/")
