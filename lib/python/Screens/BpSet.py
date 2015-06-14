from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.Pixmap import Pixmap
from Components.ConfigList import ConfigListScreen
from Components.config import getConfigListEntry, config, ConfigYesNo, ConfigText, ConfigSelection, ConfigClock, ConfigNumber, NoSave
from Components.Sources.List import List
from Components.Network import iNetwork
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, pathExists, resolveFilename, SCOPE_CURRENT_SKIN
from os import system, remove as os_remove, rename as os_rename, popen, getcwd, chdir
from Screens.Setup import Setup
from Plugins.SystemPlugins.NetworkBrowser.NetworkBrowser import NetworkBrowser
from Plugins.SystemPlugins.SoftwareManager.BackupRestore import BackupScreen



class DeliteSettings(Screen):
	skin = """
	<screen position="160,110" size="390,360" title="Black Hole Extra Settings">
		<widget source="list" render="Listbox" position="10,10" size="370,330" scrollbarMode="showOnDemand" >
			<convert type="TemplatedMultiContent">
                		{"template": [
                		MultiContentEntryText(pos = (60, 1), size = (300, 36), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
                		MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (36, 36), png = 1),
                		],
                		"fonts": [gFont("Regular", 24)],
                		"itemHeight": 36
                		}
            		</convert>
		</widget>
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self.list = []
		self["list"] = List(self.list)
		self.updateList()
		
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.KeyOk,
			"back": self.close

		})
		
	def KeyOk(self):
		self.sel = self["list"].getCurrent()
		self.sel = self.sel[2]
		
		if self.sel == 0:
			from Screens.BpDevice import DeliteDevicesPanel
			self.session.open(DeliteDevicesPanel)
		elif self.sel == 1:
			self.session.open(Setup, "usage")
		elif self.sel == 2:
			self.session.open(Setup, "userinterface")
		elif self.sel == 3:
			from Plugins.SystemPlugins.OSDPositionSetup.plugin import OSDScreenPosition
			self.session.open(OSDScreenPosition)
		elif self.sel == 4:
			from Plugins.SystemPlugins.OSD3DSetup.plugin import OSD3DSetupScreen
			self.session.open(OSD3DSetupScreen)
		elif self.sel == 5:
			from Screens.BpFormat import Bp_UsbFormat
			self.session.open(Bp_UsbFormat)
		elif self.sel == 6:
			from Screens.BpDevice import BlackPoleSwap
			self.session.open(BlackPoleSwap)
		elif self.sel == 7:
			self.session.open(DeliteInadyn)
		elif self.sel == 8:
			from Plugins.Extensions.DLNABrowser.plugin import DLNADeviceBrowser
			self.session.open(DLNADeviceBrowser)
		elif self.sel == 9:
			from Plugins.Extensions.DLNAServer.plugin import DLNAServer
			self.session.open(DLNAServer)
		elif self.sel == 10:
			self.session.open(DeliteOpenvpn)
		elif self.sel == 11:
			self.session.open(Setup, "epgsettings")
		elif self.sel == 12:
			self.session.open(Setup, "recording")
		elif self.sel == 13:
			from Screens.RecordPaths import RecordPathsSettings
			self.session.open(RecordPathsSettings)
		elif self.sel == 14:
			self.session.open(Setup, "subtitlesetup")
		elif self.sel == 15:
			self.session.open(Setup, "autolanguagesetup")
		elif self.sel == 16:
			self.session.open(BhNetBrowser)
		
		else:
			self.noYet()
		
	def noYet(self):
		nobox = self.session.open(MessageBox, _("Function Not Yet Available"), MessageBox.TYPE_INFO)
		nobox.setTitle(_("Info"))
	
		
	def updateList(self):
		self.list = [ ]
		mypath = resolveFilename(SCOPE_CURRENT_SKIN, "")
		if mypath == "/usr/share/enigma2/" or mypath == "/usr/share/enigma2/./":
			mypath = "/usr/share/enigma2/skin_default/"
		
		mypixmap = mypath + "icons/infopanel_space.png"
		png = LoadPixmap(mypixmap)
		name = _("Devices Manager")
		idx = 0
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_osd.png"
		png = LoadPixmap(mypixmap)
		name = _("General settings")
		idx = 1
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_osd.png"
		png = LoadPixmap(mypixmap)
		name = _("Osd settings")
		idx = 2
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_osd.png"
		png = LoadPixmap(mypixmap)
		name = _("Osd Position setup")
		idx = 3
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_osd.png"
		png = LoadPixmap(mypixmap)
		name = _("Osd 3D setup")
		idx = 4
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_space.png"
		png = LoadPixmap(mypixmap)
		name = _("Usb Format Wizard")
		idx = 5
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/swapsettings.png"
		png = LoadPixmap(mypixmap)
		name = _("Swap File settings")
		idx = 6
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/inadynsettings.png"
		png = LoadPixmap(mypixmap)
		name = _("Inadyn")
		idx = 7
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_samba.png"
		png = LoadPixmap(mypixmap)
		name = _("Dlna Client")
		idx = 8
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_samba.png"
		png = LoadPixmap(mypixmap)
		name = _("Dlna Server")
		idx = 9
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_samba.png"
		png = LoadPixmap(mypixmap)
		name = _("OpenVpn Panel")
		idx = 10
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_samba.png"
		png = LoadPixmap(mypixmap)
		name = _("Internal Epg settings")
		idx = 11
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_cron.png"
		png = LoadPixmap(mypixmap)
		name = _("Record settings")
		idx = 12
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_space.png"
		png = LoadPixmap(mypixmap)
		name = _("Recording paths")
		idx = 13
		res = (name, png, idx)
		self.list.append(res)
				
		mypixmap = mypath + "icons/infopanel_kmod.png"
		png = LoadPixmap(mypixmap)
		name = _("Subtitle settings")
		idx = 14
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/inadynsettings.png"
		png = LoadPixmap(mypixmap)
		name = _("Auto language settings")
		idx = 15
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/mountwizard.png"
		png = LoadPixmap(mypixmap)
		name = _("Network Browser & Mountpoints")
		idx = 16
		res = (name, png, idx)
		self.list.append(res)
		
		
		self["list"].list = self.list
		
		

class BhNetBrowser(Screen):
	skin = """
	<screen position="center,center" size="800,520" title="Select Network Interface">
		<widget source="list" render="Listbox" position="10,10" size="780,460" scrollbarMode="showOnDemand" >
			<convert type="StringList" />
		</widget>
    		<ePixmap pixmap="skin_default/buttons/red.png" position="200,480" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/yellow.png" position="440,480" size="140,40" alphatest="on" />
		<widget name="key_red" position="200,480" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<widget name="key_yellow" position="440,480" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
    	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["key_red"] = Label(_("Select"))
		self["key_yellow"] = Label(_("Close"))
		
		self.list = []
		self["list"] = List(self.list)
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.selectInte,
			"back": self.close,
			"red": self.selectInte,
			"yellow": self.close
		})
		
		self.list = [ ]
		self.adapters = [(iNetwork.getFriendlyAdapterName(x),x) for x in iNetwork.getAdapterList()]
		for x in self.adapters:
			res = (x[0], x[1])
			self.list.append(res)

		self["list"].list = self.list
		
	def selectInte(self):
		mysel = self["list"].getCurrent()
		if mysel:
			inter = mysel[1]
			self.session.open(NetworkBrowser, inter, "/usr/lib/enigma2/python/Plugins/SystemPlugins/NetworkBrowser")


