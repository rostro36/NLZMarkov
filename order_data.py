import os
import re

def order(depths,query,path):
    dicts=[dict()]*len(depths)                                                  #make dicts to store the possible choices given the previous words
    counter=0
    allfiles=len(os.listdir(path))                                              #only used to give a time estimate
    for file in os.listdir(path):                                               #open each file exactly once
        f=open(path+file,'r')
        filetext=f.read()
        filetext=re.split("\n",filetext)                                        #sections are split by linebreaks
        for sectionsit in range(len(depths)):                                   #go through sections
            depth=depths[sectionsit]                                            #use the sectionsit as the "working variables"
            currdict=dicts[sectionsit]
            currtext='£$ '*depth+filetext[sectionsit]+' $£'                     #£$ are used as startsymbols, $£ is a stop signal
            currtext=re.split(" ",currtext)                                     #get words
            for currit in range(depth,len(currtext)):                           #make a index for every word (after startsymbols)
                key=tuple([currtext[currit-r] for r in range(1,depth+1)])       #use the previous depth-many words as keys
                if not key in currdict:                                         #add them to the choices array
                    currdict[key]=[currtext[currit]]
                else:
                    currdict[key].append(currtext[currit])
        if counter%10==0:                                                       #dont print for every file
            print('@#ordered '+str(counter+1)+' of '+str(allfiles+1))
        counter+=1
    print('@@ordering done')
    return dicts
