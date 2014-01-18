import requests


def getSource(URL):
    searchURL = 'http://images.google.com/searchbyimage?image_url=' + URL
    payload = {'image_url' : URL}
    r = requests.get(searchURL)
    print (r.url)
    searchURL = r.url.replace('https://images.google.com/webhp?', 'https://www.google.com/search?')
    
    r = requests.get(searchURL)
    print (r.url)
    print (r.text)
    
    
getSource('http://i.imgur.com/sdCl5Km.png')