class BhMinidlna(Screen):
	skin = """
	<screen position="center,center" size="602,405" title="Black Hole UPnP Minidlna Server Panel">
		<widget name="lab1" position="20,20" size="580,260" font="Regular;20" valign="center" transparent="1"/>
		<widget name="lab2" position="20,300" size="300,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labstop" position="320,300" size="150,30" font="Regular;20" valign="center" halign="center" backgroundColor="red"/>
		<widget name="labrun" position="320,300" size="150,30" zPosition="1" font="Regular;20" valign="center" halign="center" backgroundColor="green"/>
		<ePixmap pixmap="skin_default/buttons/red.png" position="125,360" size="150,30" alphatest="on"/>
		<ePixmap pixmap="skin_default/buttons/green.png" position="325,360" size="150,30" alphatest="on"/>
		<widget name="key_red" position="125,362" zPosition="1" size="150,25" font="Regular;20" halign="center" backgroundColor="transpBlack" transparent="1"/>
		<widget name="key_green" position="325,362" zPosition="1" size="150,25" font="Regular;20" halign="center" backgroundColor="transpBlack" transparent="1"/>
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		mytext = _("Minidlna: UPnP media server Black Hole version.\nMinidlna is fully configured for your box and ready to work. Just enable it and play.\nMinidlna include little web interface.\n\nMinidlna webif url: http://ip_box:8200\nMinidlna config: /etc/minidlna.conf\nMinidlna home site: http://sourceforge.net/projects/minidlna/")
		self["lab1"] = Label(mytext)
		self["lab2"] = Label(_("Current Status:"))
		self["labstop"] = Label(_("Stopped"))
		self["labrun"] = Label(_("Running"))
		self["key_red"] = Label(_("Enable"))
		self["key_green"] = Label(_("Disable"))
		self.my_serv_active = False
				
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.close,
			"back": self.close,
			"red": self.ServStart,
			"green": self.ServStop
		})
		
		self.onLayoutFinish.append(self.updateServ)

	def ServStart(self):
		if self.my_serv_active == True:
			self.session.open(MessageBox, _("Minidlna already up and running."), MessageBox.TYPE_INFO)
		else:
			rc = system("ln -s ../init.d/minidlna /etc/rc3.d/S90minidlna")
			rc = system("/etc/init.d/minidlna start")
			mybox = self.session.open(MessageBox, "Minidlna Server Enabled.", MessageBox.TYPE_INFO)
			mybox.setTitle("Info")
			self.updateServ()
			
		
	def ServStop(self):
		if self.my_serv_active == True:
			rc = system("/etc/init.d/minidlna stop")
			if fileExists("/etc/rc3.d/S90minidlna"):
				os_remove("/etc/rc3.d/S90minidlna")
				
			mybox = self.session.open(MessageBox, _("Minidlna Server Disabled."), MessageBox.TYPE_INFO)
			mybox.setTitle(_("Info"))
			rc = system("sleep 1")
			self.updateServ()
		

	def updateServ(self):
		self["labrun"].hide()
		self["labstop"].hide()
		rc = system("ps > /tmp/nvpn.tmp")
		self.my_serv_active = False
		
		if fileExists("/tmp/nvpn.tmp"):
			f = open("/tmp/nvpn.tmp",'r')
 			for line in f.readlines():
				if line.find('minidlna') != -1:
					self.my_serv_active = True
			f.close()
			os_remove("/tmp/nvpn.tmp")
		
			
		if self.my_serv_active == True:
			self["labstop"].hide()
			self["labrun"].show()
		else:
			self["labstop"].show()
			self["labrun"].hide()
			
			
class DeliteInadyn(Screen):
	skin = """
	<screen position="120,70" size="480,410" title="Black Hole E2 Inadyn Manager">
		<widget name="linactive" position="10,10" zPosition="1" pixmap="skin_default/icons/ninactive.png" size="32,32"  alphatest="on" />
		<widget name="lactive" position="10,10" zPosition="2" pixmap="skin_default/icons/nactive.png" size="32,32"  alphatest="on" />
		<widget name="lab1" position="50,10" size="350,30" font="Regular;20" valign="center"  transparent="1"/>
		<widget name="lab2" position="10,50" size="230,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labtime" position="240,50" size="100,30" font="Regular;20" valign="center" backgroundColor="#4D5375"/>
		<widget name="lab3" position="10,100" size="150,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labuser" position="160,100" size="310,30" font="Regular;20" valign="center" backgroundColor="#4D5375"/>
		<widget name="lab4" position="10,150" size="150,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labpass" position="160,150" size="310,30" font="Regular;20" valign="center" backgroundColor="#4D5375"/>
		<widget name="lab5" position="10,200" size="150,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labalias" position="160,200" size="310,30" font="Regular;20" valign="center" backgroundColor="#4D5375"/>
		<widget name="sinactive" position="10,250" zPosition="1" pixmap="skin_default/icons/ninactive.png" size="32,32"  alphatest="on" />
		<widget name="sactive" position="10,250" zPosition="2" pixmap="skin_default/icons/nactive.png" size="32,32"  alphatest="on" />
		<widget name="lab6" position="50,250" size="100,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labsys" position="160,250" size="310,30" font="Regular;20" valign="center" backgroundColor="#4D5375"/>
		<widget name="lab7" position="10,300" size="150,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labstop" position="160,300" size="100,30" font="Regular;20" valign="center"  halign="center" backgroundColor="red"/>
		<widget name="labrun" position="160,300" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" backgroundColor="green"/>
		<ePixmap pixmap="skin_default/buttons/red.png" position="20,360" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/green.png" position="170,360" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/yellow.png" position="320,360" size="140,40" alphatest="on" />
		<widget name="key_red" position="20,360" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<widget name="key_green" position="170,360" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
		<widget name="key_yellow" position="320,360" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["lab1"] = Label(_("Activate Inadyn"))
		self["lactive"] = Pixmap()
		self["linactive"] = Pixmap()
		self["lab2"] = Label(_("Time Update in Minutes:"))
		self["labtime"] = Label()
		self["lab3"] = Label(_("Username:"))
		self["labuser"] = Label()
		self["lab4"] = Label(_("Password:"))
		self["labpass"] = Label()
		self["lab5"] = Label(_("Alias:"))
		self["labalias"] = Label()
		self["sactive"] = Pixmap()
		self["sinactive"] = Pixmap()
		self["lab6"] = Label(_("System:"))
		self["labsys"] = Label()
		self["lab7"] = Label(_("Status:"))
		self["labstop"] = Label(_("Stopped"))
		self["labrun"] = Label(_("Running !"))
		self["key_red"] = Label(_("Start"))
		self["key_green"] = Label(_("Show Log"))
		self["key_yellow"] = Label(_("Setup"))
		
		self["lactive"].hide()
		self["sactive"].hide()
		self["labrun"].hide()
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.KeyOk,
			"back": self.close,
			"red": self.restartIna,
			"green": self.inaLog,
			"yellow": self.setupin
		})

		self.onLayoutFinish.append(self.updateIna)
		
	def restartIna(self):
		if self.my_nabina_state == False:
			mybox = self.session.open(MessageBox, _("You have to Activate Inadyn before to start"), MessageBox.TYPE_INFO)
			mybox.setTitle("Info")
		else:
			rc = system("/usr/bin/inadyn_script.sh stop")
			rc = system("/usr/bin/inadyn_script.sh start")
			rc = system("ps")
			self.updateIna()

	def updateIna(self):
		self["lactive"].hide()
		self["linactive"].hide()
		self["sactive"].hide()
		self["sinactive"].hide()
		self["labrun"].hide()
		self["labstop"].hide()
		
		self.my_nabina_state = False
		
		if fileExists("/usr/bin/inadyn_script.sh"):
			f = open("/usr/bin/inadyn_script.sh",'r')
 			for line in f.readlines():
				line = line.strip()
				if line.find('INADYN_ON=') != -1:
					line = line[10:]
					if line == "1":
						self["lactive"].show()
						self.my_nabina_state = True
					else:
						self["linactive"].show()
				elif line.find('INADYN_USERNAME=') != -1:
					line = line[16:]
					self["labuser"].setText(line)
				elif line.find('INADYN_PASSWORD=') != -1:
					line = line[16:]
					self["labpass"].setText(line)
				elif line.find('INADYN_ALIAS=') != -1:
					line = line[13:]
					self["labalias"].setText(line)
				elif line.find('UPDATE_PERIOD=') != -1:
					line = int(line[14:])
					line = ((line/1000) / 60)
					self["labtime"].setText(str(line))
				elif line.find('DYN_SYSTEM_ON=') != -1:
					line = line[14:]
					if line == "1":
						self["sactive"].show()
					else:
						self["sinactive"].show()
				elif line.find('DYN_SYSTEM=') != -1:
					line = line[11:]
					self["labsys"].setText(line)
					
 			f.close()

		rc = system("ps > /tmp/ninady.tmp")
		check = False
		if fileExists("/tmp/ninady.tmp"):
			f = open("/tmp/ninady.tmp",'r')
 			for line in f.readlines():
				if line.find('inadyn') != -1:
					check = True

			f.close()
			system("rm -f /tmp/ninady.tmp")
			
		if check == True:
			self["labstop"].hide()
			self["labrun"].show()
			self["key_red"].setText(_("Restart"))
		else:
			self["labstop"].show()
			self["labrun"].hide()
			self["key_red"].setText(_("Start"))	
			


	def KeyOk(self):
		pass


	def setupin(self):
		self.session.openWithCallback(self.updateIna, DeliteInaSetup)

	def inaLog(self):
		self.session.open(DeliteInaLog)


