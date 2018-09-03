## NLZMarkov
Markov chain based on articles of the "Neue Luzerner Zeitung".

### With two modes:
* one is a naive Markov chain that only depends on the previous words.
* the second is a part of speech enhanced variante, where the next word depends on the previous words and the type expected by the last given word.




### What possible to make better:
* the gui is not robust, because it doesn't use multithreading
* split the methods better, such that a module doesn't consist of just one method.

### What to do better next time:
* better names from the start.
* more methods.
* methods verbs, modules nouns.

### Used libraries:
* PyQt5
* urllib3
* urllib
* nltk
* treetagger(wrapper) and the german language package
* standard python libraries (i think)
