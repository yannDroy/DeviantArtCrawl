import imghdr
import os

dirs = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
        "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
        "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6",
        "7", "8", "9", "_",]

for d in dirs:
    for f in os.listdir("images/%s/" % d):
        name = f.split(".")[0]
        os.rename("images/%s/%s" % (d, f),
                  "images/%s/%s.%s" % (d, name, imghdr.what("images/%s/%s" % (d, f))))
