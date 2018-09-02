import random


def mkNaiveChain(depths, dicts):
    sectionLists = []
    for sectionIterator in range(
            len(depths)
    ):  #there are possibly different sections (as of right now there are two)
        currentChaindepth = depths[sectionIterator]
        currentChain = dicts[
            sectionIterator]  #for different sections there are different chainpieces
        currentString = ['£$'] * currentChaindepth  #start
        while True:
            nextChoices = currentChain[tuple([
                currentString[-r] for r in range(1, currentChaindepth + 1)
            ])]  #find next possible words according to previous
            nextWord = nextChoices[random.randrange(
                len(nextChoices))]  #randomly choose one of the choices
            if nextWord == '$£':  #end signal
                break
            else:
                currentString.append(nextWord)  #append it to the end
        #currentString now looks pretty bad
        currentOutput = ''
        for word in currentString[
                currentChaindepth:]:  #up to currentChaindepth it is just start
            if word[0].isalpha() or word[0].isdigit():
                currentOutput += ' ' + word
            else:  #if it is only ,.;'
                currentOutput += word
        sectionLists.append(
            currentOutput)  #append sectionoutput to combination of others
        print('€@' + str(sectionIterator) + ': ' + currentOutput)
    return sectionLists