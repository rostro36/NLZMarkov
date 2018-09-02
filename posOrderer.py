import os
import re
import treetaggerwrapper

tagger = treetaggerwrapper.TreeTagger(TAGLANG='de')


def orderPOS(depths, query, path, bar):
    dicts = [dict()] * len(
        depths
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
            currentText = tagger.tag_text(currentText)  #get words
            currentText = treetaggerwrapper.make_tags(
                currentText, exclude_nottags=True
            )  #get nice tags, throw away html artefacts/non-words
            #pad at the start and at the back, to get a start for the chain and an end. Go one too much for type look ahead.
            currentText = [
                treetaggerwrapper.Tag(
                    word='$START$', pos='START', lemma='START')
            ] * (depth + 1) + currentText + [
                treetaggerwrapper.Tag(word='$END$', pos='ENDE', lemma='ENDE')
            ] * 2
            #prepare for nextpos; we now START will be the first part of speech.
            ################nextpos = 'START'
            #we dont need to run for the starting £$ and can only go to the first end sequence
            for currit in range(depth, len(currentText) - 1):
                #key consists of the previous words and the next part of speech given the current word.
                key = tuple((tuple(([
                    currentText[currit - r].word for r in range(1, depth + 1)
                ])), currentText[currit].pos))
                #the entry is the current word, the next part of speech.
                entry = (currentText[currit].word, currentText[currit + 1].pos)
                if not key in currentDict:  #add them to the choices array
                    currentDict[key] = [entry]
                else:
                    currentDict[key].append(entry)
        if counter % 10 == 0:  #dont print for every file
            print('@#ordered ' + str(counter + 1) + ' of ' + str(allFiles + 1))
            #update progressbar in gui if given
            if bar != None:
                bar.setValue((counter + 1) / (allFiles + 1) * 100)
        counter += 1

    print('@@ordering done')
    #update progressbar in gui if given
    if bar != None:
        bar.setValue(100)
    return dicts
