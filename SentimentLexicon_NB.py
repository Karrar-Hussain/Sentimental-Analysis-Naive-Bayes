'''
Created on Oct 21, 2016

@author: Karrar
'''
import re
import os
import math, collections
class SentimentLexicon_NB(object):
    '''
    classdocs
    '''

    
    def __init__(self):
        self.conj_pat='and|or|but|nor|so|for|yet'
        self.not_pat='(\w+n\'t)|(\s?not)|(never)'
        self.punc_pat='\,|\.|\?|\:|\!|\;'
        self.lexiconDic=collections.defaultdict(lambda:0)
        self.reviews=[]
        self.train()
    def train(self):
        lexiconFile="./data/sub.tff"
        lexiconF=open(lexiconFile)

        val=0
        type_pat='type=(\w+)'
        word_pat='word1=(\w+)'
        priorpolarity='priorpolarity=(\w+)'
        for line in lexiconF:
            type_found=re.findall(type_pat, line)
            word_found=re.findall(word_pat, line)
            prior_found=re.findall(priorpolarity, line)
            val+=1
            if(len(type_found)>0):
                type= '%s' % type_found
            if(len(word_found)>0):
                word= '%s' % word_found
            if(len(prior_found)>0):
                prior= '%s' % prior_found
            stri=""
            for s in list(type):
                if(s!='[' and s!=']' and s!='\''):
                    stri+=s
            if(stri=="weaksubj"):
                weight=1
            else:
                weight=2
            stri=""
            for s in list(word):
                if(s!='[' and s!=']' and s!='\''):
                    stri+=s
            words=stri
            stri=""
            for s in list(prior):
                if(s!='[' and s!=']' and s!='\''):
                    stri+=s
            if(stri=="negative"):
                weight=weight * -1
            self.lexiconDic[words]=weight
    def readReviews(self):
        negFiles="./data/imdb1/neg"
        posFiles="./data/imdb1/pos"
        
        for file in os.listdir(negFiles):
            if file.endswith(".txt"):
                f = open(negFiles+"/"+file)
                sentence=""
                for line in f:
                    line = line.strip()
                    line = line.lower() 
                    line = line.replace('"','')
                    line = line.replace('(','')
                    line = line.replace(')','')
                    sentence += line.lower()
                self.reviews.append((sentence,"Neg"))
        
        for file in os.listdir(posFiles):
            if file.endswith(".txt"):
                f = open(posFiles+"/"+file)
                sentence=""
                for line in f:
                    line = line.strip()
                    line = line.lower() 
                    line = line.replace('"','')
                    line = line.replace('(','')
                    line = line.replace(')','')
                    sentence += line.lower()
                self.reviews.append((sentence,"Pos"))
    def buildMicroPhrase(self):
        micro_phrase=[]
        micro_word=[]
        result=i=score=0
        for (words,sent) in self.reviews:
            words_filtered = [e.lower() for e in words.split() if len(e) >= 1]
            bol=False
            score=0
            i+=1
            for word in words_filtered:
                foundConj=re.findall(self.conj_pat, word)
                foundPunc=re.findall(self.punc_pat, word)
                if(len(foundConj)>0 or len(foundPunc)>0):
                        #if(word=='.' or word==',' or word==':'or word==';' or word=='?' or word=='!'or word=='nor' or word=='or'or word=='and' or word=='for'or word=='but' or word=='yet'or word=='so'):
                    if(len(micro_word)>0):
                        micro_phrase.append((micro_word,i))
                        #print(":::: i=",i,micro_word)
                    micro_word=[]
                    #print("--------------->>>",word,micro_phrase)
                else:
                    micro_word.append(word)
                    #print("---------->>>>>>",micro_word)
        self.BasicPolarity(micro_phrase)
        v=input("Continue...")
        self.NormalizedPolarity(micro_phrase)        
    def BasicPolarity(self,micro_phrases):
        
        score=result=neutral=0
        num=1                
        for(microPhrase,i) in micro_phrases:
            if(num!=i):
                finalScore=score
                score=0
            bol=False
            for w in microPhrase:
                if(bol):
                    score+=-1*self.lexiconDic[w]
                else:
                    found=re.findall(self.not_pat, w)
                    if(len(found)>0):
                        bol=True    
                    else:
                        score+=self.lexiconDic[w]
            if(num!=i):
                num=i
                if(finalScore<0):
                    #print("The Doc is : Positive +ve",sent)
                    if(i<1000):
                        result+=1
                        print("TP:The Doc is Negative -ve i =",i," Score=",finalScore)
                    else:
                        print("FP:The Doc is Psitive +ve" ,i," Score=",finalScore)
                    
                elif(finalScore>0):
                    #print("The Doc is : Negative ----ve",sent)
                    if(i>=1000):
                        print("TP:The Doc is Positive i =",i," Score=",finalScore)
                        result+=1
                    else:
                        print("FP:The Doc is Negative -ve" , i," Score=",finalScore)
                else:
                    print("Un Identified Object Doc is Neutral +-ve")
                    neutral+=1    
        accuracy=(result/len(self.reviews))*100
        print("Accuracy:Basic Polarity " ,accuracy,"Neutrals Doc=",neutral,"TP: ",result, "Total doc ",len(self.reviews))
    def NormalizedPolarity(self,micro_phrases):
        
        score=result=neutral=0
        num=1                
        for(microPhrase,i) in micro_phrases:
            if(num!=i):
                finalScore=score
                score=0
            bol=False
            for w in microPhrase:
                if(bol):
                    score-=self.lexiconDic[w]/len(microPhrase)
                else:
                    found=re.findall(self.not_pat, w)
                    if(len(found)>0):
                        bol=True    
                    else:
                        score+=self.lexiconDic[w]/len(microPhrase)
            if(num!=i):
                num=i
                if(finalScore<0):
                    #print("The Doc is : Positive +ve",sent)
                    if(i<1000):
                        result+=1
                        print("TP:The Doc is Negative -ve i =",i," Score=",finalScore)
                    else:
                        print("FP:The Doc is Psitive +ve" ,i," Score=",finalScore)
                    
                elif(finalScore>0):
                    #print("The Doc is : Negative ----ve",sent)
                    if(i>=1000):
                        print("TP:The Doc is Positive i =",i," Score=",finalScore)
                        result+=1
                    else:
                        print("FP:The Doc is Negative -ve" , i," Score=",finalScore)
                else:
                    print("Un Identified Object Doc is Neutral +-ve")
                    neutral+=1    
        accuracy=(result/len(self.reviews))*100
        print("Accuracy:Normalized Polarity " ,accuracy,"Neutrals Doc=",neutral,"TP: ",result, "Total doc ",len(self.reviews))
   
def main():
    
    obj=SentimentLexicon_NB()
    obj.readReviews()
    obj.buildMicroPhrase()
    
    
if __name__ == "__main__":
    main()