import serial
import time
import feedparser
import math

# RSS Feed offset from local time, in hours
RSSTIMEOFFSET = 7

# Cutoff for "new" headlines, in minutes
HLCUT = 60

class LEDSerial(serial.Serial):
	def __init__(self, port):
		serial.Serial.__init__(self)
		self.baudrate = 9600
		self.port = port
		self.open()
		time.sleep(2)

	def send(self, msg):
		"""Write msg to LED sign."""
		for i in msg:
			self.write(i)
			self.flush()
		# newline char means msg end
		self.write(chr(10))
	
class LEDSerialRSS(LEDSerial):
	def __init__(self, port, feed, new):
		LEDSerial.__init__(self, port)
		self.url = feed
		self.entrynum = 0
		self.new = new
		self.lastsent = ""
		self.lastcheck = time.mktime(time.localtime())
		self.update_feed()

	def update_feed(self):
		"""Update RSS feed"""
		parsed = feedparser.parse(self.url)
		if self.new:
			good = []
			for i in parsed.entries:
				temp_time = time.mktime(i.updated_parsed) - (RSSTIMEOFFSET * 3600)
				if math.fabs(self.lastcheck - temp_time) <= (HLCUT * 60):
					good.append(i)
				else:
					break
			self.feed = good
		else:
			self.feed = parsed.entries	
		self.entrynum = 0
		self.lastcheck = time.mktime(time.localtime())

	def next_headline(self):
		"""Send next headline to sign, update feed if necessary."""
		if self.entrynum < len(self.feed):
			entry = self.feed[self.entrynum]
			# assumes feed timezone is EDT
			feed_time = time.mktime(entry.updated_parsed) - (RSSTIMEOFFSET * 3600)
			if (not self.new) or (math.fabs(self.lastcheck - feed_time) <= (HLCUT * 60)): 
				output = "  %s.  " % entry.title
				self.send(output)
				self.entrynum += 1
				self.lastsent = output
				return self.lastsent 
			else:
				if self.lastsent != "No new headlines.":
					self.send(" ")
				self.entrynum += 1
				self.lastsent = "No new headlines."
				return self.lastsent
		else:
			self.update_feed()
			if self.new:
				if self.lastsent != "No new headlines.":
					self.send(" ")
					self.lastsent = "No new headlines."
				else:
					time.sleep(15)
				return self.lastsent
			else:
				self.next_headline() 		
