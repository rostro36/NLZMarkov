import os
import re

mainchaindepth=3
titlechaindepth=2

query='quai churchill leinenpflicht initiative'
titlechain=dict()
mainchain=dict()
path=os.getcwd()+"/NLZMarkov/"+query+"/"
for file in os.listdir(path):
    f=open(path+file,'r')
    filetext=f.read()
    filetext=re.split("\n",filetext)
    #£$ is a startsymbol, whereas $£ is a stopsymbol
    titletext='£$ '*titlechaindepth+filetext[0]+' $£'
    maintext='£$ '*mainchaindepth+filetext[1]+' $£'

    titletext=re.split(" ",titletext)
    maintext=re.split(" ",maintext)
    for titleit in range(titlechaindepth,len(titletext)):
        key=tuple([titletext[titleit-r] for r in range(1,titlechaindepth+1)])
        if not key in titlechain:
            titlechain[key]=[titletext[titleit]]
        else:
            titlechain[key].append(titletext[titleit])
    for mainit in range(mainchaindepth,len(maintext)):
        key=tuple([maintext[mainit-r] for r in range(1,mainchaindepth+1)])
        if not key in mainchain:
            mainchain[key]=[maintext[mainit]]
        else:
            mainchain[key].append(maintext[mainit])
print('order done')
