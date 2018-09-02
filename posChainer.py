import random


def mkPOSchain(depths, dicts):
    sectionLists = []
    for sectionIterator in range(
            len(depths)
    ):  #there are possibly different sections (as of right now there are two)
        currentChainDepth = depths[sectionIterator]
        currentChain = dicts[
            sectionIterator]  #for different sections there are different chainpieces
        currentString = ['$START$'] * currentChainDepth  #start
        #we need a start variable for the chain; it is defined as ['£$', 'START']
        nextWord = ['$START$', 'START']
        while True:
            #find next possible words according to previous and the type for the next word described by the last word.
            nextChoices = currentChain[tuple((tuple(
                ([currentString[-r] for r in range(1, currentChainDepth + 1)])),
                                              nextWord[1]))]

            nextWord = nextChoices[random.randrange(
                len(nextChoices))]  #randomly choose one of the choices
            if nextWord[0] == '$END$':  #end signal
                break
            else:
                currentString.append(nextWord[0])  #append it to the end
        #currentString now looks pretty bad
        currentOutput = ''
        for word in currentString[(
                currentChainDepth +
                1):]:  #up to currentChainDepth+1 it is just start
            if word[0].isalpha() or word[0].isdigit():
                currentOutput += ' ' + word
            else:  #if it is only ,.;'
                currentOutput += word
        sectionLists.append(
            currentOutput)  #append sectionoutput to combination of others
        print('€@' + str(sectionIterator) + ': ' + currentOutput)
    return sectionLists