class DeliteInaSetup(Screen, ConfigListScreen):
	skin = """
	<screen position="140,120" size="440,300" title="Black Hole E2 Inadyn Setup">
		<widget name="config" position="10,10" size="420,240" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="150,250" size="140,40" alphatest="on" />
		<widget name="key_red" position="150,250" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self.list = []
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = Label(_("Save"))
		
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"red": self.saveIna,
			"back": self.close,
			"green": self.vkeyb

		})
			
		self.updateList()
	
	
	def updateList(self):
	
		self.ina_active = NoSave(ConfigYesNo(default="False"))
		self.ina_user = NoSave(ConfigText(fixed_size = False))
		self.ina_pass = NoSave(ConfigText(fixed_size = False))
		self.ina_alias = NoSave(ConfigText(fixed_size = False))
		self.ina_period = NoSave(ConfigNumber())
		self.ina_sysactive = NoSave(ConfigYesNo(default="False"))
		self.ina_system = NoSave(ConfigText(fixed_size = False))
		
		if fileExists("/usr/bin/inadyn_script.sh"):
			f = open("/usr/bin/inadyn_script.sh",'r')
 			for line in f.readlines():
				line = line.strip()
				if line.find('INADYN_ON=') != -1:
					line = line[10:]
					if line == "1":
						self.ina_active.value = True
					else:
						self.ina_active.value = False
					ina_active1 = getConfigListEntry(_("Activate Inadyn"), self.ina_active)
					self.list.append(ina_active1)
				elif line.find('INADYN_USERNAME=') != -1:
					line = line[16:]
					self.ina_user.value = line
					ina_user1 = getConfigListEntry(_("Username"), self.ina_user)
					self.list.append(ina_user1)
				elif line.find('INADYN_PASSWORD=') != -1:
					line = line[16:]
					self.ina_pass.value = line
					ina_pass1 = getConfigListEntry(_("Password"), self.ina_pass)
					self.list.append(ina_pass1)
				elif line.find('INADYN_ALIAS=') != -1:
					line = line[13:]
					self.ina_alias.value = line
					ina_alias1 = getConfigListEntry(_("Alias"), self.ina_alias)
					self.list.append(ina_alias1)
				elif line.find('UPDATE_PERIOD=') != -1:
					line = int(line[14:])
					line = ((line/1000) / 60)
					self.ina_period.value = line
					ina_period1 = getConfigListEntry(_("Time Update in Minutes"), self.ina_period)
					self.list.append(ina_period1)
				elif line.find('DYN_SYSTEM_ON=') != -1:
					line = line[14:]
					if line == "1":
						self.ina_sysactive.value = True
					else:
						self.ina_sysactive.value = False
					ina_sysactive1 = getConfigListEntry(_("Set System"), self.ina_sysactive)
					self.list.append(ina_sysactive1)
				elif line.find('DYN_SYSTEM=') != -1:
					line = line[11:]
					self.ina_system.value = line
					ina_system1 = getConfigListEntry(_("System"), self.ina_system)
					self.list.append(ina_system1)
					
 			f.close()
		
		
		self["config"].list = self.list
		self["config"].l.setList(self.list)
		
	def vkeyb(self):
		sel = self["config"].getCurrent()
		if sel:
			self.vkvar = sel[0]
			self.vki = self["config"].getCurrentIndex()
			value = "xmeo"
			if self.vki == 1:
				value = self.ina_user.value
			elif self.vki == 2:
				value = self.ina_pass.value
			elif self.vki == 3:
				value = self.ina_alias.value
			elif self.vki == 6:
				value = self.ina_system.value
			
			if value != "xmeo":
				self.session.openWithCallback(self.UpdateAgain, VirtualKeyBoard, title=self.vkvar, text=value)
			else:
				self.session.open(MessageBox, _("Please use Virtual Keyboard for text rows only:\n-Username\n-Password\n-Alias\n-System"), MessageBox.TYPE_INFO)
	
	def UpdateAgain(self, newt):
		self.list = [ ]
		if newt is None:
			newt = ""
		if newt.strip() != "":
			if self.vki == 1:
				self.ina_user.value = newt
			elif self.vki == 2:
				self.ina_pass.value = newt
			elif self.vki == 3:
				self.ina_alias.value = newt
			elif self.vki == 6:
				self.ina_system.value = newt
		
			ina_active1 = getConfigListEntry(_("Activate Inadyn"), self.ina_active)
			self.list.append(ina_active1)
			ina_user1 = getConfigListEntry(_("Username"), self.ina_user)
			self.list.append(ina_user1)
			ina_pass1 = getConfigListEntry(_("Password"), self.ina_pass)
			self.list.append(ina_pass1)
			ina_alias1 = getConfigListEntry(_("Alias"), self.ina_alias)
			self.list.append(ina_alias1)
			ina_period1 = getConfigListEntry(_("Time Update in Minutes"), self.ina_period)
			self.list.append(ina_period1)
			ina_sysactive1 = getConfigListEntry(_("Set System"), self.ina_sysactive)
			self.list.append(ina_sysactive1)
			ina_system1 = getConfigListEntry(_("System"), self.ina_system)
			self.list.append(ina_system1)
		
			self["config"].list = self.list
			self["config"].l.setList(self.list)
			#self.session.open(MessageBox, "aggiornata", MessageBox.TYPE_INFO)	
		
	def saveIna(self):
		
		if fileExists("/usr/bin/inadyn_script.sh"):
			inme = open("/usr/bin/inadyn_script.sh",'r')
			out = open("/usr/bin/inadyn_script.tmp",'w')
			for line in inme.readlines():
				line = line.replace('\n', '')
				if line.find('INADYN_ON=') != -1:
					strview = "0"
					if self.ina_active.value == True:
						strview = "1"
					line = "INADYN_ON=" + strview
				
				elif line.find('INADYN_USERNAME=') != -1:
					line = "INADYN_USERNAME=" + self.ina_user.value.strip()
				
				elif line.find('INADYN_PASSWORD=') != -1:
					line = "INADYN_PASSWORD=" + self.ina_pass.value.strip()
				
				elif line.find('INADYN_ALIAS=') != -1:
					line = "INADYN_ALIAS=" + self.ina_alias.value.strip()
				
				elif line.find('UPDATE_PERIOD=') != -1:
					strview = (self.ina_period.value * 1000 * 60)
					strview = str(strview)
					line = "UPDATE_PERIOD=" + strview
				
				elif line.find('DYN_SYSTEM_ON=') != -1:
					strview = "0"
					if self.ina_sysactive.value == True:
						strview = "1"
					line = "DYN_SYSTEM_ON=" + strview
				
				elif line.find('DYN_SYSTEM=') != -1:
					line = "DYN_SYSTEM=" + self.ina_system.value.strip()
				
				out.write(line + "\n")
				
			out.close()
			inme.close()
		
		else :
			self.session.open(MessageBox, _("Sorry Inadyn Script is Missing"), MessageBox.TYPE_INFO)
			self.close()
			
		if fileExists("/usr/bin/inadyn_script.tmp"):
			system("mv -f  /usr/bin/inadyn_script.tmp /usr/bin/inadyn_script.sh")
			system("chmod 0755 /usr/bin/inadyn_script.sh")
		
		self.myStop()

		
	def myStop(self):
		self.close()
		
		
class DeliteInaLog(Screen):
	skin = """
	<screen position="140,120" size="440,300" title="Black Hole E2 Inadyn Log">
		<widget name="infotext" position="10,10" size="420,280" font="Regular;18" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["infotext"] = ScrollLabel("")
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.close,
			"back": self.close,
			"up": self["infotext"].pageUp,
			"down": self["infotext"].pageDown

		})
		
		strview = ""
		if fileExists("/var/log/inadyn.log"):
			f = open("/var/log/inadyn.log",'r')
 			for line in f.readlines():
				strview += line
				
			f.close()
		self["infotext"].setText(strview)


