import os
from gather_data import gather
from poschain import posmkchain
from posorder_data import posorder
from nchain import nmkchain
from norder_data import norder

query = ''  #fill in your own query
sectiondepths = [2, 3]  #[title,main]

repetition = 3

#0 is naive, 1 is PoS
mode = 1


#download query, get progress in bar
def goGather(query, bar):
    #'' gives a permission error in gather and makes no sense
    if query != '':
        path = os.getcwd() + "/" + query + "/"  #save of the articles
        if not os.path.isdir(path):  #check if articles already fetched
            return gather(query, path, bar)  #fetch them, store in path
        else:
            return 0
    else:
        return 3


#order query with sectiondepths, get progress in bar
def goposOrder(sectiondepths, query, bar):
    path = os.getcwd() + "/" + query + "/"
    return posorder(sectiondepths, query, path,
                    bar)  #order with depths, save in dicts


#makes repetition-many chains with the sectiondepths,
def goposChain(sectiondepths, dicts, repetition):
    result = ''
    #split title and the chains by a linebreak
    for i in range(repetition):
        result += posmkchain(sectiondepths, dicts)[0]
        result += "\n"
        result += posmkchain(sectiondepths, dicts)[1]
        result += "\n"
    return result  #make the chain, returns string


#order query with sectiondepths, get progress in bar
def gonOrder(sectiondepths, query, bar):
    path = os.getcwd() + "/" + query + "/"
    return norder(sectiondepths, query, path,
                  bar)  #order with depths, save in dicts


#makes repetition-many chains with the sectiondepths,
def gonChain(sectiondepths, dicts, repetition):
    result = ''
    #split title and the chains by a linebreak
    for i in range(repetition):
        result += nmkchain(sectiondepths, dicts)[0]
        result += "\n"
        result += nmkchain(sectiondepths, dicts)[1]
        result += "\n"
    return result  #make the chain, returns string


#exec if no gui, kinda funky style but enables easier gui
if __name__ == '__main__':
    success = goGather(query, None)
    #check how the gathering worked out
    if (success == 0):
        #it was successful
        #decide if PoS or naive.
        if mode == 1:
            goposChain(sectiondepths, goposOrder(sectiondepths, query, None),
                       repetition)
        elif mode == 0:
            gonChain(sectiondepths, gonOrder(sectiondepths, query, None),
                     repetition)
    elif (success == 1):
        print('There are no results for the query.')
    elif (success == 2):
        print('Cant reach articles on net.')
    elif (success == 3):
        print('No query word given.')
