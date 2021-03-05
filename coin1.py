from coinbase.wallet.client import Client
from coinbase.wallet.model import Transaction
#from forex_python.converter import CurrencyRates
import sys
import json
import httplib
import urllib
import config_coin_mpv
import config_coin_arg

if (len(sys.argv)>0):
   user = sys.argv[1]

if (user=='mpv'):
    api_key = config_coin_mpv.api_key
    api_secret = config_coin_mpv.api_secret
   
if (user=='arg'):
    api_key = config_coin_arg.api_key
    api_secret = config_coin_arg.api_secret


client = Client(api_key, api_secret)
currency_EUR = 'BTC-EUR'
currency_USD = 'BTC-USD'
currencyEURUSD='EUR-USD'
currency_LINK='LINK-EUR'
total = 0
message = []

preu = client.get_spot_price(currency_pair=currency_EUR)
preuEUR = str(preu.amount)
preu = client.get_spot_price(currency_pair=currency_USD)
preuUSD = str(preu.amount)
preu0 = client.get_spot_price(currency_pair=currencyEURUSD)
preuEUR0 = str(preu0.amount)
preu = client.get_spot_price(currency_pair=currency_LINK)
preuLINK = str(preu.amount)

accounts = client.get_accounts()

print '<br>1 BTC ' + preuEUR + ' &euro;'
print '<br>1 BTC ' + preuUSD  + ' $'
print '<br>1 LINK ' + preuLINK + ' &euro;'
print("<br>1 &euro; = " + str(preuEUR0) + " $")
fvalortotal=0

llista = []
llista_id = []
llista_nomcompte = []
llista_saldo = []

for wallet in accounts.data:

    #print(wallet)
    valor = str( wallet['native_balance'])
    balanc = str(wallet['balance'])
    fvalor = float(valor.replace("EUR ",""))

    if round(fvalor)!=0:

      if str(wallet['currency'])=='BTC':
         cadena = '<br/><br/>'
         cadena = cadena + '<a href="http://bitstamp.net/markets/btc/eur" target="_blank">'
         cadena = cadena + '<img src=\"https://assets.bitstamp.net/widgets/s/widgets/widgets/img/btc.5e2d1332.svg\" width=\"40\" height=\"40\"></a>'
         cadena = cadena + '<b> Bitcoin</b>'
         cadena += '<br>Saldo ' + balanc
         cadena += '<br>Saldo ' + valor.replace("EUR ","") + ' &euro;'
         llista.insert(0,cadena)
         llista_id.insert(0,str(wallet['id']))
         llista_nomcompte.insert(0,str(wallet['name']))
         llista_saldo.insert(0,round(fvalor,2))

      if str(wallet['currency'])=='LINK':
         cadena2 = '<br/><br/>'
         cadena2 = cadena2 + '<a href="https://www.bitstamp.net/markets/link/eur/" target="_blank">'
         cadena2 = cadena2 + '<img src=\"https://assets.bitstamp.net/dashboard/s/widgets/dashboard/98015f33f9e7bcb0acc781f022646f8f.svg\" width=\"40\" height=\"40\"></a>'
         cadena2 = cadena2 + '<b> Chainlink</b>'
         cadena2 += '<br>Saldo ' + balanc
         cadena2 += '<br>Saldo ' + valor.replace("EUR ","") + ' &euro;'
         llista.append(cadena2)
         llista_id.append(str(wallet['id']))
         llista_nomcompte.append(str(wallet['name']))
         llista_saldo.append(round(fvalor,2))

      if str(wallet['currency'])=='ETH':
         cadena3 = '<br/><br/>'
         cadena3 = cadena3 + '<a href="https://www.bitstamp.net/markets/eth/eur/" target="_blank">'
         cadena3 = cadena3 + '<img src=\"https://assets.bitstamp.net/dashboard/s/widgets/dashboard/44cfa606c6c2ace5de7d6a29ff2bb998.svg\" width=\"40\" height=\"40\"></a>'
         cadena3 = cadena3 + '<b> Ethereum</b>'
         cadena3 += '<br>Saldo ' + balanc
         cadena3 += '<br>Saldo ' + valor.replace("EUR ","") + ' &euro;'
         llista.append(cadena3)
         llista_id.append(str(wallet['id']))
         llista_nomcompte.append(str(wallet['name']))
         llista_saldo.append(round(fvalor,2))

      fvalortotal+=fvalor

for i in range(len(llista)) :
          #print(llista[i])
          i+=1

    
print("<br><br><b>Saldo Total</b>")
print("<br>" + str(fvalortotal) + " &euro;")

print("<br><br><b>CARTERA</b>")

i=0
llista_valor_transacc = []
ftransaccionstotal=0

for id in llista_id:

 print(llista[i])
 #print("<br><b>" + llista_nomcompte[i] + " </b>")
 transactions = client.get_transactions(id)
 ftransaccionswallet=0
 str_transacc="<i>Transaccions </i>"
 str_transacc+="<button type=\"button\" class=\"btn btn-info\" data-toggle=\"collapse\" data-target=\"#transacc" + str(i) + "\">+</button>"
 str_transacc+="<div id=\"transacc" + str(i) + "\" class=\"collapse\">"
 str_transacc+="<font size=\"5\">"
 for t in transactions.data:

        #print("<p>" + t.details.header[:-3] + "</p>")
        fvalor=float(t.native_amount.amount)
        
        str_transacc+="<p>" + t.native_amount.amount + " &euro;"
        str_transacc+=" " + t.created_at[:10] + "</p>"
        #print("<p>" + str(t.amount) + "</p>")        

        ftransaccionswallet+=fvalor
       
        ftransaccionstotal+=fvalor
 str_transacc+="<p>Total: " + str(ftransaccionswallet) + "</p>"
 str_transacc+="</font></div>"
 llista_valor_transacc.append(ftransaccionswallet)
 print("<p>Benefici: " + str(llista_saldo[i]-ftransaccionswallet) + " &euro;")
 fperc_benefici=((llista_saldo[i]*100)/ftransaccionswallet)-100
 if (fperc_benefici>=0):
     print(" <font size=\"5\"><span style=\"color:rgb(0,180,0);\">+" + str(round(fperc_benefici,2)) + "%</span></font></p>")
 else:
     print(" <font size=\"5\"><span style=\"color:red;\">" + str(round(fperc_benefici,2)) + "%</span></font></p>")
 print(str_transacc)
 i=i+1

print("<br>")
print("<br><b>Valor actual:</b> " + str(fvalortotal) + " &euro;")
print("<br><b>Total transaccions:</b> " + str(ftransaccionstotal) + " &euro;")

fperc_benefici=round(((fvalortotal*100)/ftransaccionstotal)-100,2)

if (fperc_benefici>=0):
    spercbenefici="<font size=\"5\"><span style=\"color:rgb(0,180,0);\">+" + str(fperc_benefici) + "%</span></font>"
else:
    spercbenefici="<font size=\"5\"><span style=\"color:red;\">" + str(fperc_benefici) + "%</span></font>"

if ((fvalortotal-ftransaccionstotal)>=0):
 print("<br><b>Benefici: </b>" + str(fvalortotal-ftransaccionstotal) + " &euro;</span> " + spercbenefici)
else:
 print("<br><b>Benefici: </b>" + str(fvalortotal-ftransaccionstotal) + " &euro;</span> " + spercbenefici)
