import sys
import requests
import urllib
import imghdr
import os
from bs4 import BeautifulSoup

dirs = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
        "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
        "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6",
        "7", "8", "9", "_", "()"]

if len(sys.argv) <= 2:
    raise Exception("Usage: %s cutoff URL1 [URL2 URL3 ...]" % sys.argv[0])

if not os.path.exists("visited.dat"):
    os.mknod("visited.dat")

if not os.path.exists("images/"):
    os.mkdir("images")

for d in dirs:
    if not os.path.exists("images/%s" % d):
        os.mkdir("images/%s" % d)

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
