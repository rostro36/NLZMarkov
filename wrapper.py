import os
from gatherer import gather
from posChainer import mkPOSchain
from posOrderer import orderPOS
from naiveChainer import mkNaiveChain
from naiveOrderer import orderNaive

#for better readable code
POS = 1
Naive = 0
Successful = 0
NoResults = 1
NoArticlesFound = 2
NoQuery = 3


#download query, get progress in bar
def wrapGather(query, bar):
    #'' gives a permission error in gather and makes no sense
    if query != '':
        path = os.getcwd() + "/" + query + "/"  #save of the articles
        if not os.path.isdir(path):  #check if articles already fetched
            return gather(query, path, bar)  #fetch them, store in path
        else:
            return Successful
    else:
        return NoQuery


#order query with sectiondepths, get progress in bar
def wrapOrderPOS(sectiondepths, query, bar):
    path = os.getcwd() + "/" + query + "/"
    return orderPOS(sectiondepths, query, path,
                    bar)  #order with depths, save in dicts


#makes repetition-many chains with the sectiondepths,
def wrapChainPOS(sectiondepths, dicts, repetition):
    result = ''
    #split title and the chains by a linebreak
    for i in range(repetition):
        results = mkPOSchain(sectiondepths, dicts)
        result += results[0]
        result += "\n"
        result += results[1]
        result += "\n"
    return result  #make the chain, returns string


#order query with sectiondepths, get progress in bar
def wrapOrderNaive(sectiondepths, query, bar):
    path = os.getcwd() + "/" + query + "/"
    return orderNaive(sectiondepths, query, path,
                      bar)  #order with depths, save in dicts


#makes repetition-many chains with the sectiondepths,
def wrapChainNaive(sectiondepths, dicts, repetition):
    result = ''
    #split title and the chains by a linebreak
    for i in range(repetition):
        results = mkNaiveChain(sectiondepths, dicts)
        result += results[0]
        result += "\n"
        result += results[1]
        result += "\n"
    return result  #make the chain, returns string
