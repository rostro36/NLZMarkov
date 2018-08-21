import random


def posmkchain(depths, dicts):
    sectionlists = []
    for sectionit in range(
            len(depths)
    ):  #there are possibly different sections (as of right now there are two)
        currchaindepth = depths[sectionit]
        currchain = dicts[
            sectionit]  #for different sections there are different chainpieces
        currstring = ['£$'] * currchaindepth  #start
        #we need a start variable for the chain; it is defined as ['£$', 'START']
        nextword = ['£$', 'START']
        while True:
            #find next possible words according to previous and the type for the next word described by the last word.
            nextchoices = currchain[tuple((tuple(
                ([currstring[-r] for r in range(1, currchaindepth + 1)])),
                                           nextword[1]))]

            nextword = nextchoices[random.randrange(
                len(nextchoices))]  #randomly choose one of the choices
            if nextword[0] == '$£':  #end signal
                break
            else:
                currstring.append(nextword[0])  #append it to the end
        #currstring now looks pretty bad
        curroutput = ''
        for word in currstring[(
                currchaindepth + 1):]:  #up to currchaindepth+1 it is just start
            if word[0].isalpha() or word[0].isdigit():
                curroutput += ' ' + word
            else:  #if it is only ,.;'
                curroutput += word
        sectionlists.append(
            curroutput)  #append sectionoutput to combination of others
        print('€@' + str(sectionit) + ': ' + curroutput)
    return sectionlists
