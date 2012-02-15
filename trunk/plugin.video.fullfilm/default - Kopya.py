import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon

__settings__ = xbmcaddon.Addon(id='plugin.video.filmizle')
__language__ = __settings__.getLocalizedString



            
def CATEGORIES():
        addDir(__language__(30000),'search',8,'')
        addDir(__language__(30001),'http://www.filmizle.com.tr/tur/turler',1,'')
        addDir(__language__(30002),'http://www.filmizle.com.tr/tur/yabanci-filmler',2,'')
        addDir(__language__(30003),'http://www.filmizle.com.tr/tur/yerli-filmler',3,'')
        addDir(__language__(30027),'http://www.filmizle.com.tr/tur/boxset',9,'')
        addDir(__language__(30004),'http://www.filmizle.com.tr/tur/yesilcam-filmleri-izle',4,'')
def Genre(url):
        addDir(__language__(30016),url+'/animasyon',6,'')
        addDir(__language__(30005),url+'/aile-filmleri-izle',6,'')
        addDir(__language__(30006),url+'/belgesel-filmleri-izle',6,'')
        addDir(__language__(30007),url+'/dram',6,'')
        addDir(__language__(30008),url+'/fantastik-bilim-kurgu',6,'')
        addDir(__language__(30009),url+'/gizem',6,'')
        addDir(__language__(30010),url+'/korku-gerilim',6,'')
        addDir(__language__(30011),url+'/muzik',6,'')
        addDir(__language__(30012),url+'/politik-filmler-izle',6,'')
        addDir(__language__(30013),url+'/romantik-duygusal',6,'')
        addDir(__language__(30014),url+'/seri-film-izle',6,'')
        addDir(__language__(30015),url+'/tarih-filmleri-izle',6,'') 
        addDir(__language__(30017),url+'/biyografi-filmleri-izle',6,'')
        addDir(__language__(30018),url+'/eski-filmler-izle',6,'')
        addDir(__language__(30019),url+'/genclik',6,'')
        addDir(__language__(30020),url+'/komedi',6,'')
        addDir(__language__(30021),url+'/macera-aksiyon',6,'')
        addDir(__language__(30022),url+'/polisiye-suc',6,'')
        addDir(__language__(30023),url+'/psikolojik-filmler-izle',6,'')
        addDir(__language__(30024),url+'/savas-filmleri-izle',6,'')
        addDir(__language__(30025),url+'/spor-filmleri-izle',6,'')
        addDir(__language__(30026),url+'/western',6,'')

def Boxset(url):
        addDir('Jackie Chan',url+'/jackie-chan-filmleri-izle-boxset',6,'')
        addDir('Jet li',url+'/jet-li-filmleri-izle',6,'')
        addDir('Jason Statham',url+'/jason-statham-filmleri-izle-boxset',6,'')
        addDir('Will Smith',url+'/will-smith-filmleri-izle-boxset',6,'')        
def Yabanci(url):
        addDir('2007 ve oncesi',url+'/2007-ve-oncesi',6,'')
        addDir('2008',url+'/2008',6,'')
        addDir('2009',url+'/2009',6,'')
        addDir('2010',url+'/2010',6,'')
        addDir('2011',url+'/2011-yabanci-film-izle',6,'')
        addDir('2012',url+'/2012-yapimi-filmler',6,'')
def Yerli(url):
        addDir('2007 ve oncesi',url+'/2007-ve-oncesi',6,'')
        addDir('2008',url+'/2008',6,'')
        addDir('2009',url+'/2009',6,'')
        addDir('2010',url+'/2010-yerli-filmler',6,'')
        addDir('2011',url+'/2011-yapimi-yerli-filmler',6,'')
def Yesilcam(url):
        addDir('Adile Nasit',url+'/adile-nasit-filmleri-izle',6,'')
        addDir('Fatma Girik',url+'/fatma-girik-filmleri-izle',6,'')
        addDir('Kadir Inanir',url+'/kadir-inanir-filmleri-izle',6,'')
        addDir('Mujde Ar',url+'/mujde-ar-filmleri-izle',6,'')
        addDir('Sener Sen',url+'/sener-sen-filmleri-izle',6,'')
        addDir('Turkan Soray',url+'/turkan-soray-filmleri-izle',6,'')
        addDir('Cuneyt Arkin',url+'/cuneyt-arkin-filmleri-izle',6,'')
        addDir('Filiz Akin',url+'/filiz-akin-filmleri-izle',6,'')
        addDir('Kemal Sunal',url+'/kemal-sunal-filmleri-izle',6,'')
        addDir('Orhan Gencebay',url+'/orhan-gencebay-filmleri-izle',6,'')
        addDir('Tarik Akan',url+'/tarik-akan-filmleri-izle',6,'')
        addDir('Tarik Akan',url+'/tarik-akan-filmleri-izle',6,'')

