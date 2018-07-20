import random

def mkchain(depths,dicts):
    sectionlists=[]
    for sectionit in range(len(depths)):                                        #there are possibly different sections (as of right now there are two)
        currchaindepth=depths[sectionit]
        currchain=dicts[sectionit]                                              #for different sections there are different chainpieces
        currstring=['£$']*currchaindepth                                        #start
        while True:
            nextchoices=currchain[tuple([currstring[-r] for r in range(1,currchaindepth+1)])] #find next possible words according to previous
            nextword=nextchoices[random.randrange(len(nextchoices))]            #randomly choose one of the choices
            if nextword =='$£':                                                 #end signal
                break
            else:
                currstring.append(nextword)                                     #append it to the end
        #currstring now looks pretty bad
        curroutput=''
        for word in currstring[currchaindepth:]:                                #up to currchaindepth it is just start
            curroutput+=word+' '
        curroutput= curroutput[:-1]                                             #delete the last blank
        sectionlists.append(curroutput)                                         #append sectionoutput to combination of others
        print('€@'+str(sectionit)+': '+curroutput)
    return sectionlists
