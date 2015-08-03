**Convertisseur de devise** est une application développée avec PyQt4.

Ce logiciel permet de convertir en temps réel les devises nationales des pays en s'appuyant sur les données
mis en ligne de la Banque de Canada (url: http://www.bankofcanada.ca/en/markets/csv/exchange_eng.csv).
Ce logiciel permet aussi de convertir en temps réel 1 Bitcoin en devises nationales en s'appuyant sur le données
mis en ligne sur le site Bitpay (url: http://www.bitpay.com)

	Need Fix: 
	    - Ajouter des Altcoins (Litecoin, dodgecoin, etc..)
	    - Convertir les montants entrées par l'utilisateur
	    - Ajouter d'autres sources pour la conversion des Bitcoin et les Altcoins
	Fixed:
	    [x] Ajout de Litecoin en dépendance des Btc-E.com 
	    [x] Ajout de QtCore.QCoreApplication.processEvents() pour que la fenêtre ne gêle pas en téléchargeant les données des sites.


![alt tag](http://3.bp.blogspot.com/-t0ccDJBIUQk/Vb-JvbFz3JI/AAAAAAAAAOw/TB24GCYpZcs/s640/S%25C3%25A9lection_003.jpg)