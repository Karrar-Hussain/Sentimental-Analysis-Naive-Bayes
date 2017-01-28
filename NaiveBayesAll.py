'''
Created on Oct 16, 2016
This file contents all function of naive bayes 
Multinomial naive bayes 
Multinomial naive bayes with stop words 
Multinomial naive bayes with NOT_ words
Multinomial naive bayes with stop words and NOT_words


@author: Karrar
'''
import re
import os
import math, collections
class NaiveBayesAll:

    def __init__(self,testVal,choice):
        """Initialize your data structures in the constructor."""
        self.Nc=collections.defaultdict(lambda: 0)
        self.wordCountClass=collections.defaultdict(lambda: 0)
        self.probWordClass=collections.defaultdict(lambda: 0.0)
        self.vocabulary=set()
        self.testDoc=[] 
        self.negDocCount=0
        self.posDocCount=0
        self.totalDoc=0
        self.posTweets=[]
        self.negTweets=[]
        self.totalW=0
        self.totalPosWord=0
        self.totalNegWord=0
        self.probPosClass=0.0
        self.probNegClass=0
        self.stopWords=collections.defaultdict(lambda: 0)
        self.not_pat='(\w+n\'t)|(\s?not)|(never)'
        self.readStopWrod()
        self.train(testVal,choice)
        

    def readStopWrod(self):
        f=open('./data/english.stop')
        
        for line in f:
            line=line.strip()
            line=line.replace('\n','')
            self.stopWords[line]=1
        #print("length of : ",len(stopWords),stopWords)    
    def SimpleNaiveBayes(self):
        tweets = []
        #stopWords=self.readStopWrod()
        for (words, sentiment) in self.posTweets + self.negTweets:
            words_filtered = [e.lower() for e in words.split() if len(e) >= 1]
            tweets.append((words_filtered, sentiment))
        for (words,sent) in tweets:
            for word in words:
                self.vocabulary.add(word)
                self.totalW+=1
                #print("Word is the key: ",word)
        for (words,sent) in self.posTweets:
            words_filtered = [e.lower() for e in words.split() if len(e) >= 1]
            for word in words_filtered:
                self.wordCountClass[(word,"Pos")]+=1
                self.totalPosWord+=1
        for (words,sent) in self.negTweets:
            words_filtered = [e.lower() for e in words.split() if len(e) >= 1]
            for word in words_filtered:
                self.wordCountClass[(word,"Neg")]+=1
                self.totalNegWord+=1
    def StopWords(self):
        tweets = []
        #stopWords=self.readStopWrod()
        for (words, sentiment) in self.posTweets + self.negTweets:
            words_filtered = [e.lower() for e in words.split() if len(e) >= 1]
            tweets.append((words_filtered, sentiment))
        for (words,sent) in tweets:
            for word in words:
                if(self.stopWords[word]!=1):
                    self.vocabulary.add(word)
                    self.totalW+=1
                #print("Word is the key: ",word)
        for (words,sent) in self.posTweets:
            words_filtered = [e.lower() for e in words.split() if len(e) >= 1]
            for word in words_filtered:
                if(self.stopWords[word]!=1):
                    self.wordCountClass[(word,"Pos")]+=1
                    self.totalPosWord+=1
        for (words,sent) in self.negTweets:
            words_filtered = [e.lower() for e in words.split() if len(e) >= 1]
            for word in words_filtered:
                if(self.stopWords[word]!=1):
                    self.wordCountClass[(word,"Neg")]+=1
                    self.totalNegWord+=1
    def NotWords(self):
        tweets = []
        #words_filtered=[([],)]
        for (words, sentiment) in self.posTweets + self.negTweets:
            words_filtered = [e.lower() for e in words.split() if len(e) >= 1]
            tweets.append((words_filtered, sentiment))
                #print(file)
        for (words,sent) in tweets:
            bol=False
            for word in words:
                if(word=='.' or word==',' or word=='?' or word=='?'):
                    bol=False
                elif(bol ):
                    word="NOT_"+word
                    #print("------>>>>>>>>>>>>>>>>>>>>",word)
                elif(bol==False): 
                    found=re.findall(self.not_pat, word)
                    if len(found)>0:
                        bol=True
                self.vocabulary.add(word)
                self.totalW+=1
        for (words,sent) in self.posTweets:
            words_filtered = [e.lower() for e in words.split() if len(e) >= 1]
            bol=False
            for word in words_filtered:
                if(word=='.' or word==',' or word=='?' or word=='!'):
                    bol=False
                elif(bol ):
                    word="NOT_"+word
                    #print("------>>>>>>>>>>>>>>>>>>>>",word)
                elif(bol==False): 
                    found=re.findall(self.not_pat, word)
                    if len(found)>0:
                        bol=True
                self.wordCountClass[(word,"Pos")]+=1
                self.totalPosWord+=1
        #my_first_pat = '(\w+)\s*(?:@|@-|&#x40;)\s*(\w+)\s*((?:.|dot|dt)\w+)*\s*(?:.|dot|dt)edu'
        for (words,sent) in self.negTweets:
            words_filtered = [e.lower() for e in words.split() if len(e) >= 1]
            bol=False
            for word in words_filtered:
                if(word=='.' or word==',' or word=='?' or word=='!'):
                    bol=False
                elif(bol ):
                    word="NOT_"+word
                    #print("------>>>>>>>>>>>>>>>>>>>>",word)
                elif(bol==False): 
                    found=re.findall(self.not_pat, word)
                    if(len(found)>0):
                        bol=True
                self.wordCountClass[(word,"Neg")]+=1
                self.totalNegWord+=1
        
    def StopWordsAnd_Not(self):
        tweets = []
        
        for (words, sentiment) in self.posTweets + self.negTweets:
            words_filtered = [e.lower() for e in words.split() if len(e) >= 1]
            tweets.append((words_filtered, sentiment))
        for (words,sent) in tweets:
            bol=False
            for word in words:
                if(self.stopWords[word]!=1):
                    if(word=='.' or word==',' or word=='?' or word=='!'):
                        bol=False
                    elif(bol ):
                        word="NOT_"+word
                        #print("------>>>>>>>>>>>>>>>>>>>>",word)
                    elif(bol==False): 
                        found=re.findall(self.not_pat, word)
                        if len(found)>0:
                            bol=True
                    self.vocabulary.add(word)
                    self.totalW+=1
                #print("Word is the key: ",word)
        for (words,sent) in self.posTweets:
            words_filtered = [e.lower() for e in words.split() if len(e) >= 1]
            bol=False
            for word in words_filtered:
                if(self.stopWords[word]!=1):
                    if(word=='.' or word==',' or word=='?' or word=='!'):
                        bol=False
                    elif(bol ):
                        word="NOT_"+word
                        #print("------>>>>>>>>>>>>>>>>>>>>",word)
                    elif(bol==False): 
                        found=re.findall(self.not_pat, word)
                        if len(found)>0:
                            bol=True
                    self.wordCountClass[(word,"Pos")]+=1
                    self.totalPosWord+=1
        for (words,sent) in self.negTweets:
            words_filtered = [e.lower() for e in words.split() if len(e) >= 1]
            bol=False
            for word in words_filtered:
                if(self.stopWords[word]!=1):
                    if(word=='.' or word==',' or word=='?' or word=='!'):
                        bol=False
                    elif(bol ):
                        word="NOT_"+word
                        #print("------>>>>>>>>>>>>>>>>>>>>",word)
                    elif(bol==False): 
                        found=re.findall(self.not_pat, word)
                        if(len(found)>0):
                            bol=True
                    self.wordCountClass[(word,"Neg")]+=1
                    self.totalNegWord+=1
    def train(self,testVal,choice):
        posFiles="./data/imdb1/pos"
        negFiles="./data/imdb1/neg"
        test=0
        i=0
        val=testVal
        for file in os.listdir(negFiles):
            if file.endswith(".txt"):
                self.negDocCount+=1
                f = open(negFiles+"/"+file)
                sentence=""
                for line in f:
                    sentence += line.lower()
                test=10*len(os.listdir(negFiles))/100
                if i<test+val and i>val:
                    self.testDoc.append(sentence)
                    #print("Test Valuesssss; "+sentence,test)
                else:
                    self.negTweets.append((sentence,"Neg"))
                i+=1
        test=0
        i=0
        for file in os.listdir(posFiles):
            if file.endswith(".txt"):
                self.posDocCount+=1
                f = open(posFiles+"/"+file)
                sentence=""
                for line in f:
                    sentence += line.lower()
                test=10*len(os.listdir(negFiles))/100
                if i<test+val and i>val:
                    self.testDoc.append(sentence)
                    #print("Test Valuesssss;>>Positive::: "+sentence,test)
                else:
                    self.posTweets.append((sentence,"Pos"))
                i+=1
        if(choice==1):  
            self.SimpleNaiveBayes()
        elif(choice==2):
            self.StopWords()
        elif(choice==3):
            self.NotWords()
        else:    
            self.StopWordsAnd_Not()
        self.totalDoc=self.negDocCount+self.posDocCount
        self.probPosClass=self.posDocCount/self.totalDoc
        self.probNegClass=self.negDocCount/self.totalDoc
        print("Total Vocabulary: Words > ",len(self.vocabulary), self.totalW)
        print("Total Class doc Count Neg, Pos, total:",self.negDocCount,self.posDocCount,self.totalDoc )
    def postProb(self,word):
        scoreP=math.log((self.wordCountClass[(word,"Pos")]+1)/(len(self.vocabulary)+self.totalPosWord))
        scoreN=math.log((self.wordCountClass[(word,"Neg")]+1)/(len(self.vocabulary)+self.totalNegWord))
        return scoreP,scoreN
    def classifyDocNaiveBayes(self,doc):
        scoreP=math.log(self.probPosClass)
        scoreN=math.log(self.probNegClass)
        words_filtered = [e.lower() for e in doc.split() if len(e) >= 1]
        for word in words_filtered:     
            P,N=self.postProb(word) 
            scoreP+=P
            scoreN+=N
        return scoreP,scoreN
    def classifyDocSTOP_WORD(self,doc):
        scoreP=math.log(self.probPosClass)
        scoreN=math.log(self.probNegClass)
        words_filtered = [e.lower() for e in doc.split() if len(e) >= 1]
        for word in words_filtered:            
            if(self.stopWords[word]!=1):
                P,N=self.postProb(word) 
                scoreP+=P
                scoreN+=N
        return scoreP,scoreN
    def classifyDocNOT_WORD(self,doc):
        scoreP=math.log(self.probPosClass)
        scoreN=math.log(self.probNegClass)
        words_filtered = [e.lower() for e in doc.split() if len(e) >= 1]
        bol=False
        for word in words_filtered:            
            if(word=='.' or word==',' or word=='?'or word=='!'):
                bol=False
            elif(bol ):
                word="NOT_"+word
            elif(bol==False): 
                found=re.findall(self.not_pat, word)
                if len(found)>0:
                    bol=True
            P,N=self.postProb(word) 
            scoreP+=P
            scoreN+=N    
        return scoreP,scoreN
    def classifyDocNOTAndSTOP_WORD(self,doc):
        scoreP=math.log(self.probPosClass)
        scoreN=math.log(self.probNegClass)
        #words_filtered = set([e.lower() for e in doc.split() if len(e) >= 1])
        words_filtered = [e.lower() for e in doc.split() if len(e) >= 1]
        bol=False
        for word in words_filtered:
            if(self.stopWords[word]!=1):            
                if(word=='.' or word==',' or word=='?' or word=='!'):
                    bol=False
                elif(bol ):
                    word="NOT_"+word
                elif(bol==False): 
                    found=re.findall(self.not_pat, word)
                    if len(found)>0:
                        bol=True
                P,N=self.postProb(word) 
                scoreP+=P
                scoreN+=N
        return scoreP,scoreN
    def testNB(self,testVal,choice):
        scoreP=scoreN=0
        result=0
        i=0
        #stopWords=self.readStopWrod()
        for doc in self.testDoc:
                    
            p=n=0
            if(choice==1):  
                p,n=self.classifyDocNaiveBayes(doc)    
            elif(choice==2):
                p,n=self.classifyDocSTOP_WORD(doc)
            elif(choice==3):
                p,n=self.classifyDocNOT_WORD(doc) 
            else:
                p,n=self.classifyDocNOTAndSTOP_WORD(doc) 
            
            scoreP=p
            scoreN=n    
            if(scoreP>scoreN):
                if(i>=100):
                    result+=1
                    #print("Tp: True Positive The Review is Positive",scoreN,scoreP)
                #else:
                    
                    #print("Fp: False Positive The Review is +ve",scoreN,scoreP)
            else:
                if(i<100):
                    result+=1
                    #print("Tp: True Positive The Review is Negative",scoreN,scoreP)
                #else:
                    
                    #print("Fp: False Positive The Review is -ve",scoreN,scoreP)
            i+=1

        print("Tp :",int(result)," Fp :",int(i-result))
        result=(result/i)*100
        print("Accurracy for test case ",testVal, ": " ,result," Total docs :",i)
        return result
      
def main():
    i=0
    avgAccuracy=0
    print("press: 1) For Multinomial Naive Bayes")
    print("press: 2) For Multinomial Naive Bayes StopWord Approach")
    print("press: 3) For Multinomial Naive Bayes NOT_Word Approach")
    print("press: 4) For Multinomial Naive Bayes StopWord And NotWord Approach ")
    #print("Your Choice: ")
    choice=int(input("Your Choice:"))
    while(i<10):
        print("Training...")
        obj=NaiveBayesAll(i*100,choice)
        print("Testing...")
        avgAccuracy+=obj.testNB(i+1,choice) 
        
        i+=1
    if(choice==1):    
        print("Avarage of 10-Fold Accuracy:Multinomial MultinomialNaive Bayes ",avgAccuracy/i)
    elif(choice==2):    
        print("Avarage of 10-Fold Accuracy:Multinomial Naive Bayes STop_Word ",avgAccuracy/i)
    elif(choice==3):    
        print("Avarage of 10-Fold Accuracy:Multinomial Naive Bayes NOT_Word ",avgAccuracy/i)
    else:    
        print("Avarage of 10-Fold Accuracy:Multinomial Naive Bayes StopWord & NOT_Word ",avgAccuracy/i)
if __name__ == "__main__":
    main()