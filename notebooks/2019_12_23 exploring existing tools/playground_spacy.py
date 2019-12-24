"""
    Exploring the spaCy NER items
"""

import spacy

article = '''
Asian shares skidded on Tuesday after a rout in tech stocks put Wall Street to the sword, while a 
sharp drop in oil prices and political risks in Europe pushed the dollar to 16-month highs as investors dumped 
riskier assets. MSCI’s broadest index of Asia-Pacific shares outside Japan dropped 1.7 percent to a 1-1/2 
week trough, with Australian shares sinking 1.6 percent. Japan’s Nikkei dived 3.1 percent led by losses in 
electric machinery makers and suppliers of Apple’s iphone parts. Sterling fell to $1.286 after three straight 
sessions of losses took it to the lowest since Nov.1 as there were still considerable unresolved issues with the
European Union over Brexit, British Prime Minister Theresa May said on Monday.'''

if __name__ == "__main__":
    print("Running spaCy")

    spacy_nlp = spacy.load('en')
    document = spacy_nlp(article)

    print('Original Sentence: %s' % (article))

    for element in document.ents:
        print('Type: %s, Value: %s' % (element.label_, element))
