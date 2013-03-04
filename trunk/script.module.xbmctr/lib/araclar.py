# -*- coding: iso8859-9 -*-
# # xbmctr MEDIA CENTER, is an XBMC add on that sorts and displays 
# video content from several websites to the XBMC user.
#
# Copyright (C) 2011, Emin Ayhan Colak
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

# for more info please visit http://xbmctr.com


'''
Edited on 5 April 2012

@author: Dr Ayhan Colak

'''
import urllib2,urllib,re,HTMLParser,cookielib
import sys,os,base64,time
import xbmc, xbmcgui, xbmcaddon, xbmcplugin

##__settings__ = xbmcaddon.Addon(id="script.video.xbmctr")
##__language__ = __settings__.getLocalizedString
##downloadFolder = __settings__.getSetting('downloadFolder')
##home = __settings__.getAddonInfo('path')
##IMAGES_PATH = xbmc.translatePath(os.path.join(home, 'resources','images'))
##sys.path.append(IMAGES_PATH)
##SUBS_PATH = xbmc.translatePath(os.path.join(home, 'resources', 'subs'))
##sys.path.append(SUBS_PATH)


def name_prepare(videoTitle):
        print 'DUZELTME ONCESI:',videoTitle
        videoTitle=videoTitle.replace('İzle',"").replace('Türkçe',"").replace('Turkce',"").replace('Dublaj',"|TR|").replace('Altyazılı'," [ ALTYAZILI ] ").replace('izle',"").replace('Full',"").replace('720p',"").replace('HD',"")
        return videoTitle   
        
def get_url(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        print req
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty("IsPlayable", "true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok



def addDir(name,url,thumbnail,mode,filepath):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumbnail="+urllib.quote_plus(thumbnail)+"&filepath="+urllib.quote_plus(filepath)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
def hata():
        d = xbmcgui.Dialog()
        d.ok('http://xbmctr.com GIRIS HATASI !', '  Bagış yaparak Site V.I.P. bolumune','  kayit olabilir ve bu bolumu izleyebilirsiniz.')
        __settings__.openSettings()
        return False

def inside(__settings__,folders):
        filepath=os.path.join(folders,'nfo.txt')
        if check_empty_xml(filepath)== "YOK":
                cj = cookielib.CookieJar()
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                urllib2.install_opener(opener)

                login= __settings__.getSetting("login")
                if not login:
                        __settings__.openSettings()
                else:
                        pass
                login= __settings__.getSetting("login")
                password= __settings__.getSetting("password")
                req = urllib2.Request("http://forum.xbmctr.com/member.php"); #Login Page
                req.add_header('User-Agent',"Mozilla/5.0 (X11; Linux x86_64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1")

                vals = {'action' : 'do_login','url' : 'http://forum.xbmctr.com/','username' : login,'password' : password,'Submit' : 'login'}
                data = urllib.urlencode(vals)
                try:
                        opener.open(req,data).read() #Source of Login Page
                except:
                        d = xbmcgui.Dialog()
                        d.ok('http://xbmctr.com GIRIS HATASI !', '  Bagış yaparak Site V.I.P. bolumune','  kayit olabilir ve bu bolumu izleyebilirsiniz.')
                        exit()
                resp = opener.open('http://forum.xbmctr.com/manager/')
                data=resp.read()
                if "  V.I.P" in data:
                        print "Succesfully Loged in."
                else:
                        print 'Login Hata'
                        return False
        else:
                return True                

def Download_tool():        
        if downloadFolder is '':
                d = xbmcgui.Dialog()
                d.ok('Download Error','You have not set the download folder.\n Please set the addon settings and try again.','','')
                __settings__.openSettings(sys.argv[ 0 ])
        else:
                if not os.path.exists(downloadFolder):
                        print 'Download Folder Doesnt exist. Trying to create it.'
                        os.makedirs(downloadFolder)

def Download_subtitle(SUBS_PATH,videoTitle,url):
        filepath = xbmc.translatePath(os.path.join(SUBS_PATH, str(videoTitle)+'.srt'))
        def download(url, dest):
##                    dialog = xbmcgui.DialogProgress()
##                    dialog.create('Downloading Movie','From Source', filename)
                    urllib.urlretrieve(url, dest, lambda nb, bs, fs, url = url: _pbhook(nb, bs, fs, url,''))
                    print dest
        def _pbhook(numblocks, blocksize, filesize, url = None,dialog = None):
                    try:
                        
                        percent = min((numblocks * blocksize * 100) / filesize, 100)
##                        dialog.update(percent)
                    except:
                        percent = 100
##                        dialog.update(percent)
##                    if dialog.iscanceled():
##                                    dialog.close()
        download(url, filepath)
        iscanceled = True
        xbmc.executebuiltin('Notification("Subtitle","Downloaded")')
        return filepath

def Download_xml(SUBS_PATH,videoTitle,url):
        videoTitle=videoTitle.replace(" ","_")
        filepath = xbmc.translatePath(os.path.join(SUBS_PATH, str(videoTitle)+'.xml'))
        def download(url, dest):
##                    dialog = xbmcgui.DialogProgress()
##                    dialog.create('Downloading Movie','From Source', filename)
                    urllib.urlretrieve(url, dest, lambda nb, bs, fs, url = url: _pbhook(nb, bs, fs, url,''))
                    print dest
        def _pbhook(numblocks, blocksize, filesize, url = None,dialog = None):
                    try:
                        
                        percent = min((numblocks * blocksize * 100) / filesize, 100)
##                        dialog.update(percent)
                    except:
                        percent = 100
##                        dialog.update(percent)
##                    if dialog.iscanceled():
##                                    dialog.close()
        download(url, filepath)
        iscanceled = True
        xbmc.executebuiltin('Notification("Source","Downloaded")')
        return filepath

def check_time(xml):
        status=''
        if "TV" in xml:
                status="ESKI"
        else:
                if datetime.datetime.now()-datetime.datetime.fromtimestamp(os.path.getmtime(xml))> datetime.timedelta(minutes=30):
                        status="ESKI"
                else:
                        status="GUNCEL"
        return status

def check_xml_status(SUBS_PATH,name,url):
        name=name.replace(" ","_")
        xml = xbmc.translatePath(os.path.join(SUBS_PATH, str(name)+'.xml'))
        Sonuc=check_empty_xml(xml)
        if Sonuc == 'YOK':
                print 'XML YOK'
                xml=Download_xml(SUBS_PATH,name,url)
                print 'XML OLUSTURULDU'
        else:
                print 'XML BULUNDU'
                pass

        status=check_time(xml)
        print "XML DOSYA DURUMU : " +str(status)
        if status == "ESKI":
                print "xml dosya = ESKI / YENIDEN TARANIYOR."
                xml=Download_xml(SUBS_PATH,name,url)
                print 'XML YENILENDI'
                return xml
        
        elif status == "GUNCEL":
                print "VAROLAN XML OKUNUYOR:",xml
                return xml
        else:
                print 'RECENT SONUC :xml degerlendirilemedi'
        
        return xml

def check_empty_xml(xml):
        if os.path.isfile(xml):
                Sonuc='VAR'
        else:
                Sonuc='YOK'
       
        return Sonuc

