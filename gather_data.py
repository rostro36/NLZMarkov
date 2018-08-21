import urllib3
import io
import re
import os
import html
import urllib.parse as up

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning
                        )  #otherwise gives warnings I dont know how to fix.


def gather(query, path, bar):
    http = urllib3.PoolManager()
    URL = 'https://www.luzernerzeitung.ch/suche?form%5Bq%5D=' + up.quote_plus(
        query)
    r = http.request('GET', URL)  #get the actual site
    data = r.data.decode("utf-8")  #make it readable
    emptyflag = '<div class="searchresults__emptynotice">'
    if emptyflag in data:  #check if there is a result
        print('there are no results for your query')
        return 1

    data = re.sub('.*<span id="totalCounter">', '', data, 1,
                  re.DOTALL)  #determine how many results there are
    results = ''
    for char in data:
        if char == '<':
            break
        elif char.isdigit():
            results += char
    print('there are ' + results + ' results')

    number_of_pages = int(
        (int(results) - 1) / 10 +
        1)  #instead of math.ceil, determine how many sites of results there are
    for resultpage in range(1, number_of_pages + 1):
        resultdata = http.request(
            'GET', URL + '&page=' + str(resultpage))  #download the result page
        resultdata = resultdata.data.decode("utf-8")
        datas = re.split('<a class="teaser__link " href="', resultdata)
        pageid = 0
        for result in datas[
                1:]:  #go through the results given by the page of the results
            nextlink = ''  #build the next link to the actual article
            for char in result:
                if char != '"':  #" marks the end of the article URL
                    nextlink += char
                else:
                    break
            #print(resultpage,pageid,nextlink)
            site = http.request('GET', nextlink)  #download the article
            sitedata = site.data.decode("utf-8")
            sitedata = html.unescape(sitedata)  #decode the article properly

            sitedata = re.split('<div class="leadtext">', sitedata)
            if len(sitedata) >= 2:  #some sites dont have a leadtext
                sitedata = sitedata[1]  #filter out the leadtext
                sitetext = re.split('</div>', sitedata)[0]
            else:
                sitedata = sitedata[0]
                sitetext = " "
            sitetext += "\n"

            sitedatas = re.split(
                '<p class="text regwalled" itemprop="articleBody">',
                sitedata)  #filter out the main text
            for text in sitedatas[
                    1:]:  #there are possibly many sectons of the main text
                sitetext += up.unquote(text.split('</p>')[0])
                sitetext += ' '
            filename = path + str(resultpage).zfill(2) + str(
                pageid) + ".txt"  #filename to save
            os.makedirs(
                os.path.dirname(filename),
                exist_ok=True)  #make the directory, if it doesn't already exist
            with open(filename, "w", encoding="utf-8") as f:  #write it
                f.write(sitetext)
            pageid += 1
        print('##we have downloaded ' +
              str(min(int(results), resultpage * 10)) + ' of ' + results)
        #update progressbar in gui if given
        if bar != None:
            bar.setValue(
                min(int(results), resultpage * 10) / int(results) * 100)
    print('#@gather done')
    #update progressbar in gui if given
    if bar != None:
        bar.setValue(100)
    return 0
