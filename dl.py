import sys
import requests
import urllib
import imghdr
import os
from bs4 import BeautifulSoup


if len(sys.argv) <= 2:
    raise Exception("Usage: %s cutoff URL1 [URL2 URL3 ...]" % sys.argv[0])

os.utime("visited.dat", None)

visited = open("visited.dat").read().splitlines()
new_visited = []
to_visit = []
cutoff = int(sys.argv[1])
count = 0

for arg in sys.argv[2:]:
    if arg not in to_visit:
        to_visit.append(arg)

print("\n\nDownloading %d random images from DeviantArt...\n\n" % cutoff)

while len(to_visit) > 0 and count < cutoff:
    url = to_visit[0]
    
    to_visit.remove(url)

    if url not in visited and url not in new_visited:
        count += 1

        print(" ===> Visiting %d: '%s'" % (count, url))

        try:
            req = requests.get(url)
        
            soup = BeautifulSoup(req.text, "html5lib")
            
            src = soup.img.attrs["src"]
            
            name = src.split("/")[-1].split('.')[0]
            dirname = name[0]
            
            urllib.request.urlretrieve(src, "images/%s/%s" % (dirname, name))
            os.rename("images/%s/%s" % (dirname, name),
                      "images/%s/%s.%s" % (dirname, name,
                                           imghdr.what("images/%s/%s" % (dirname, name))))
            
            new_visited.append(url)
        
            next_images = soup.findAll("div", {"class": "tt-crop thumb"})
    
            for i in next_images:
                to_visit.append(i.a.attrs["href"])
            
        except Exception as e:
            print("      !!! Issue with this URL: %s" % e)
    
    else:
        print(" (Ignoring: '%s')" % url)

file_visited = open("visited.dat", "a")

for f in new_visited:
    file_visited.write(f)
    file_visited.write("\n")

file_visited.close()