class DeliteOpenvpn(Screen):
	skin = """
	<screen position="80,150" size="560,310" title="Black Hole E2 OpenVpn Panel">
		<widget name="lab1" position="20,20" size="150,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="lab1a" position="170,16" size="370,60" font="Regular;20" valign="center" transparent="1"/>
		<widget name="lab2" position="20,90" size="150,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labactive" position="170,90" size="250,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="lab3" position="20,160" size="150,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labstop" position="170,160" size="100,30" font="Regular;20" valign="center"  halign="center" backgroundColor="red"/>
		<widget name="labrun" position="170,160" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" backgroundColor="green"/>
		<ePixmap pixmap="skin_default/buttons/red.png" position="0,260" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/green.png" position="140,260" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/yellow.png" position="280,260" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/blue.png" position="420,260" size="140,40" alphatest="on" />
		<widget name="key_red" position="0,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<widget name="key_green" position="140,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
		<widget name="key_yellow" position="280,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
		<widget name="key_blue" position="420,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["lab1"] = Label(_("Vpn Version: "))
		self["lab1a"] = Label(_("OpenVPN Panel - by Black Hole Team."))
		self["lab2"] = Label(_("Startup Module:"))
		self["labactive"] = Label(_("Inactive"))
		self["lab3"] = Label(_("Current Status:"))
		self["labstop"] = Label(_("Stopped"))
		self["labrun"] = Label(_("Running"))
		self["key_red"] = Label(_("Start"))
		self["key_green"] = Label(_("Stop"))
		self["key_yellow"] = Label(_("Set Active"))
		self["key_blue"] = Label(_("Show Log"))
		self.my_vpn_active = False
		self.my_vpn_run = False
				
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.close,
			"back": self.close,
			"red": self.restartVpn,
			"green": self.stopVpnstop,
			"yellow": self.activateVpn,
			"blue": self.Vpnshowlog

		})
		
		self.onLayoutFinish.append(self.updateVpn)
		
	def activateVpn(self):
		
		myline = 'AUTOSTART="all"'
		mymess = _("OpenVpn Enabled. Autostart activated.")
		if self.my_vpn_active == True:
			myline = 'AUTOSTART="none"'
			mymess = _("OpenVpn disabled.")
			
		if fileExists("/usr/bin/openvpn_script.sh"):
			inme = open("/usr/bin/openvpn_script.sh",'r')
			out = open("/usr/bin/openvpn_script.tmp",'w')
			for line in inme.readlines():
				if line.find('AUTOSTART="') != -1:
					line = myline + '\n'
				out.write(line)
			out.close()
			inme.close()
			
		if fileExists("/usr/bin/openvpn_script.tmp"):
			os_rename("/usr/bin/openvpn_script.tmp", "/usr/bin/openvpn_script.sh")
			system("chmod 0755 /usr/bin/openvpn_script.sh")
		
		mybox = self.session.open(MessageBox, mymess, MessageBox.TYPE_INFO)
		mybox.setTitle("Info")
		
		self.updateVpn()
		
	def restartVpn(self):
		if self.my_vpn_active == False:
			mybox = self.session.open(MessageBox, _("You have to Activate OpenVpn before to start"), MessageBox.TYPE_INFO)
			mybox.setTitle("Info")
		elif self.my_vpn_active == True and self.my_vpn_run == False:
			rc = system("/usr/bin/openvpn_script.sh start")
			rc = system("ps")
			self.updateVpn()
		elif self.my_vpn_active == True and self.my_vpn_run == True:
			rc = system("/usr/bin/openvpn_script.sh restart")
			rc = system("ps")
			self.updateVpn()
			
	def stopVpnstop(self):
		if self.my_vpn_run == True:
			rc = system("/usr/bin/openvpn_script.sh stop")
			rc = system("ps")
			self.updateVpn()
			
	def Vpnshowlog(self):
		self.session.open(DeliteVpnLog)
		
	def updateVpn(self):
		
		rc = system("ps > /tmp/nvpn.tmp")
		self["labrun"].hide()
		self["labstop"].hide()
		self["labactive"].setText(_("Inactive"))
		self["key_yellow"].setText(_("Set Active"))
		self.my_vpn_active = False
		self.my_vpn_run = False
		
		
		if fileExists("/usr/bin/openvpn_script.sh"):
			f = open("/usr/bin/openvpn_script.sh",'r')
 			for line in f.readlines():
				if line.find('AUTOSTART="all"') != -1:
					self["labactive"].setText(_("Active/Autostart enabled"))
					self["key_yellow"].setText(_("Deactivate"))
					self.my_vpn_active = True
								
			f.close()
				
				
		if fileExists("/tmp/nvpn.tmp"):
			f = open("/tmp/nvpn.tmp",'r')
 			for line in f.readlines():
				if line.find('openvpn') != -1:
					self.my_vpn_run = True

			f.close()
			os_remove("/tmp/nvpn.tmp")
			
		if self.my_vpn_run == True:
			self["labstop"].hide()
			self["labrun"].show()
			self["key_red"].setText(_("Restart"))
		else:
			self["labstop"].show()
			self["labrun"].hide()
			self["key_red"].setText(_("Start"))
			
	
class DeliteVpnLog(Screen):
	skin = """
	<screen position="80,100" size="560,400" title="Black Hole OpenVpn Log">
		<widget name="infotext" position="10,10" size="540,380" font="Regular;18" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["infotext"] = ScrollLabel("")
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.close,
			"back": self.close,
			"up": self["infotext"].pageUp,
			"down": self["infotext"].pageDown

		})
		
		strview = ""
		rc = system("tail /etc/openvpn/openvpn.log > /etc/openvpn/tmp.log")
		#tail /etc/openvpn/openvpn.log
		if fileExists("/etc/openvpn/tmp.log"):
			f = open("/etc/openvpn/tmp.log",'r')
 			for line in f.readlines():
				strview += line
				
			f.close()
			os_remove("/etc/openvpn/tmp.log")
		self["infotext"].setText(strview)
		

class BhBackupSettings(Screen):
	skin = """
	<screen position="center,center,100" size="800,300" title="Back Up your settings">
		<widget name="infotext" position="10,10" size="780,240" font="Regular;26" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="330,250" size="140,40" alphatest="on" />
		<widget name="key_red" position="330,250" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		msg = _("Backup your Settings.\n\nYou can setup backup location and backup files in Plugins -> Softare managment -> advanced.")
		
		self["infotext"] = Label(msg)
		self["key_red"] = Label(_("Backup"))
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.doIt,
			"red": self.doIt,
			"back": self.close

		})
	def doIt(self):
		self.session.open(BackupScreen, runBackup = True)
		self["infotext"].setText(_("Backup Complete"))
