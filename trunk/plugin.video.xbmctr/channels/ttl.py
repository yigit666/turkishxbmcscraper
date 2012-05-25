# xbmctr MEDIA CENTER, is an XBMC add on that sorts and displays 
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
import mechanize
import cookielib,sys
import urllib2,urllib,re
import xbmcplugin,xbmcgui,xbmc,xbmcaddon 
import scraper, xbmctools
# -*- coding: iso-8859-9 -*-
Addon = xbmcaddon.Addon('plugin.video.xbmcTR')
profile = xbmc.translatePath(Addon.getAddonInfo('profile'))
unname='firefox'
addonSettings = xbmcaddon.Addon(id='plugin.video.xbmcTR')
__language__ = addonSettings.getLocalizedString

FILENAME = "ttl"


def main():
          uname = addonSettings.getSetting('uname')
          sitepasssword=xbmctools.namefix()
          sitepassword = addonSettings.getSetting('sitepassword')
          if (not uname or uname == '') or (not sitepassword or sitepassword == ''):
               d = xbmcgui.Dialog()
               d.ok('Kullanıcı adı yada şifre gerekiyor.','http://xbmctr.com sitemize üye olunuz.')
               addonSettings.openSettings(sys.argv[0])
               
          br = mechanize.Browser()

          cj = cookielib.LWPCookieJar()
          br.set_cookiejar(cj)

          br.set_handle_equiv(True)
          #br.set_handle_gzip(True)
          br.set_handle_redirect(True)
          br.set_handle_referer(True)
          br.set_handle_robots(False)

          br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

          br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

          br.open('http://xbmctr.com/acces/functions/login.php')

          br.select_form(nr=0)

          br.form['myusername'] = unname
          br.form['mypassword'] = sitepasssword
          br.submit()
          link = br.response().read()
          match = xbmctools.settt(link,'tt')
          for tur,videoTitle,Url,Thumbnail,info in match:
               xbmctools.addVideoLink(videoTitle,Url,Thumbnail)




