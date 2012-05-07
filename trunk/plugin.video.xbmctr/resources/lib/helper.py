# Multi Documentary Streams, is an XBMC add on that sorts and displays 
# video content from several websites to the XBMC user.
#
# Copyright (C) 2011, Ricardo Ocana Leal
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
Created on 14 nov 2011

@author: drascom
edited on 13 04 2012 
'''

import urllib2, re
import scraper

'''
Method that searches through a site for available videos.
 
@param url: URL to the site containing the videos
@param videoTitle: String with the title of the video to search for
'''
def prepareVideo(url, videoTitle):
    i=0
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8')
    response = urllib2.urlopen(req)
    link=response.read()
    gurl=response.geturl()
    #codemega=gurl[-8:]
    altcode=re.compile('href="http://www.youtube.com/view_play_list(.+?)"').findall(link)
    secondaltcode=re.compile('.*src="http://www.youtube.com/embed/videoseries\?list=(.+?)"').findall(link)
    thirdaltcode=re.compile('value="http://www.youtube.com/p/(.+?)"').findall(link)
    stagevu=re.compile('href="http://stagevu.com/(.+?)">StageVu</a>').findall(link)
    #smalltitle=re.compile('target="_blank" href="(.+?)">(.+?)</a></strong>').findall(link)
    veehd=re.compile('href="http://veehd.com/video/(.+?)">VeeHD</a>').findall(link)
    gubacode=re.compile("src='http://www.guba.com/.+?bid=(.+?)' quality='.+?'").findall(link)
    
    #Search for videos hosted on "stageVu"
    for code in stagevu:
        if scraper.stageVu(code, i):
            i=i+1
    '''        
    for url, name in smalltitle:
        scraper.smallTitle(url, name)text = re.sub('&amp;', '&', text)
    '''    
    #Search for videos hosted on "veeHD"
    for code in veehd:
        scraper.veeHD(code)
        
    #Search for playlist videos hosted on "youtube"
    for code in altcode:
        code = code.replace('?p=','')
        scraper.youTubePlaylist(code, videoTitle)
    
    #Search for playlist videos hosted on "youtube"    
    for code in secondaltcode:
        code = code[2:18]
        scraper.youTubePlaylist(code, videoTitle)
        
    #Search for playlist videos hosted on "youtube"
    for code in thirdaltcode:
        code = code[:16]
        scraper.youTubePlaylist(code, videoTitle)
        
    #Search for single video hosted on "youtube"
    try:
        coderaw2 = re.compile('value="http://www.youtube.com/v/(.+?)"').findall(link)[0]
        codeplist2 = coderaw2[:11]
        scraper.youTube("http://www.youtube.com/watch?v="+codeplist2, videoTitle)
    except: pass
    
    #Search for single video hosted on "youtube"
    try:
        coderaw2 = re.compile('"http://www.youtube.com/embed/(.+?)"').findall(link)[0]
        codeplist2 = coderaw2.replace('?rel=0','')
        scraper.youTube("http://www.youtube.com/watch?v="+codeplist2, videoTitle)
    except: pass
    
    #Search for single video hosted on "youtube"
    try:
        coderaw2 = re.compile('"http://www.youtube.com/embed/(.+?)"').findall(link)[0]
        scraper.youTube("http://www.youtube.com/watch?v="+str(coderaw2), videoTitle)
    except: pass
    
    #Search for videos hosted on "Guba"
    try:
        scraper.guba(gubacode, videoTitle)
    except: pass
    
    #Search for videos hosted on "Vimeo"
    try:
        swap = re.compile('clip_id=(.+?)&amp;server=vimeo').findall(link)
        if not swap:
            swap = re.compile('"http://player.vimeo.com/video/(.+?)?title').findall(link)
        if not swap:
            swap= re.compile('"http://player.vimeo.com/video/(.+?)"').findall(link)
            
        for code in swap:
            scraper.vimeo(code, videoTitle)
    except: pass
    
    #Search for videos hosted on "googlevideo"
    try:
        swap = re.compile('src=".+?docId=(.+?)"').findall(link)
        if not swap:
            swap = re.compile('type="application/x-shockwave-flash" src=".+?docId=(.+?)"').findall(link)
        if not swap:
            swap = re.compile('src=".+?docid=(.+?)&#038;hl=un"').findall(link)
        if not swap:
            swap = re.compile('src=".+?docid=(.+?)&#038;hl=en"').findall(link)
        if not swap:
            swap = re.compile('src=.+?docid=(.+?)&#038;hl=en&#038;fs=true').findall(link)
        if not swap:
            swap = re.compile("docid:'(.+?)'").findall(link)
        
        for code in swap:
            scraper.googleVideo(code, videoTitle)
    except: pass
    
    #Search for videos hosted on "megaupload"
    try:
        code=re.compile('value="http://www.megavideo.com/v/(.+?)"').findall(link)
        scraper.megaVideo(code, videoTitle)
    except: pass
    
'''
Helper method for retrieving nicely parsed HTML.

@param url: URL to the site
@return: code11/HTML code
'''
def getUrl(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8')
    response = urllib2.urlopen(req).read()
    code = re.sub('&quot;', '', response)
    code1 = re.sub('&#039;', '', code)
    code2 = re.sub('&#215;', '', code1)
    code3 = re.sub('&#038;', '', code2)
    code4 = re.sub('&#8216;', '', code3)
    code5 = re.sub('&#8217;', '', code4)
    code6 = re.sub('&#8211;', '', code5)
    code7 = re.sub('&#8220;', '', code6)
    code8 = re.sub('&#8221;', '', code7)
    code9 = re.sub('&#8212;', '', code8)
    code10 = re.sub('&amp;', '&', code9)
    code11 = re.sub("`", '', code10)
    return code11

'''
Replaces unwanted characters from the input parameter text, and returns the result.

@param text: String to be cleaned
@return: text
'''
def cleanText(text):
    text = re.sub('<em>', '[I]', text)
    text = re.sub('</em>', '[/I]', text)
    text = re.sub('&amp;', '&', text)
    text = re.sub('<br />', '', text)
    return text
