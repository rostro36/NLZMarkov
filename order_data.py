import os
import re
import treetaggerwrapper

tagger = treetaggerwrapper.TreeTagger(TAGLANG='de')


def order(depths, query, path):
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
            currtext = tagger.tag_text(currtext)  #get words
            currtext = treetaggerwrapper.make_tags(
                currtext, exclude_nottags=True
            )  #get nice tags, throw away html artefacts/non-words
            #pad at the start and at the back, to get a start for the chain and an end. Go one too much for type look ahead.
            currtext = [
                treetaggerwrapper.Tag(word='£$', pos='START', lemma='START')
            ] * (depth + 1) + currtext + [
                treetaggerwrapper.Tag(word='$£', pos='ENDE', lemma='ENDE')
            ] * 2
            #prepare for nextpos; we now START will be the first part of speech.
            nextpos = 'START'
            #we dont need to run for the starting £$ and can only go to the first end sequence
            for currit in range(depth, len(currtext) - 1):
                #key consists of the previous words and the next part of speech given the current word.
                key = tuple((tuple(
                    ([currtext[currit - r].word for r in range(1, depth + 1)])),
                             currtext[currit].pos))
                #the entry is the current word, the next part of speech.
                entry = (currtext[currit].word, currtext[currit + 1].pos)
                if not key in currdict:  #add them to the choices array
                    currdict[key] = [entry]
                else:
                    currdict[key].append(entry)
        if counter % 10 == 0:  #dont print for every file
            print('@#ordered ' + str(counter + 1) + ' of ' + str(allfiles + 1))
        counter += 1

    print('@@ordering done')
    return dicts
