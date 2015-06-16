from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.MenuList import MenuList
from Components.Sources.List import List
from Components.Pixmap import MultiPixmap
from Components.About import about
from Tools.Directories import fileExists
from ServiceReference import ServiceReference
from os import system, listdir, remove as os_remove
from enigma import iServiceInformation, eTimer
import socket

from xml.dom import Node
from xml.dom import minidom
from Screens.Console import Console
import urllib

class DeliteBluePanel(Screen):
	skin = """
	<screen name="DeliteBluePanel" position="center,center" size="1000,720"  title="Black Hole Blue Panel" flags="wfNoBorder">
        <ePixmap position="339,170" zPosition="3" size="60,40" pixmap="skin_default/buttons/key_ok.png" alphatest="blend" transparent="1" />
        <eLabel text="Black Hole Blue Panel" position="80,30" size="800,38" font="Regular;34" halign="left" transparent="1"/> 
        <widget name="lab1" position="129,90" size="230,25" font="Regular;24" zPosition="2"  transparent="1"/>
        <widget name="list" position="75,126" size="340,38" zPosition="2"  transparent="1"/> 
        <widget name="lab2" position="139,172" size="190,24" font="Regular;20" halign="center" valign="center" zPosition="2" transparent="1"/>
    	<widget name="lab3" position="79,201" size="120,28" font="Regular;24" halign="left" zPosition="2" transparent="1"/> 
        <widget name="activecam" position="79,201" size="350,28" font="Regular;24" halign="left" zPosition="2" transparent="1"/>
        <widget name="Ilab1" position="79,257" size="350,28" font="Regular;24" zPosition="2" transparent="1"/>
        <widget name="Ilab2" position="79,290" size="350,28" font="Regular;24" zPosition="2" transparent="1"/>
        <widget name="Ilab3" position="79,315" size="350,28" font="Regular;24" zPosition="2" transparent="1"/>
        <widget name="Ilab4" position="79,345" size="350,28" font="Regular;24" zPosition="2" transparent="1"/>
        <widget name="Ecmtext" position="79,380" size="440,300" font="Regular;20" zPosition="2" transparent="1"/>
        <ePixmap position="145,650" size="140,40" pixmap="skin_default/buttons/red.png" alphatest="on" zPosition="1" />
        <ePixmap position="430,650" size="140,40" pixmap="skin_default/buttons/yellow.png" alphatest="on" zPosition="1" />
        <ePixmap position="715,650" size="140,40" pixmap="skin_default/buttons/blue.png" alphatest="on" zPosition="1" />
		<widget name="key_red" position="145,650" zPosition="2" size="140,40" font="Regular;24" halign="center" valign="center" backgroundColor="red" transparent="1" />		
		<widget name="key_yellow" position="430,650" zPosition="2" size="140,40" font="Regular;24" halign="center" valign="center" backgroundColor="yellow" transparent="1" />
		<widget name="key_blue" position="715,650" zPosition="2" size="140,40" font="Regular;24" halign="center" valign="center" backgroundColor="blue" transparent="1" />
    </screen>"""
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["lab1"] = Label()
		self["lab2"] = Label(_("Set Default CAM"))
		self["lab3"] = Label()
		self["Ilab1"] = Label()
		self["Ilab2"] = Label()
		self["Ilab3"] = Label()
		self["Ilab4"] = Label()
		self["key_red"] = Label(_("Epg Panel"))
		self["key_green"] = Label(_("Download CAM"))
		self["key_yellow"] = Label(_("Sys Info"))
		self["key_blue"] = Label(_("Extra Settings"))
		self["activecam"] = Label()
		self["Ecmtext"] = ScrollLabel()
		
		self["actions"] = ActionMap(["ColorActions", "OkCancelActions", "DirectionActions"],
		{
			"ok": self.keyOk,
			"cancel": self.close,
			"green": self.keyGreen,
			"red": self.keyRed,
			"yellow": self.keyYellow,
			"blue": self.keyBlue,
			"up": self["Ecmtext"].pageUp,
			"down": self["Ecmtext"].pageDown
		}, -1)
		
