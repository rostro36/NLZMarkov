import urllib3
import io
import re
import os
import html
import urllib.parse as up

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning
                        )  #otherwise gives warnings I dont know how to fix.
#local variables easier to read
Successful = 0
NoResults = 1
NoArticlesFound = 2
NoQuery = 3


def goGather(query, bar):
    #'' gives a permission error in gather and makes no sense
    if query != '':
        path = os.getcwd() + "/" + query + "/"  #save of the articles
        if not os.path.isdir(path):  #check if articles already fetched
            return gather(query, path, bar)  #fetch them, store in path
        else:
            return Successful
    else:
        return NoQuery


def gather(query, path, bar):
    http = urllib3.PoolManager()
    URL = 'https://www.luzernerzeitung.ch/suche?form%5Bq%5D=' + up.quote_plus(
        query)
    #check if internet works as it should
    try:
        r = http.request('GET', URL)  #get the actual site
    except Exception as ex:
        print(ex)
        return NoArticlesFound
    data = r.data.decode("utf-8")  #make it readable

    emptyFlag = '<div class="searchresults__emptynotice">'
    if emptyFlag in data:  #check if there is a result
        print('there are no results for your query')
        return NoResults

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
    for resultPage in range(1, number_of_pages + 1):
        try:
            resultData = http.request(
                'GET',
                URL + '&page=' + str(resultPage))  #download the result page
        except Exception as ex:
            print(ex)
            return NoArticlesFound
        resultData = resultData.data.decode("utf-8")
        datas = re.split('<a class="teaser__link " href="', resultData)
        pageID = 0
        for result in datas[
                1:]:  #go through the results given by the page of the results
            nextLink = ''  #build the next link to the actual article
            for char in result:
                if char != '"':  #" marks the end of the article URL
                    nextLink += char
                else:
                    break
            #print(resultPage,pageID,nextLink)
            site = http.request('GET', nextLink)  #download the article
            siteData = site.data.decode("utf-8")
            siteData = html.unescape(siteData)  #decode the article properly

            siteData = re.split('<div class="leadtext">', siteData)
            if len(siteData) >= 2:  #some sites dont have a leadtext
                siteData = siteData[1]  #filter out the leadtext
                siteText = re.split('</div>', siteData)[0]
            else:
                siteData = siteData[0]
                siteText = " "
            siteText += "\n"

            siteDatas = re.split(
                '<p class="text regwalled" itemprop="articleBody">',
                siteData)  #filter out the main text
            for text in siteDatas[
                    1:]:  #there are possibly many sectons of the main text
                siteText += up.unquote(text.split('</p>')[0])
                siteText += ' '
            filename = path + str(resultPage).zfill(2) + str(
                pageID) + ".txt"  #filename to save
            os.makedirs(
                os.path.dirname(filename),
                exist_ok=True)  #make the directory, if it doesn't already exist
            with open(filename, "w", encoding="utf-8") as f:  #write it
                f.write(siteText)
            pageID += 1
        print('##we have downloaded ' +
              str(min(int(results), resultPage * 10)) + ' of ' + results)
        #update progressbar in gui if given
        if bar != None:
            bar.setValue(
                min(int(results), resultPage * 10) / int(results) * 100)
    print('#@gather done')
    #update progressbar in gui if given
    if bar != None:
        bar.setValue(100)
    return Successful
