import wx
import serialscan
import ledserial
import time
import sys
import threading
import pickle
import os.path
import base64
import cStringIO

icon_off_b64 = \
"""/9j/4AAQSkZJRgABAQEASABIAAD//gATQ3JlYXRlZCB3aXRoIEdJTVD/2wBDAAEBAQEBAQEBAQEB
AQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBD
AQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEB
AQEBAQEBAQH/wAARCAAgACADASIAAhEBAxEB/8QAGAABAAMBAAAAAAAAAAAAAAAACAAGCQf/xAA5
EAAABAUCBAMFBAsAAAAAAAAFBgcIBAkVFhcDFAoYGSYCEyUAASg2NxIaWWUnNTlFR0pXZ3i48P/E
ABQBAQAAAAAAAAAAAAAAAAAAAAD/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwB9
9Ud9n3sPpo5z+CX+iuMkd/Daz79R8fZa+rXdnz5+RfLXo3tOK1mjvslr8hnJSueF80c0eS/0ZI6o
1y455dbN+rKfHuj0e+zX+oKVUKr6rvtiG7MAfz13/fg8eyA4utdOV908iVy9rXxy7uAXVdLKrds3
hiRRWSH+1rjpBgt+4LfpNboI3St3v6QJbfZ6wZ/s0n1TYVXlPToHLn91lfW1pvTp5fzrgxtoXYOd
3JmggKt24Co6HFI1XUUg6DCe9QEx0Pyd+XKOJ6mrG+OwSJeJ3e0qD80zbDMPVcvrUlLozABJIRD1
EpgR0+NSPLKM+MRgUu0waDQVLAOGOJfV47CQAlpmDTmD+/QLIiOFNQtA+kgrE8+hZ37A7+ed1o5F
E4j4XeWzls6fP8bcxXpmJ4ZZ/tGlluW5iz89q9d/ddL9RADk/wBqbwlf+AEhv/Yod9gX6pKwliHc
bmOqktalp+j6ZFemXMoqpHIuJ+RC7W5SIeXQaum42CQQXwirmAXCgIMqAhD78YEw8MhfNjY2G0NV
AcU0NNYeQtkgjcuAT8XaKuLgHEEA+OLS1Vk6jyIBJYLq6zRO1bOoErupqmhMgzH8FpGypmMZq5cK
gwXRC5oLV0QgSgfcP59UhWbC9GbE6xy7aGp5KRJSsGWUdc5ttJ1as5tqOkAx9uH9YiqbQ6nG0qjw
T6sAwG82G/gN0GRUFGxEeXIVmwqvKekvtoIDU6+trTeotzAErObbQuwc7uTK5/SnuMaWIOKRquop
B0YLdlDxjofk7Ax0cT1NKC8YIB37BZWTHJFE4jpovU5wModPnNXxHN1cBjuynhlnHH0CJpStK7bt
PnzZUK9bPoW0oozucwFUVhLFXmm8LBi1S0/UrGrQJH6TqLYByLhxsFUyc4oRu5NDrbokI2qoBVqI
fchNHdgYwPfwdTDYXdaH21+zSQrNhSiU9OgbQf2p0BbXZdOnl/JWc22il/YIcmaD+q3cYKsQiUir
apSEYMW71Hi5XPO2BcrAnp6sF4LBIl4Yh7SXvzTNz0w9KC+iqUtcMAErZEIsSp5HUE1LCsoN4xGO
S7UBoxBVTHIYnF9ITsGgCpGYSOYx7tAzCIGU090CEdyscD6KEgP/2Q==
"""

icon_on_b64 = \
"""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
tW6EIxoRyiuSsUnPnQeHg1qHBIf/2Q==
"""

class RSSPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)

		# Sub panel
                self.subpanel = wx.Panel(self)

		# Controls
		self.check = wx.CheckBox(self, -1, 'RSS Feed')		
	
		self.label_url = wx.StaticText(self.subpanel, -1, label="URL", style=wx.ALIGN_CENTER)
		self.combo_url = wx.ComboBox(self.subpanel, -1, size=(300,-1), style=wx.CB_DROPDOWN)		
		self.button_save = wx.Button(self.subpanel, label="Save", size=(50,-1))
		self.button_delete = wx.Button(self.subpanel, label ="Delete", size=(60,-1))
		options = ['Show all headlines', 'Only show new headlines']
		self.rb_options = wx.RadioBox(self.subpanel, label="Options", 
			choices=options, majorDimension=1, style=wx.RA_SPECIFY_COLS)

		# URL sizer
		self.sizer_url = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer_url.Add(self.label_url, 0, wx.ALIGN_LEFT)
		self.sizer_url.Add(self.combo_url, 1, wx.EXPAND)
		self.sizer_url.Add(self.button_save, 0, wx.EXPAND)
		self.sizer_url.Add(self.button_delete, 0, wx.EXPAND)	
		
		# Sizer for Sub panel
		self.sizer_subpanel = wx.BoxSizer(wx.VERTICAL)
		self.sizer_subpanel.Add(self.sizer_url, 0, wx.EXPAND)
                self.sizer_subpanel.Add(self.rb_options, 0, wx.EXPAND)
		self.subpanel.SetSizerAndFit(self.sizer_subpanel)

		# Panel main sizer
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.check, 0, wx.ALIGN_LEFT)
		self.sizer.Add(self.subpanel, 0, wx.EXPAND)

		# Finish Panel
		self.SetSizerAndFit(self.sizer)
		self.Show()

	def set_state(self, state):
		self.subpanel.Enable(state)
		self.check.SetValue(state)			

class CustomPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)

		# Controls
		self.check = wx.CheckBox(self, -1, 'Custom Text')		
		self.tc = wx.TextCtrl(self, -1)
	
		# Panel main sizer
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.check, 0, wx.ALIGN_LEFT)
		self.sizer.Add(self.tc, 0, wx.EXPAND)		

		# Finish Panel
		self.SetSizerAndFit(self.sizer)
		self.Show()

	def set_state(self, state):
		self.tc.Enable(state)
		self.check.SetValue(state)

class ControlPanel(wx.Panel):
        def __init__(self, parent):
                wx.Panel.__init__(self, parent)

                # Controls
                self.button = wx.ToggleButton(self, label="Start", size=(100,-1))
		self.combo = wx.ComboBox(self, -1, choices=serialscan.scan(), style=wx.CB_READONLY)
		self.combo.SetSelection(0)
		self.label_serial = wx.StaticText(self, -1, label="Serial Port", size=(80,-1))

                # Panel main sizer
                self.sizer = wx.BoxSizer(wx.HORIZONTAL)
                self.sizer.Add(self.label_serial, 0, wx.ALIGN_LEFT)
		self.sizer.Add(self.combo, 1, wx.EXPAND)
		self.sizer.Add(self.button, 0, wx.ALIGN_LEFT)

                # Finish Panel
                self.SetSizerAndFit(self.sizer)
                self.Show()        

	def set_start(self):
		self.button.Enable(True)
		self.button.SetLabel("Start")
		self.button.SetValue(False)
		self.combo.Enable(True)
        
	def set_stop(self):
		self.button.Enable(True)
		self.button.SetLabel("Stop")
		self.button.SetValue(True)
		self.combo.Enable(False)