#		if not fileExists("/usr/lib/libcrypto.so.0.9.7"):
#			system("ln -s /lib/libcrypto.so.0.9.8 /usr/lib/libcrypto.so.0.9.7")
#			system("ln -s /lib/libcrypto.so.0.9.8 /lib/libcrypto.so.0.9.7")
		self.emlist = []
		self.populate_List()
		self["list"] = MenuList(self.emlist)
		self["lab1"].setText(_("%d  CAMs Installed") % (len(self.emlist)))
		
		self.timer = eTimer()
		self.timer.callback.append(self.downloadxmlpage)
		self.timer.start(100, 1)
		self.addon = 'emu'
		self.icount = 0
		self.downloading = False
        
		self.onShow.append(self.updateBP)

	def populate_List(self):
		self.camnames = {}
		cams = listdir("/usr/camscript")
		for fil in cams:
			if fil.find('Ncam_') != -1:
				f = open("/usr/camscript/" + fil,'r')
				for line in f.readlines():
					line = line.strip()
					if line.find('CAMNAME=') != -1:
						name = line[9:-1]
						self.emlist.append(name)
						self.camnames[name] = "/usr/camscript/" + fil
				f.close()

	def updateBP(self):
		try:
			name = ServiceReference(self.session.nav.getCurrentlyPlayingServiceReference()).getServiceName()
			sinfo = self.session.nav.getCurrentService().info()
			provider = self.getServiceInfoValue(iServiceInformation.sProvider, sinfo)
			wide = self.getServiceInfoValue(iServiceInformation.sAspect, sinfo)
			width = sinfo and sinfo.getInfo(iServiceInformation.sVideoWidth) or -1
			height = sinfo and sinfo.getInfo(iServiceInformation.sVideoHeight) or -1	
			videosize = "%dx%d" %(width, height)
			aspect = "16:9" 
			if aspect in ( 1, 2, 5, 6, 9, 0xA, 0xD, 0xE ):
				aspect = "4:3"
		except:
			name = "N/A"; provider = "N/A"; aspect = "N/A"; videosize  = "N/A"	
		
		self["Ilab1"].setText(_("Name: ") + name)
		self["Ilab2"].setText(_("Provider: ") + provider)
		self["Ilab3"].setText(_("Aspect Ratio: ") + aspect)
		self["Ilab4"].setText(_("Videosize: ") + videosize)
	
		self.defaultcam = "/usr/camscript/Ncam_Ci.sh"
		if fileExists("/etc/BhCamConf"):
			f = open("/etc/BhCamConf",'r')
			for line in f.readlines():
   				parts = line.strip().split("|")
				if parts[0] == "deldefault":
					self.defaultcam = parts[1]
			f.close()
			
		self.defCamname =  "Common Interface"	
		for c in self.camnames.keys():
			if self.camnames[c] == self.defaultcam:
				self.defCamname = c
		pos = 0
		for x in self.emlist:
			if x == self.defCamname:
				self["list"].moveToIndex(pos)
				break
			pos += 1

		mytext = "";
		if fileExists("/tmp/ecm.info"):
			f = open("/tmp/ecm.info",'r')
 			for line in f.readlines():
				mytext = mytext + line.strip() + "\n"
 			f.close()
		if len(mytext) < 5:
			mytext = "\n\n    " + _("Ecm Info not available.")
				
		self["activecam"].setText(self.defCamname)
		self["Ecmtext"].setText(mytext)


	def getServiceInfoValue(self, what, myserviceinfo):
		v = myserviceinfo.getInfo(what)
		if v == -2:
			v = myserviceinfo.getInfoString(what)
		elif v == -1:
			v = "N/A"
		return v


	def keyOk(self):
		self.sel = self["list"].getCurrent()
		self.newcam = self.camnames[self.sel]
		
		out = open("/etc/BhCamConf",'w')
		out.write("deldefault|" + self.newcam + "\n")
		out.close()
		
		out = open("/etc/CurrentBhCamName", "w")
		out.write(self.sel)
		out.close()
		cmd = "cp -f " + self.newcam + " /usr/bin/StartBhCam"
		system (cmd)
		cmd = "STOP_CAMD," + self.defaultcam
		self.sendtoBh_sock(cmd)
		
		cmd = "NEW_CAMD," + self.newcam
		self.sendtoBh_sock(cmd)
		oldcam = self.camnames[self.sel]
		self.session.openWithCallback(self.myclose, Nab_DoStartCam, self.sel)
		
		
	def sendtoBh_sock(self, data):
		client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		client_socket.connect("/tmp/Blackhole.socket")
		client_socket.send(data)
            	client_socket.close()
				
	def keyYellow(self):
		self.session.open(BhsysInfo)

	def keyBlue(self):
		from Screens.BpSet import DeliteSettings
		self.session.open(DeliteSettings)
		
	
	def downloadxmlpage(self):
		from twisted.web.client import getPage
		url = 'http://vuplus-images.co.uk/panel/addonslist.xml'
		getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

	def errorLoad(self, error):
		print str(error)

	def _gotPageLoad(self, data):
		self.xml = data
		try:
			if self.xml:
				xmlstr = minidom.parseString(self.xml)
				self.data = []
				self.names = []
				icount = 0
				list = []
				xmlparse = xmlstr
				self.xmlparse = xmlstr
				for plugins in xmlstr.getElementsByTagName('plugins'):
					self.names.append(plugins.getAttribute('cont').encode('utf8'))

				self.list = list
				self.downloading = True
			else:
				self.downloading = False
				return
		except:
			self.downloading = False

	def keyGreen(self):
		if self.downloading == True:
			try:
				self.session.openWithCallback(self.populate_List, IpkgPackages, self.xmlparse, " Cams - BlackHole 2.x.x ")
			except:
				self.close()
		
	def keyRed(self):
		from Plugins.SystemPlugins.CrossEPG.crossepg_main import crossepg_main
		crossepg_main.setup(self.session)

	def myclose(self):
		self.close()

