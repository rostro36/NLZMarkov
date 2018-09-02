import os
import re
import nltk


def orderNaive(depths, query, path, bar):
    dicts = (
        dict(), dict()
    )  #make dicts to store the possible choices given the previous words
    counter = 0
    allFiles = len(os.listdir(path))  #only used to give a time estimate
    for file in os.listdir(path):  #open each file exactly once
        f = open(path + file, 'r', encoding="utf-8")
        fileText = f.read()
        #fileText=bytes(fileText,'utf-8').decode('cp1252')
        fileText = re.split("\n", fileText)  #sections are split by linebreaks
        for sectionsIterator in range(len(depths)):  #go through sections
            depth = depths[
                sectionsIterator]  #use the sectionsIterator as the "working variables"
            currentDict = dicts[sectionsIterator]
            currentText = fileText[sectionsIterator]
            currentText = nltk.tokenize.word_tokenize(currentText)  #get words
            currentText = ['$START$'] * depth + currentText + [
                '$END$'
            ]  #£$ are used as startsymbols, $£ is a stop signal

            for currentIterator in range(
                    depth, len(currentText)
            ):  #make a index for every word (after startsymbols)
                key = tuple([
                    currentText[currentIterator - r]
                    for r in range(1, depth + 1)
                ])  #use the previous depth-many words as keys
                if not key in currentDict:  #add them to the choices array
                    currentDict[key] = [currentText[currentIterator]]
                else:
                    currentDict[key].append(currentText[currentIterator])
        if counter % 10 == 0:  #dont print for every file
            print('@#ordered ' + str(counter + 1) + ' of ' + str(allFiles + 1))
            if bar != None:
                bar.setValue((counter + 1) / (allFiles + 1) * 100)
        counter += 1
    print('@@ordering done')
    if bar != None:
        bar.setValue(100)
    return dicts
