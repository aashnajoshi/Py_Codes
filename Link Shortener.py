from pyshorteners import Shortener as sh
lnk = input("Enter the link you want to Shorten: ")
print(sh().tinyurl.short(lnk))