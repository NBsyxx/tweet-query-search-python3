"""
Please use Python version 3.7+
"""

import csv
from sys import prefix
from turtle import pos
from typing import List, Tuple
from collections import defaultdict
import time
from itertools import combinations
from random import randint

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
                print(character)
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
        print("postfix:",postfix)
        return postfix
    

    def eval_postfix(self, postfix):
        stack = []
        for cur in postfix:
            if isinstance(cur,set):
                stack.append(cur)
            if cur in self.Operators:
                top1 = stack.pop()
                top2 = stack.pop()
                stack.append(self.eval(top1,top2,cur))
        print("Evaluation success",stack)
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
        list_of_words = self.parse_infix_to_postfix(list_of_words)
        list_of_times = self.eval_postfix(list_of_words)
        list_of_times.sort(reverse=True)

        return [(self.list_of_tweets[t],t) for t in list_of_times[0:5]]

if __name__ == "__main__":
    # A full list of tweets is available in data/tweets.csv for your use.
    tweet_csv_filename = "../data/small.csv"
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
    ti.process_tweets(list_of_tweets)
    print(ti.search("this & is & ( neeva | !me ) & this & is & ( neeva | !me )") )
    print("Success!")
