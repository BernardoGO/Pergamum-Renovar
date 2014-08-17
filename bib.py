#bib.py

import mechanize
import cookielib
import urllib
import logging
import sys
from BeautifulSoup import BeautifulSoup
import time
from datetime import datetime, timedelta

Usuario = ''
Senha = ''


def main():

    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    r= br.open('http://bib.pucminas.br/pergamum/biblioteca_s/php/login_usu.php')

    # Select the second (index one) form
    br.select_form(nr=0)

    # User credentials
    br.form['login'] = Usuario
    br.form['password'] = Senha

    br.submit()

    
    html = br.response().get_data()

    soup = BeautifulSoup(html)

    codigoreduzido = soup.find('input', {'id': 'id_codigoreduzido_anteriorPendente'}).get('value')
    #print value txt_cinza
    final=soup.findAll('a', {'class':'txt_azul'})

    nome = soup.find('div', {'id': 'nome'}).find('strong').text
    print nome
    d = datetime.utcnow()
    for_js = int(time.mktime(d.timetuple())) * 1000
    #print for_js

    for x in final:
        strin = str(x.get('href')).replace("javascript:renova", "").replace("(", "").replace(")", "").replace("\'", "")
        if len(strin) > 8:
            strin = strin.split(',');
            #print strin
            brow = mechanize.Browser()
            r= br.open('http://bib.pucminas.br/pergamum/biblioteca_s/meu_pergamum/index.php?flag=&rs=ajax_renova&rst=&rsrnd='+str(for_js)+'&rsargs[]='+str(strin[0])+'&rsargs[]='+str(strin[1])+'&rsargs[]='+str(strin[2])+'&rsargs[]='+str(codigoreduzido)+'')

    url = "http://bib.pucminas.br/pergamum/biblioteca_s/meu_pergamum/index.php?flag=";
    br.open(url)
    html = br.response().get_data()
    soup = BeautifulSoup(html)
    final= zip( soup.findAll('td', {'class':'txt_cinza'}), soup.findAll('td', {'class':'txt_azul_11'}))
    print "Livros Renovados. Novas Datas:"
    for x in final:
        print "\t"+x[0].text + " " + x[1].text.split('/')[0]
main()


























