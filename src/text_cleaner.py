import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


class TextCleaning:
    """ Classe pour realiser le 'netoyage' du texte """

    def remove_non_ascii(self, string):
        '''
        Description: fonction qui enleve les characteres 
        non-ascii du texte
        Sortie: texte sans les charachteres non ascii
        '''
        stripped = (c for c in string if 0 < ord(c) < 127)
        return "".join(stripped)

    def remove_non_letters(self, string):
        '''
        Description: fonction qui enleve tout les 
        characteres qui ne sont pas les letteres 
        (i.e punctuation, chiffres )
        Sortie: texte sans les chiffres et characteres speciales 
        '''
        string = re.sub(r"[^a-zA-Z]", " ", string)
        return string

    def stem_words(self, string):
        '''
        Description: fonction qui fait le 'stemming' 
        des mots. 
        Sortie: dictionare avec les utilisateurs 
        '''
        ps = PorterStemmer()
        string = [ps.stem(word) for word in string]
        return string

    def remove_stop_words(self, string):
        '''
        Description: fonction qui enleve les mots
        'sans imprtance' tel que les pronoms, prepositions, conjunctions, etc.
        Sortie: texte sans les 'stop-words'
        '''
        stop_words = set(stopwords.words("english"))
        string = [
            word for word in string if (word not in stop_words) and (len(word) > 2)
        ]
        return string

    def tokenize_words(self, string):
        '''
        Description: fonction qui produit un liste de mots du texte
        Sortie: liste des mots dans le texte
        '''
        return string.split()

    def clean_text(self, text):
        '''
        Description: fonction qui gere le netoyage du texte
        Sortie: texte 'propre'
        '''
        text = text.lower()
        text = self.remove_non_letters(text)
        text = self.remove_non_ascii(text)
        text = self.tokenize_words(text)
        text = self.remove_stop_words(text)
        text = self.stem_words(text)
        return text