def search():
        keyboard = xbmc.Keyboard("", 'Search', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText()
            #print query
            url = ('http://www.filmizle.com.tr/index.php?s='+ query )
            #print url
            Movie(url)
def Movie(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xc3\xbc',"u").replace('&amp;',"&").replace('\xc4\xb1',"i").replace('&#039;',"'").replace('\xc5\x9e',"S").replace('\xc3\xa7',"c").replace('\xc3\xb6',"o").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()        
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
        match=re.compile('<a href=".*? - (.*?)" target="_blank"><img src="http://www.filmizle.com.tr/wp-content/themes/film/images/ktwitter.png" alt="" /></a>\n</div>\n</div>\n\n<div class="film-arka">\n<div class="filmortala">\n<div class=".*?"></div>\n<p><img src="(.*?)" alt="" title="(.*?)"').findall(link)
        for url,thumbnail,name in match:
                addDir(name,url,7,thumbnail)

def playList(url):
        ok = True
        url= url +':;'+url+'/2:;' +url+'/3:;' +url+'/4:;'+url+'/5:;'
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
        pDialog = xbmcgui.DialogProgress()
        ret = pDialog.create('Loading playlist...')
        links = url.split(':;')
        del links [5]
        totalLinks = len(links)
        loadedLinks = 0
        remaining_display = 'XBMC Film listesine  :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B] yuklendi..'
        pDialog.update(0,__language__(30030),remaining_display)
        a=0
        for url in links:
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<param name="movie" value="http://www.filmizle.com.tr/poisplayer/mediaplayer.swf\?file=(.*?)\&autostart').findall(link)
                for partLink in match:
                        name='Part'
                        a=a+1
                        name= name+' '+str(a)
                        addLink(name,partLink,'')
                        playList.add(partLink)
                        loadedLinks = loadedLinks + 1
                        percent = (loadedLinks * 100)/totalLinks
                        remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B] into XBMC player playlist.'
                        pDialog.update(percent,'Please wait for the process to retrieve video link.',remaining_display)
                        if (pDialog.iscanceled()):
                                return False

        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playList)
        if not xbmcPlayer.isPlayingVideo():
                d = xbmcgui.Dialog()
                d.ok('Video Yok', 'Calamiyorum','Geri don.')
        return ok
        
def Download(url):
       filename = (name+'.mp4')
       downloadFolder = __settings__.getSetting('downloadFolder')
       print downloadFolder
       if downloadFolder is '':
                d = xbmcgui.Dialog()
                d.ok('Download Error','You have not set the download folder.\n Please set the addon settings and try again.','','')
                __settings__.openSettings(sys.argv[ 0 ])
       else:
                if not os.path.exists(downloadFolder):
                        print 'Download Folder Doesnt exist. Trying to create it.'
                        os.makedirs(downloadFolder)

                def download(url, dest):
                                dialog = xbmcgui.DialogProgress()
                                dialog.create('Downloading Movie','From Source', filename)
                                urllib.urlretrieve(url, dest, lambda nb, bs, fs, url = url: _pbhook(nb, bs, fs, url, dialog))
                def _pbhook(numblocks, blocksize, filesize, url = None,dialog = None):
                                try:
                                                percent = min((numblocks * blocksize * 100) / filesize, 100)
                                                dialog.update(percent)
                                except:
                                                percent = 100
                                                dialog.update(percent)
                                if dialog.iscanceled():
                                                dialog.close()
                if (__settings__.getSetting('downloadFolder') == ''):
                                __settings__.openSettings('downloadFolder')
                filepath = xbmc.translatePath(os.path.join(__settings__.getSetting('downloadFolder'),filename))
                download(url, filepath)
                iscanceled = True
                xbmc.executebuiltin('Notification("Diziport","Select&Download")')
                
def MAINMENU(url):
        addDir(__language__(30002),'http://www.filmizle.com.tr/','','special://home/addons/plugin.video.filmizle/resources/images/main.jpg')
        
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param



def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.Player().play(liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
elif mode==1:
        print ""+url
        Genre(url)
elif mode==2:
        print ""+url
        Yabanci(url)
elif mode==3:
        print ""+url
        Yerli(url)
elif mode==4:
        print ""+url
        Yesilcam(url)
elif mode==5:
        print ""+url
        adres(url)
elif mode==6:
        print ""+url
        Movie(url)
elif mode==7:
        print ""+url
        playList(url)
elif mode==8:
        print ""+url
        search()
elif mode==9:
        print ""+url
        Boxset(url)




xbmcplugin.endOfDirectory(int(sys.argv[1]))
