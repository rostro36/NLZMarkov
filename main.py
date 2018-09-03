#from wrapper import wrapGather, wrapChainNaive, wrapChainPOS, wrapOrderPOS, wrapOrderNaive
from gatherer import goGather
from naiveOrderer import goOrderNaive
from naiveChainer import goChainNaive
from posOrderer import goOrderPOS
from posChainer import goChainPOS
query = 'quai churchill leinenpflicht initiative'  #fill in your own query
sectiondepths = [1, 1]  #[title,main]

repetition = 2

#0 is naive, 1 is PoS
mode = 0

#for better readable code
POS = 1
Naive = 0
Successful = 0
NoResults = 1
NoArticlesFound = 2
NoQuery = 3

success = goGather(query, None)
#check how the gathering worked out
if (success == Successful):
    #it was successful
    #decide if PoS or naive.
    if mode == POS:
        print('yeah')
        goChainPOS(sectiondepths, goOrderPOS(sectiondepths, query, None),
                   repetition)
    elif mode == Naive:
        goChainNaive(sectiondepths, goOrderNaive(sectiondepths, query, None),
                     repetition)
elif (success == NoResults):
    print('There are no results for the query.')
elif (success == NoArticlesFound):
    print('Cant reach articles on net.')
elif (success == NoQuery):
    print('No query word given.')
