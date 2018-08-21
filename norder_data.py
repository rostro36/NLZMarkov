import os
import re
import nltk


def norder(depths, query, path, bar):
    dicts = [dict()] * len(
        depths
    )  #make dicts to store the possible choices given the previous words
    counter = 0
    allfiles = len(os.listdir(path))  #only used to give a time estimate
    for file in os.listdir(path):  #open each file exactly once
        f = open(path + file, 'r', encoding="utf-8")
        filetext = f.read()
        #filetext=bytes(filetext,'utf-8').decode('cp1252')
        filetext = re.split("\n", filetext)  #sections are split by linebreaks
        for sectionsit in range(len(depths)):  #go through sections
            depth = depths[
                sectionsit]  #use the sectionsit as the "working variables"
            currdict = dicts[sectionsit]
            currtext = filetext[sectionsit]
            currtext = nltk.tokenize.word_tokenize(currtext)  #get words
            currtext = ['£$'] * depth + currtext + [
                '$£'
            ]  #£$ are used as startsymbols, $£ is a stop signal

            for currit in range(
                    depth, len(currtext)
            ):  #make a index for every word (after startsymbols)
                key = tuple([currtext[currit - r] for r in range(1, depth + 1)
                            ])  #use the previous depth-many words as keys
                if not key in currdict:  #add them to the choices array
                    currdict[key] = [currtext[currit]]
                else:
                    currdict[key].append(currtext[currit])
        if counter % 10 == 0:  #dont print for every file
            print('@#ordered ' + str(counter + 1) + ' of ' + str(allfiles + 1))
            if bar != None:
                bar.setValue((counter + 1) / (allfiles + 1) * 100)
        counter += 1
    print('@@ordering done')
    if bar != None:
        bar.setValue(100)
    return dicts
