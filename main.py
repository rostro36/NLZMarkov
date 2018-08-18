import os
from chain import mkchain
from gather_data import gather
from order_data import order

query = ''  #fill in your own query
sectiondepths = [1, 2]  #[title,main]
path = os.getcwd() + "/" + query + "/"  #save of the articles
if not os.path.isdir(path):  #check if articles already fetched
    gather(query, path)  #fetch them, store in path
dicts = order(sectiondepths, query, path)  #order with depths, save in dicts
mkchain(sectiondepths, dicts)  #make the chain, returns [strings]
