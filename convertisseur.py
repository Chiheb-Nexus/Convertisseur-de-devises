#!/user/bin/python
# -*- coding: utf-8 -*-

import sys
import datetime
import urllib2
import json     
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore

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
		bitpayLabel = QLabel("Taux de change de Bitcoin sur <font color=red>Bitpay.com</font> date: "+ "<font color= blue>"+\
			str(datetime.date.today()) + "</font>")
		self.bitpayName = QComboBox()
		self.bitpayName.addItem("1 Bitcoin")
		self.bitpayRate = QComboBox()
		self.bitcoinBitpay()

		"""
		# Qr Code for donation
		image = QLabel()
		pixmap = QPixmap('qrcode.bmp')
		image.setPixmap(pixmap)
		"""
		blog = QLabel("Blog:<font color=blue> Chiheb NeXus </font>: <b>http://nexus-coding.blogspot.com</b>")
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
		self.setWindowTitle("Convertisseur de devise")

	def updateUi(self):
		to = unicode(self.toComboBox.currentText())
		from_ = unicode(self.fromComboBox.currentText())
		amount = (self.rates[from_] / self.rates[to]) * self.fromSpinBox.value()
		self.toLabel.setText("%0.2f" % amount)

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

		url="https://bitpay.com/api/rates"
		jURL=urllib2.urlopen(url)
		jObject=json.load(jURL)
		valueur = jObject
		for i in valueur:
			if i[u'rate'] != 1:
				rate = unicode(i[u'rate'])
				code = unicode(i[u'code'])
				self.bitpayRate.addItem(unicode(rate) + " " + unicode(code))


if __name__ == '__main__':
	app = QApplication(sys.argv)
	form = Form()
	form.show()
	app.exec_()