
import urllib,urllib2
import sys,re
import os

url='http://dizimag.com'

req = urllib2.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
response = urllib2.urlopen(req)
link=response.read()
response.close()
match=re.compile('<a href=(.*?).*? class="yana"><img src=(.*?).*? class=avatar width=40><span><h1>(.*?)</h1>(.*?)</span>').findall(link)
print match

