'''
kill all autocomplete
'''

import urllib3
import io
import re
import os
import html
import urllib.parse as up

query=''

http=urllib3.PoolManager()
URL='https://www.luzernerzeitung.ch/suche?form%5Bq%5D='+up.quote_plus(query)
r=http.request('GET',URL)
data=r.data.decode("utf-8")
emptyflag='<div class="searchresults__emptynotice">'
if emptyflag in data:
    print('there are no results for your query')
    quit()
data=re.sub('.*<span id="totalCounter">','',data,1,re.DOTALL)

results=''
for char in data:
    if char=='<':
        break
    elif char.isdigit():
        results+=char
print('there are '+results+' results')

number_of_pages=int((int(results)-1)/10+1)                                      #instead of math.ceil
for resultpage in range(1,number_of_pages+1):
    print(resultpage)
    resultdata=http.request('GET',URL+'&page='+str(resultpage))
    resultdata=resultdata.data.decode("utf-8")
    datas=re.split('<a class="teaser__link " href="',resultdata)
    pageid=0
    for result in datas[1:]:
        nextlink=''
        for char in result:
            if char !='"':
                nextlink+=char
            else:
                break
        print(resultpage,pageid,nextlink)
        site=http.request('GET',nextlink)
        sitedata=site.data.decode("utf-8")
        sitedata=html.unescape(sitedata)

        sitedata=re.split('<div class="leadtext">',sitedata)[1]
        sitetext=re.split('</div>',sitedata)[0]
        sitetext+="\n"

        sitedatas=re.split('<p class="text regwalled" itemprop="articleBody">',sitedata)
        for text in sitedatas[1:]:
            sitetext+=up.unquote(text.split('</p>')[0])
            sitetext+=' '
        filename = os.getcwd()+"/NLZMarkov/"+query+"/"+str(resultpage).zfill(2)+str(pageid)+".txt"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            f.write(sitetext)
        pageid+=1
    print('###we have written to '+str(resultpage*10)+' of '+str(results))
print('all done')