class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title)
		
		# Object for LED sign	
		self.led = None

		# Boolean for connection state
		self.connected = False

		# Keep track of current time
		self.timer = wx.Timer(self)

		#Favorite RSS feeds
		self.favorites = []
		self.rss_filename = '8x8_rss_favorites.txt'

		# Setting up the menu.
                self.filemenu = wx.Menu()

		# Set up icons
		icon_off_decoded = base64.b64decode(icon_off_b64)
		icon_off_stream = cStringIO.StringIO(icon_off_decoded)
		icon_off_bmp = wx.BitmapFromImage(wx.ImageFromStream(icon_off_stream))
		self.icon_off = wx.EmptyIcon()
		self.icon_off.CopyFromBitmap(icon_off_bmp)
		
		icon_on_decoded = base64.b64decode(icon_on_b64)
                icon_on_stream = cStringIO.StringIO(icon_on_decoded)
                icon_on_bmp = wx.BitmapFromImage(wx.ImageFromStream(icon_on_stream))
                self.icon_on = wx.EmptyIcon()
                self.icon_on.CopyFromBitmap(icon_on_bmp)

		self.icon = self.icon_off
		self.SetIcon(self.icon)
		self.tbicon = wx.TaskBarIcon()

                # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets
                self.menuAbout = self.filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
                self.menuExit = self.filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

                # Creating the menubar.
                self.menuBar = wx.MenuBar()
                self.menuBar.Append(self.filemenu, "&File") # Adding the "filemenu" to the MenuBar
                self.SetMenuBar(self.menuBar) # Adding the MenuBar to the Frame content

		self.CreateStatusBar()
                self.SetStatusText("Disconnected.")

		self.sizer = wx.BoxSizer(wx.VERTICAL)
		
		self.panel_rss = RSSPanel(self)
		self.panel_custom = CustomPanel(self)
		self.panel_control = ControlPanel(self)
	
		self.panel_rss.set_state(True)
		self.panel_custom.set_state(False)
		self.panel_control.set_start()

		self.sizer.Add(self.panel_rss, 0, wx.EXPAND)
		self.line1 = wx.StaticLine(self)
		self.line2 = wx.StaticLine(self)
		self.sizer.Add(self.line1, 0, wx.EXPAND)
		self.sizer.Add(self.panel_custom, 0, wx.EXPAND)
		self.sizer.Add(self.line2, 0, wx.EXPAND)
		self.sizer.Add(self.panel_control, 0, wx.EXPAND)
		self.SetSizerAndFit(self.sizer)
		
		self.load_favorites()

		self.Bind(wx.EVT_CHECKBOX, self.on_rss_checkbox, self.panel_rss.check)
		self.Bind(wx.EVT_CHECKBOX, self.on_custom_checkbox, self.panel_custom.check)
		self.Bind(wx.EVT_TOGGLEBUTTON, self.on_control_button, self.panel_control.button)
		self.Bind(wx.EVT_TIMER, self.next_headline, self.timer)
		self.Bind(wx.EVT_CLOSE, self.on_close)
		self.Bind(wx.EVT_BUTTON, self.save_favorite, self.panel_rss.button_save)	
		self.Bind(wx.EVT_BUTTON, self.delete_favorite, self.panel_rss.button_delete)
                self.Bind(wx.EVT_MENU, self.on_about, self.menuAbout)
                self.Bind(wx.EVT_MENU, self.on_close, self.menuExit)
		self.Bind(wx.EVT_ICONIZE, self.on_minimize)
		self.tbicon.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.on_restore)

		self.Show(True)
		self.Centre()
	
	def on_minimize(self, e):
		if e.Iconized():
			self.Iconize(True)
			self.Hide()
			self.tbicon.SetIcon(self.icon)

	def on_restore(self, e):
		if self.IsIconized():
			self.Iconize(False)
			self.Show()
			self.Raise()
			self.tbicon.RemoveIcon()	

	def on_rss_checkbox(self, e):
		self.panel_rss.set_state(self.panel_rss.check.IsChecked())
		self.panel_custom.set_state(not self.panel_custom.check.IsChecked())
	
	def on_custom_checkbox(self, e):
		self.panel_custom.set_state(self.panel_custom.check.IsChecked())
		self.panel_rss.set_state(not self.panel_rss.check.IsChecked())

	def on_control_button(self, e):
		if not self.panel_control.button.GetValue():
			self.panel_control.set_start()
			self.panel_rss.Enable(True)
			self.panel_custom.Enable(True)
			self.disconnect()
		else:
			try:	
				self.panel_control.set_stop()
				self.panel_rss.Enable(False)
				self.panel_custom.Enable(False)
				self.panel_control.button.Enable(False)
				self.connect()
			except:	
				dlg = wx.MessageDialog(self, "%s" % sys.exc_info()[1].message,
					 "Error", style=(wx.OK|wx.ICON_ERROR)) 
				dlg.ShowModal()
				dlg.Destroy()
				self.disconnect()
				self.panel_control.set_start()
				self.panel_rss.Enable(True)
				self.panel_custom.Enable(True)
			self.panel_control.button.Enable(True)


	def connect(self):
		port = self.panel_control.combo.GetValue()
		url = self.panel_rss.combo_url.GetValue()
		new = self.panel_rss.rb_options.GetSelection() == 1
		if self.panel_rss.check.IsChecked():
			self.led = ledserial.LEDSerialRSS(port, url, new)
			self.connected = True
			self.icon = self.icon_on
			self.SetIcon(self.icon)
			self.panel_control.button.Enable(True)
			self.next_headline(())
		elif self.panel_custom.check.IsChecked():
			self.led = ledserial.LEDSerial(port)
			self.connected = True
			self.icon = self.icon_on
			self.SetIcon(self.icon)
			msg = self.panel_custom.tc.GetValue()
			self.led.send(msg)
			self.SetStatusText("Connected: \"%s\"" % msg) 	

	def next_headline(self, e):
		if self.connected:
			output = self.led.next_headline()
			self.SetStatusText("Connected: \"%s\"" % output)
			self.timer.Start((len(output) * 5 / 8) * 1000)
	
	def load_favorites(self):
		if os.path.exists(self.rss_filename):
			with open(self.rss_filename, "r") as f:
				self.favorites = pickle.load(f) 
			combo = self.panel_rss.combo_url
			combo.Clear()
			combo.AppendItems(self.favorites)
			combo.SetSelection(len(self.favorites) - 1)

	def save_favorite(self, e):
		combo = self.panel_rss.combo_url
		new_fav = combo.GetValue()
		if new_fav != "":
			self.favorites.append(new_fav)
			with open(self.rss_filename, "w") as f:
				pickle.dump(self.favorites, f)
			self.load_favorites()

	def delete_favorite(self, e):
		combo = self.panel_rss.combo_url
		unwanted_fav = combo.GetCurrentSelection()
		self.favorites.pop(unwanted_fav)
		with open(self.rss_filename, "w") as f:
			pickle.dump(self.favorites, f)
		self.load_favorites()

	def on_about(self, e):
		msg = "A wxpython interface for Modern Device 8x8 LED panels.\n\nWritten by Kevin Conley, 2011.\nkevindconley [AT] gmail [DOT] com"
                dlg = wx.MessageDialog(self, msg, "About", wx.OK)
                dlg.ShowModal()
                dlg.Destroy()

	def on_close(self, e):
		self.disconnect()	
		self.Destroy()

	def disconnect(self):
		try:
			self.timer.Stop()
		except:
			pass
		try:
			if self.connected:
				self.led.send("Waiting for input... ")
			self.led.close()
		except:
			pass
		self.connected = False
		self.icon = self.icon_off
		self.SetIcon(self.icon)
		self.SetStatusText("Disconnected.")

# Setup App
app = wx.App(False)

# Setup Frame
frame = MainWindow(None, "8x8 LED Sign Control Panel")

# App Main Loop
app.MainLoop()
