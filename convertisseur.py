#!/user/bin/python
# -*- coding: utf-8 -*-

import sys
import datetime
import urllib2
import json     
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore

__version__ = "v0.0.3"
__author__ = "Chiheb NeXus"

class Form(QDialog):
	"""
	Convertisseur.py permet de convertir en temps réel les devises nationales des pays en s'appuyant sur les données
	mis en ligne de la Banque de Canada (url: http://www.bankofcanada.ca/en/markets/csv/exchange_eng.csv)
	Convertisseur.py permet aussi de convertir en temps réel 1 Bitcoin en devises nationales en s'appuyant sur le données
	mis en ligne sur le site Bitpay (url: http://www.bitpay.com)

	Need Fix: 
	    - Ajouter des Altcoins (Litecoin, dodgecoin, etc..)
	    - Convertir les montants entrées par l'utilisateur
	    - Ajouter d'autres sources pour la conversion des Bitcoin et les Altcoins

	Fixed: 
	    - Ajout de Litecoin en dépendance des Btc-E.com 
	    - Ajout de QtCore.QCoreApplication.processEvents() pour que la fenêtre ne gêle pas en téléchargeant les données des sites.

	"""
	def __init__(self, parent=None):
		super(Form, self).__init__(parent)

		self.setFixedSize(700, 200)


		date = self.getdata()
		rates = sorted(self.rates.keys())
		dateLabel = QLabel(date)
		self.fromComboBox = QComboBox()
		self.fromComboBox.addItems(rates)
		self.fromSpinBox = QDoubleSpinBox()
		self.fromSpinBox.setRange(0.01, 10000000.00)
		self.fromSpinBox.setValue(1.00)
		self.toComboBox = QComboBox()
		self.toComboBox.addItems(rates)
		self.toLabel = QLabel("1.00")

		# Bitcoin widgets
		bitpayLabel = QLabel("Taux de change de Bitcoin sur <font color=red>Bitpay.com</font> et litecoin sur<font color= red> Btc-E.com </font>. " +\
			"<font color= blue>"+ str(datetime.date.today()) + "</font>" )
		self.bitpayName = QComboBox()
		self.bitpayName.addItem("Choisir Bitcoin ou Altcoin")
		self.bitpayName.addItem("Bitcoin")
		self.bitpayName.addItem("Litecoin")

		self.bitpayName.activated.connect(self.on_clicked)
		self.bitpayRate = QComboBox()
		
		"""
		# Qr Code for donation
		image = QLabel()
		pixmap = QPixmap('qrcode.bmp')
		image.setPixmap(pixmap)
		"""
		blog = QLabel("Blog:<font color=blue> "+__author__+" </font>: <b>http://nexus-coding.blogspot.com</b>")
		adresse = QLabel("Don en Bitcoin: <font size=3 color = blue><b>1CiGEcAs2pXmXXeTspccFVRmvUtPuiF2CV</b></font>")	

		layout = QVBoxLayout()

		grid = QGridLayout()
		grid.addWidget(dateLabel, 0, 0)
		grid.addWidget(self.fromComboBox, 1, 0)
		grid.addWidget(self.fromSpinBox, 1, 1)
		grid.addWidget(self.toComboBox, 2, 0)
		grid.addWidget(self.toLabel, 2, 1)

		grid.addWidget(bitpayLabel,3,0)
		grid.addWidget(self.bitpayName,4,0)
		grid.addWidget(self.bitpayRate, 4,1)
		#grid.addWidget(image, 5,0)
		#grid.addWidget(adresse, 5,0)

		layout.addLayout(grid)
		adresse.setAlignment(QtCore.Qt.AlignCenter)
		layout.addWidget(adresse)
		blog.setAlignment(QtCore.Qt.AlignCenter)
		layout.addWidget(blog)
		self.setLayout(layout)

		self.connect(self.fromComboBox,SIGNAL("currentIndexChanged(int)"), self.updateUi)
		self.connect(self.toComboBox,SIGNAL("currentIndexChanged(int)"), self.updateUi)
		self.connect(self.fromSpinBox,SIGNAL("valueChanged(double)"), self.updateUi)
		self.setWindowTitle("Convertisseur de devise" +" "+ __version__)

	def updateUi(self):
		to = unicode(self.toComboBox.currentText())
		from_ = unicode(self.fromComboBox.currentText())
		amount = (self.rates[from_] / self.rates[to]) * self.fromSpinBox.value()
		self.toLabel.setText("%0.2f" % amount)

	def on_clicked(self):
		if str(self.bitpayName.currentText()) == "Bitcoin":
			self.bitcoinBitpay()
		elif str(self.bitpayName.currentText()) == "Litecoin":
			self.litecoinBtce()
		else:
			self.removeItems()

	def getdata(self):
		self.rates = {}
		try:
			date = "Unknown"
			fh = urllib2.urlopen("http://www.bankofcanada.ca/en/markets/csv/exchange_eng.csv")
			for line in fh:
				if not line or line.startswith("#") or line.startswith("Closing "):
					continue
				fields = line.split(", ")
				if line.startswith("Date "):
					date = fields[-1]
				else:
					try:
						value = float(fields[-1])
						self.rates[unicode(fields[0])] = value
					except ValueError:
						pass
			return "Taux de change pour la <font color=red>Banque de Canada</font>, date: " + "<font color=blue>"+date+"</font>"
		except Exception, e:
			return u"Impossible de télécharger. Une connection internet est requise!:\n%s" % e


	def bitcoinBitpay(self):
		"""
		Bitcoin en multiples devises

		"""

		self.removeItems()
		QtCore.QCoreApplication.processEvents() # Pour que la Gui ne gêle pas !

		try:
			url="https://bitpay.com/api/rates"
			jURL=urllib2.urlopen(url)
			jObject=json.load(jURL)
			valeur = jObject
			for i in valeur:
				if i[u'rate'] != 1:
					rate = unicode(i[u'rate'])
					code = unicode(i[u'code'])
					self.bitpayRate.addItem(unicode(rate) + " " + unicode(code))
		except:
			print "Error connection"

	def litecoinBtce(self):
		"""
		Litecoin en USD
		"""
		self.removeItems()
		QtCore.QCoreApplication.processEvents() # Pour que la Gui ne gêle pas !

		try:
			url="https://btc-e.com/api/2/ltc_usd/ticker"
			jURL=urllib2.urlopen(url)
			jObject=json.load(jURL)
			valeur = jObject

			high = valeur[u'ticker'][u'high']
			low = valeur[u'ticker'][u'low']
			avg = valeur[u'ticker'][u'avg']
			vol_cur = valeur[u'ticker'][u'vol_cur']
			last = valeur[u'ticker'][u'last']
			buy = valeur[u'ticker'][u'buy']
			sell = valeur[u'ticker'][u'sell']
			server_time = valeur[u'ticker'][u'server_time']
			usd = unicode(" USD")
			self.bitpayRate.addItem(unicode("High: ") + unicode(avg) +usd)
			self.bitpayRate.addItem(unicode("Low: ") + unicode(low) + usd)
			self.bitpayRate.addItem(unicode("Average: ")+ unicode(avg) + usd)
			self.bitpayRate.addItem(unicode("Volume: ")+ unicode(vol_cur) + usd)
			self.bitpayRate.addItem(unicode("Last: ")+ unicode(last) + usd)
			self.bitpayRate.addItem(unicode("Buy: ") + unicode(buy) + usd)
			self.bitpayRate.addItem(unicode("Sell: ")+ unicode(sell) + usd)

		except:
			print "Error connection"

	def removeItems(self):
		self.bitpayRate.clear()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	form = Form()
	form.show()
	app.exec_()