class IpkgPackages(Screen):
	skin = '\n\t<screen position="center,center" size="900,720" title="Download BLACKHOLE SOFTCAMS" >\n\t\t<widget name="countrymenu" position="10,0" size="800,660" scrollbarMode="showOnDemand" />\n\t\t<ePixmap name="red" position="5,780" zPosition="4" size="540,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />\n\t\t<widget name="key_red" position="5,660" zPosition="5" size="120,60" valign="center" halign="center" font="Regular;28" transparent="1" foregroundColor="red" shadowColor="black" shadowOffset="-1,-1" />\n\t</screen>'

	def __init__(self, session, xmlparse, selection):
		Screen.__init__(self, session)
		self.xmlparse = xmlparse
		self.selection = selection
		list = []
		for plugins in self.xmlparse.getElementsByTagName('plugins'):
			if str(plugins.getAttribute('cont').encode('utf8')) == self.selection:
				for plugin in plugins.getElementsByTagName('plugin'):
					list.append(plugin.getAttribute('name').encode('utf8'))
			continue

		list.sort()
		self['countrymenu'] = MenuList(list)
		self['actions'] = ActionMap(['SetupActions'], {'cancel': self.close,
		'ok': self.selclicked}, -2)
		self['key_red'] = Button(_('Back'))

	def selclicked(self):
		try:
			selection_country = self['countrymenu'].getCurrent()
		except:
			return
		for plugins in self.xmlparse.getElementsByTagName('plugins'):
			if str(plugins.getAttribute('cont').encode('utf8')) == self.selection:
				for plugin in plugins.getElementsByTagName('plugin'):
					if plugin.getAttribute('name').encode('utf8') == selection_country:
						urlserver = str(plugin.getElementsByTagName('url')[0].childNodes[0].data)
						pluginname = plugin.getAttribute('name').encode('utf8')
						self.prombt(urlserver, pluginname)
						continue
			continue

	def prombt(self, com, dom):
		self.com = com
		self.dom = dom
		if self.selection == '{ Skins }':
			self.session.openWithCallback(self.callMyMsg, MessageBox, _('Do not install any skin unless you are sure it is compatible with your image.Are you sure?'), MessageBox.TYPE_YESNO)
		else:
			self.session.open(Console, _('Installing: %s') % dom, ['opkg install -force-overwrite %s' % com])

	def callMyMsg(self, result):
		if result:
			dom = self.dom
			com = self.com
			self.session.open(Console, _('Installing: %s') % dom, ['ipkg install -force-overwrite %s' % com])
            
class Nab_DoStartCam(Screen):
	skin = """
	<screen position="390,100" size="484,250" title="Black Hole" flags="wfNoBorder">
		<widget name="connect" position="0,0" size="484,250" zPosition="-1" pixmaps="skin_default/startcam_1.png,skin_default/startcam_2.png,skin_default/startcam_3.png,skin_default/startcam_4.png" transparent="1" />
		<widget name="lab1" position="10,180" halign="center" size="460,60" zPosition="1" font="Regular;20" valign="top" transparent="1" />
	</screen>"""
	
	def __init__(self, session, title):
		Screen.__init__(self, session)
		
		msg = _("Please wait while starting\n") + title + "..."
		self["connect"] = MultiPixmap()
		self["lab1"] = Label(msg)

		self.activityTimer = eTimer()
		self.activityTimer.timeout.get().append(self.updatepix)
		self.onShow.append(self.startShow)
		self.onClose.append(self.delTimer)
		
	def startShow(self):
		self.curpix = 0
		self.count = 0
		self["connect"].setPixmapNum(0)
		self.activityTimer.start(10)

	def updatepix(self):
		self.activityTimer.stop()
		if self.curpix > 2:
			self.curpix = 0
		#if self.count == 0:
			
		if self.count > 7:
			self.curpix = 3
		self["connect"].setPixmapNum(self.curpix)
		if self.count == 20:
			self.hide()
			
			#ref = self.session.nav.getCurrentlyPlayingServiceReference()
			#self.session.nav.playService(ref)
			self.close()
		
		self.activityTimer.start(140)
		self.curpix += 1
		self.count += 1
		
	def delTimer(self):
		del self.activityTimer

