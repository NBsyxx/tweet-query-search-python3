"""
Please use Python version 3.7+
"""

import csv
from typing import List, Tuple
from collections import defaultdict
import time

class TweetIndex:
    # Starter code--please override
    def __init__(self):
        # collect all exist timestamps 
        self.total_time = set()
        # word -> timestamps
        self.word_to_time = defaultdict(set)
        # timestamps -> twitters
        self.list_of_tweets = defaultdict(str)
        # set of query operations
        self.Operators = set(['|', '&', '(', ')'])  # collection of Operators
        self.Priority = {'|':1, '&':1} # dictionary having priorities of Operators, future we can have more in the query 


    def process_tweets(self, list_of_timestamps_and_tweets: List[Tuple[str, int]]) -> None:
        """
        process_tweets processes a list of tweets and initializes any data structures needed for
        searching over them.

        :param list_of_timestamps_and_tweets: A list of tuples consisting of a timestamp and a tweet.
        """
        for row in list_of_timestamps_and_tweets:
            timestamp = int(row[0])
            tweet = str(row[1]).lower() # Requirement: all treated as lower key
            self.list_of_tweets[timestamp] = tweet
            for word in tweet.split(" "):
                self.word_to_time[word].add(timestamp)

        self.total_time = set(self.list_of_tweets.keys())
        for word in list(self.word_to_time.keys()):
            self.word_to_time["!"+word] = self.total_time - self.word_to_time[word]
        
    
    def parse_infix_to_postfix(self, infix): 
        stack = [] # initialization of empty stack
        postfix = [] 
        for character in infix:
            if character not in self.Operators:  # if an operand append in postfix infix
                postfix.append(self.word_to_time[character])
            elif character=='(':  # else Operators push onto stack
                stack.append('(')
            elif character==')':
                while stack and stack[-1]!= '(':
                    postfix.append(stack.pop())
                stack.pop()
            else: 
                while stack and stack[-1]!='(' and self.Priority[character]<= self.Priority[stack[-1]]:
                    postfix.append(stack.pop())
                stack.append(character)
        while stack:
            postfix.append(stack.pop())
        return postfix
    

    def eval_postfix(self, postfix):
        stack = []
        for cur in postfix:
            if isinstance(cur,set):
                stack.append(cur)
            if cur in self.Operators:
                if len(stack) <= 1: 
                    print("Query Syntax Error")
                    return [-1]
                top1 = stack.pop()
                top2 = stack.pop()
                stack.append(self.eval(top1,top2,cur))
        return list(stack[0])


    def eval(self,a,b,op):
        if op == "&":
            return a & b 
        if op == "|":
            return a | b 
        

    def search(self, query: str) -> List[Tuple[str, int]]:
        """
        NOTE: Please update this docstring to reflect the updated specification of your search function

        search looks for the most recent tweet (highest timestamp) that contains all words in query.

        :param query: the given query string
        :return: a list of tuples of the form (tweet text, tweet timestamp), ordered by highest timestamp tweets first. 
        If no such tweet exists, returns empty list.
        """
        list_of_words = query.split(" ")
        if len(list_of_words) >= 2 and "&" not in query and "|" not in query:
            # it is a non-query
            list_of_times = self.total_time
            # print(self.word_to_time["neeva"])
            for i in range(len(list_of_words)):
                list_of_times = list_of_times & self.word_to_time[list_of_words[i]]
            list_of_times = list(list_of_times)
        else:      
            # it is a query    
            list_of_words = self.parse_infix_to_postfix(list_of_words)
            list_of_times = self.eval_postfix(list_of_words)
        list_of_times.sort(reverse=True)
        return [(self.list_of_tweets[t],t) for t in list_of_times[0:5]]

if __name__ == "__main__":
    # A full list of tweets is available in data/tweets.csv for your use.
    tweet_csv_filename = "../data/tweets.csv"
    list_of_tweets = []
    with open(tweet_csv_filename, "r") as f:
        csv_reader = csv.reader(f, delimiter=",")
        for i, row in enumerate(csv_reader):
            if i == 0:
                # header
                continue
            timestamp = int(row[0])
            tweet = str(row[1])
            list_of_tweets.append((timestamp, tweet))

    
    ti = TweetIndex()
    
    # test speed of preprocessing
    t0 = time.time()
    ti.process_tweets(list_of_tweets)
    print(time.time() - t0)

    # testing non-queries
    print(ti.search("neeva this him"))
    #[('that we him this neeva know', 9102), ('people him this neeva for', 8383), ('what by of special him this neeva a', 8128), ('neeva their him this see thing they', 7644), ('can special people him this neeva be who in', 5690)]
    
    print(ti.search("neeva this him !know"))
    # [('people him this neeva for', 8383), ('what by of special him this neeva a', 8128), ('neeva their him this see thing they', 7644), ('can special people him this neeva be who in', 5690), ('take of special him this neeva', 4297)]
    
    print(ti.search("brother"))
    #[]
    
    # testing queries
    print(ti.search("neeva & this & ( ( !him & know ) | ( very & because ) )"))
    # [('because very this neeva know', 9969), ('special it this neeva know could', 9314), ('that because very when than this neeva', 7258), ('time year special like those this neeva she for know', 7097), ('time it when this neeva know a', 6805)]
    
    # testing mixing expression
    print(ti.search("neeva | this & him"))
    # since it is postfix parsing so it goes from left to right  

    # testing random things 
    print(ti.search("neeva | & him"))
    # it will stdout Query Syntax Error
    # and return [('', -1)]

    print(ti.search("| & "))
    # it will stdout Query Syntax Error
    # and return [('', -1)]

    print(ti.search("neeva&hello"))
    # it will read it and parse it as a query sentence since there's no "neeva&hello"
    # and return []

    # test speed
    t0 = time.time()
    for i in range(1000):
        ti.search("neeva & hello")
    print(time.time() - t0)

    # test speed
    t0 = time.time()
    for i in range(1000):
        ti.search("neeva & this & ( ( !him & know ) | ( very & because ) )")
    print(time.time() - t0)