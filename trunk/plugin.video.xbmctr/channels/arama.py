import urllib,urllib2,re,sys
import xbmcplugin,xbmcgui,xbmcaddon,xbmc
import scraper, xbmctools

# -*- coding: iso-8859-9 -*-
Addon = xbmcaddon.Addon('plugin.video.xbmctr')
__settings__ = xbmcaddon.Addon(id='plugin.video.xbmctr')
__language__ = __settings__.getLocalizedString


FILENAME = "arama"


def main():
        keyboard = xbmc.Keyboard("", 'Search', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText()
            query=query.replace(' ','+')
            print query


        dialog = xbmcgui.Dialog()
        ret = dialog.select(__language__(30047), [__language__(30048), __language__(30049)])
        if ret == 0:
                        
                    try:
                           
                           url = ('http://diziport.com/index.php?eleman=' + query + '&bolum=dizi&obje=diziler&olay=arama')
                           link=xbmctools.get_url(url)
                           match=re.compile('<li><img src="(.*?)\?hash=123" alt=".*?" width="113" height="113" />\n<a href="(.*?)" title="(.*?)">').findall(link)
                           if len(match)>1:
                                   xbmctools.addFolder(FILENAME,'--------DiziPort--------' ,"",'','')
                                   for thumbnail,url,videoTitle in match:
                                           xbmctools.addFolder("diziport",videoTitle,"Session(url)",'http://diziport.com/'+url,'http://diziport.com/'+thumbnail)
                    except:
                           pass


                    try:
                           
                           url = ('http://www.dizihd.com/?s='+ query +'&x=0&y=0')
                           link=xbmctools.get_url(url)      
                           match=re.compile('<a href="(.+?)"><img src="(.+?)" ></a>\r\n\t\t\t\t\t\t<h2><a href=".+?">(.+?)izle.*?</a>').findall(link)
                           if len(match)>1:
                                   xbmctools.addFolder(FILENAME,'--------Dizi HD--------' ,"",'','')
                                   for url,thumbnail,videoTitle in match:
                                           xbmctools.addFolder("scraper",videoTitle,"prepare_list(videoTitle,url)",url,thumbnail)
                    except:
                            pass



        if ret == 1:
                
            try:
                Url = ('http://www.filmifullizle.com/index.php?s=' + query)
                print Url
                link=xbmctools.get_url(Url)
                match=re.compile('<div style="float: left;">\n<a href="(.*?)"><img src="(.*?)" alt="(.*?)"').findall(link)
                print match
                if len(match)>1:
                        xbmctools.addFolder(FILENAME,'--------Sinema HD--------' ,"",'','')
                        for url,thumbnail,videoTitle in match:
                                xbmctools.addFolder("scraper",videoTitle, "prepare_list(videoTitle,url)",url,thumbnail)
                                
                    
            except:
                print 'okumadı'