class BhsysInfo(Screen):
	skin = """
	<screen position="center,center" size="800,600" title="Black Hole Info" flags="wfNoBorder">
		<widget name="lab1" position="50,25" halign="left" size="700,550" zPosition="1" font="Regular;20" valign="top" transparent="1" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		self["lab1"] =  ScrollLabel()

		self.onShow.append(self.updateInfo)
		
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions"],
		{
			"ok": self.close,
			"cancel": self.close,
			"up": self["lab1"].pageUp,
			"down": self["lab1"].pageDown
		}, -1)
		
	def updateInfo(self):
		rc = system("df -h > /tmp/syinfo.tmp")
		text = _("BOX\n") + _("Brand:") + "\tMiraclebox\n"
	
		hwname = "Unknown"
		if about.getHardwareTypeString() == "ini-8000sv":
		    hwname = "MB Premium Ultra HD"
		elif about.getHardwareTypeString() == "ini-5000sv":
		    hwname = "MB Premium Twin HD"
		elif about.getHardwareTypeString() == "ini-2000sv":
		    hwname = "MB Premium Mini+ PLUS HD"
		elif about.getHardwareTypeString() == "ini-1000sv":
		    hwname = "MB Premium Mini HD"

 		text += _("Model:\t") + hwname +"\n"
		f = open("/proc/stb/info/chipset",'r')
 		text += _("Chipset:\t") + f.readline() +"\n"
 		f.close()
		text += _("MEMORY\n")
		memTotal = memFree = swapTotal = swapFree = 0
		for line in open("/proc/meminfo",'r'):
			parts = line.split(':')
			key = parts[0].strip()
			if key == "MemTotal":
				memTotal = parts[1].strip()
			elif key in ("MemFree", "Buffers", "Cached"):
				memFree += int(parts[1].strip().split(' ',1)[0])
			elif key == "SwapTotal":
				swapTotal = parts[1].strip()
			elif key == "SwapFree":
				swapFree = parts[1].strip()
		text += _("Total memory:") + "\t%s\n" % memTotal
		text += _("Free memory:") + "\t%s kB\n"  % memFree
		text += _("Swap total:") + "\t%s \n"  % swapTotal
		text += _("Swap free:") + "\t%s \n"  % swapFree
		text += "\n" + _("STORAGE") + "\n"
		f = open("/tmp/syinfo.tmp",'r')
		line = f.readline()
		parts = line.split()
		text += parts[0] + "\t" + parts[1].strip() + "      " + parts[2].strip() + "    " + parts[3].strip() + "    " + parts[4] + "\n"
		line = f.readline()
		parts = line.split()
		text += _("Flash") + "\t" + parts[1].strip() + "  " + parts[2].strip()  + "  " +  parts[3].strip()  + "  " +  parts[4] + "\n"
 		for line in f.readlines():
			if line.find('/media/') != -1:
				line = line.replace('/media/', '   ')
				parts = line.split()
				if len(parts) == 6:
					text += parts[5] + "\t" + parts[1].strip() + "  " + parts[2].strip() + "  " + parts[3].strip() + "  " + parts[4] + "\n"
		f.close()
		os_remove("/tmp/syinfo.tmp")
		
		text += "\n" + _("SOFTWARE") + "\n"
		f = open("/etc/bpversion",'r')
		text += "Firmware v.:\t" + f.readline()
		f.close()
		text += "Enigma2 v.: \t" +  about.getEnigmaVersionString() + "\n"
		text += "Kernel v.: \t" +  about.getKernelVersionString() + "\n"
		
		self["lab1"].setText(text)
		



class DeliteBp:
	def __init__(self):
		self["DeliteBp"] = ActionMap( [ "InfobarExtensions" ],
			{
				"DeliteBpshow": (self.showDeliteBp),
			})

	def showDeliteBp(self):
		self.session.openWithCallback(self.callNabAction, DeliteBluePanel)

	def callNabAction(self, *args):
		if len(args):
			(actionmap, context, action) = args
			actionmap.action(context, action)