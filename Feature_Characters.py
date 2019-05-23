import re
from urllib.parse import urlparse

def total_special_characters(url_remove_protocol):
	characters = ['-','&','@', '.', '~', '%', '#', '_']
	total_special = {}
	for c in characters:
		total_special[c] = 0
	for c in url_remove_protocol:
		if c in characters:
			total_special[c] += 1
	return total_special

def numDots(total_special):
	return total_special['.']

def numDash(total_special):
	return total_special['-']

def atSymbol(total_special):
	if (total_special['@'] > 0):
		return 1
	return 0
	# return total_special['@']

def tildeSymbol(total_special):
	if total_special['~'] > 0:
		return 1
	return 0
	# return total_special['~']

def numUnderscore(total_special):
	return total_special['_']

def numPercent(total_special):
	return total_special['%']

def numAmpersand(total_special):
	return total_special['&']

def numHash(total_special):
	return total_special['#']

def numNumericChars(url_remove_protocol):
	characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	count = 0
	for c in url_remove_protocol:
		if c in characters:
			count += 1
	return count

def get_TLD():
	f = open("Dataset/list_tld.txt", "r")
	data = []
	for x in f:
		data.append(x[:len(x)-1].lower())
	return data
TLDs = get_TLD()

def domainToken(hostname):
	domain_tokens=hostname.split('.')
	domain_tokens=[x for x in domain_tokens if x!='']
	return domain_tokens

def subdomainLevel(domain_tokens):
	count = 0
	for i in range(len(domain_tokens)):
		if domain_tokens[len(domain_tokens)-1-i] in TLDs:
			count += 1
		else :
			break
	return len(domain_tokens)-count-1

def pathLevel(paths):
	paths_tokens=[re.sub('/','',x) for x in paths]
	return len(paths_tokens)

def urlLength(url_remove_protocol):
	return len(url_remove_protocol)

def numDashInHostname(hostname):
	characters = ['-']
	count = 0
	for c in hostname:
		if c in characters:
			count += 1
	return count

def noHttps(url):
	a = url[:5]
	a = a.lower()
	if a == "https":
		return 1
	return 0
	
def ip_address(domain_tokens):
	for i in domain_tokens:
		if i.isdigit()==False:
			return 0
	else:
		return 1

def get_domain_and_subdomain(domain_tokens):
	count = 0
	for i in range(len(domain_tokens)):
		if domain_tokens[len(domain_tokens)-1-i] in TLDs:
			count += 1
		else :
			break
	sub_domain = domain_tokens[:len(domain_tokens)-1-count]
	domain = domain_tokens[len(domain_tokens)-1-count:len(domain_tokens)]
	sub_domain_str = ""
	for i in range(len(sub_domain)):
		if i == len(sub_domain)-1:
			sub_domain_str += sub_domain[i]
		else :
			sub_domain_str += sub_domain[i] + "."
	domain_str = ""
	for i in range(len(domain)):
		if i == len(domain)-1:
			domain_str += domain[i]
		else :
			domain_str += domain[i] + "."
	return sub_domain_str, domain_str

def domainInSubdomains(domain_tokens):
	sub_domain_str, domain_str = get_domain_and_subdomain(domain_tokens)
	if sub_domain_str.find(domain_str) >= 0:
		return 1
	return 0

def domainInPaths(paths, domain_tokens):
	_, domain_str = get_domain_and_subdomain(domain_tokens)
	paths_tokens=[re.sub('/','',x) for x in paths]
	if domain_str in paths_tokens:
		return 1
	return 0

def httpsInHostname(hostname):
	if hostname.find("https") >= 0:
		return 1
	return 0

def hostnameLength(hostname):
	return len(hostname)

def pathLength(paths):
	count = 0
	for x in paths:
		count += len(x)
	return count

def doubleSlashInPath(paths):
	for x in paths:
		if x.find("//") > 0:
			return 1
	return 0

def numSensitiveWords(url_remove_protocol):
	Suspicious_Words=['secure','account','update','banking','login','click',
			'confirm','password','verify','signin','ebayisapi','lucky','bonus']
	count = 0
	for x in Suspicious_Words:
		count += len(url_remove_protocol.split(x))-1
	return count

def frequentDomainNameMismatch(domain_tokens):
	TLD = domain_tokens[-1]
	if TLD in TLDs:
		return 1
	return 0

def url_length_RT(url_remove_protocol):
    if len(url_remove_protocol) < 54:
        return 1
    elif len(url_remove_protocol) >= 54 and len(url_remove_protocol) <= 75:
        return 0
    else:
       return -1
       
def num_and_size_of_query(paths):
	paths_tokens=[re.sub('/','',x) for x in paths]
	count = 0
	size = 0
	for x in paths_tokens:
		o = urlparse(x)
		size += len(o.query)
		if len(o.query) > 0:
			count += 1
	return size, count

def subdomainLevelRT(domain_tokens):
	sub_domain_str, _ = get_domain_and_subdomain(domain_tokens)
	s = sub_domain_str.split(".")
	if len(s) == 1:
		return 1
	if len(s) == 2:
		return 0
	return -1

def generated(url):
	features = []
	url_remove_protocol=re.sub(r'^http(s*)://','',url)
	patt=r'^[^/]*'
	hostname = re.match(patt,url_remove_protocol).group(0)
	domain_tokens =  domainToken(hostname)
	# print (len(hostname))

	patt_path=r'/[^/]*'	
	paths = re.findall(patt_path,url_remove_protocol)
	total_special = total_special_characters(url_remove_protocol)
	size_query, count_query = num_and_size_of_query(paths)

	features.append(numDots(total_special)) #number "." in url
	features.append(subdomainLevel(domain_tokens)) #number subdomain
	features.append(pathLevel(paths)) #deep of paths
	features.append(urlLength(url_remove_protocol)) #Length of url
	features.append(numDash(total_special)) #number "-" in url
	features.append(numDashInHostname(hostname)) #number "-" in hostname
	features.append(atSymbol(total_special)) #number "@" in url
	features.append(tildeSymbol(total_special)) #number digit in url
	features.append(numUnderscore(total_special)) #number undersorce in url
	features.append(numPercent(total_special)) #number percent in url
	features.append(count_query) #number query in url
	# print (numQueryComponents(url))
	features.append(numAmpersand(total_special)) #number ampersand in url
	features.append(numHash(total_special)) #number hash in url
	features.append(numNumericChars(url_remove_protocol))
	features.append(noHttps(url))
	features.append(ip_address(domain_tokens))
	features.append(domainInSubdomains(domain_tokens))
	features.append(domainInPaths(paths, domain_tokens))
	features.append(httpsInHostname(hostname))
	features.append(hostnameLength(hostname))
	features.append(size_query) #length of query in url
	features.append(pathLength(paths))
	features.append(doubleSlashInPath(paths))
	features.append(numSensitiveWords(url_remove_protocol))
	
	features.append(frequentDomainNameMismatch(domain_tokens))
	# Nhom Tuong Quan
	features.append(url_length_RT(url_remove_protocol))
	features.append(subdomainLevelRT(domain_tokens)) #Rotate subdomain
	return features




