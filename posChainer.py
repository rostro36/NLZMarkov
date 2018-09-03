import random


#makes repetition-many chains with the sectiondepths,
def goChainPOS(sectiondepths, dicts, repetition):
    result = ''
    #split title and the chains by a linebreak
    for i in range(repetition):
        results = mkPOSchain(sectiondepths, dicts)
        result += results[0]
        result += "\n"
        result += results[1]
        result += "\n"
    return result  #make the chain, returns string


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
