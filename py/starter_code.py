"""
Please use Python version 3.7+
"""

from ast import Expression
import csv
from lib2to3.pytree import convert
from typing import List, Tuple
import heapq
from collections import defaultdict

# '''
# Tweet Class
# comparison are based on timestamp since it is globally unique 
# '''
# @dataclass(order=True)
# class Tweet:
#     tweet: str = field(compare=False)
#     timestamp: int 

class TweetIndex:
    # Starter code--please override
    def __init__(self):
        # word -> timestamps
        self.word_to_list_of_times = defaultdict(set)
        # timestamps -> twitters, assuming timestamps are unique
        self.list_of_tweets = defaultdict(str)
        # used for hashing the signs
        self.signs = {'!': lambda: print("Error in sign usage"),
                      '|': lambda x, y: x | y,
                      '&': lambda x, y: x & y,
                      '(': lambda: print("Error in sign usage"),
                     ')': lambda: print("Error in sign usage")
        }

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
                self.word_to_list_of_times[word].add(timestamp)
    
    def seach_qls(self, query: List) -> List[int]:
            """
            Deal with the requirement of Query language specification.
            :param query: list after processed by the self.preprocess().
            :return: the list of total required timestamps.
            """
            stack = []
            idx = 0
            while idx < len(query):
                each = query[idx]
                if each not in self.signs:
                    stack.append(self.word_to_list_of_times[each])
                elif each == '(':
                    y = idx
                    balance = 1
                    while balance > 0:
                        y += 1
                        if query[y] == '(':
                            balance += 1
                        if query[y] == ')':
                            balance -= 1
                        if balance < 0:
                            print("Error in test case: your () is wrongly paired")
                    stack.append(set(self.seach_qls(query[idx+1:y])))
                    idx = y
                else:
                    stack.append(each)
                idx += 1
            # process stack
            while len(stack) > 1:
                if stack[-2] != '!':
                    rv, sign, lv = stack.pop(), stack.pop(), stack.pop()
                    stack.append(self.signs[sign](rv, lv))
                else:
                    # Lazzy solution, memory consuming for db.
                    v, _ = stack.pop(), stack.pop()
                    total_timestamps_count = len(self.list_of_tweets)
                    total = set(range(1, total_timestamps_count))
                    stack.append(total - v)
            return sorted(list(stack[0]), key=lambda x: -x)

    # Starter code--please override
    def search(self, query: str) -> List[Tuple[str, int]]:
        """
        NOTE: Please update this docstring to reflect the updated specification of your search function

        search looks for the most recent tweet (highest timestamp) that contains all words in query.

        :param query: the given query string
        :return: a list of tuples of the form (tweet text, tweet timestamp), ordered by highest timestamp tweets first. 
        If no such tweet exists, returns empty list.
        """
        def check_parentheses(list_of_words):
            stack = []
            for i in range(len(list_of_words)-1,-1,-1):
                if list_of_words[i] == "(" or list_of_words[i] == ")":
                    stack.append(list_of_words[i])
                if len(stack) >= 2 and stack[-1]== "(" and stack[-2] == ")":
                    stack = stack[:-2]
            if stack == []:
                return True 
            else:
                return False 

        def search_and(words,candidates) -> List[Tuple[int, str]]:
            # search candidates that has all the words
            print("candidate 0",candidates[0])
            for word in words:
                future_candidates = []
                for timestamp,tweet in candidates:
                    if word.lower() in tweet.lower().split(): # case insensitive
                        future_candidates.append((timestamp,tweet))
                    candidates = future_candidates
            return candidates


        def search_or(words,candidates) -> List[Tuple[int, str]]:
            #search candidates that has one of the words
            future_candidates = [] 
            hash = set([w.lower() for w in words]) # case insensitive
            for timestamp,tweet in candidates:
                for w in tweet.split():
                        if w.lower() in hash: # case insensitive
                         future_candidates.append((timestamp,tweet))
            candidates = future_candidates
            return candidates


        def search_not(words,candidates) -> List[Tuple[int, str]]:
            # search candidates that does not has any of the words
            not_candidates = set(search_or(words, candidates))
            return [c for c in candidates if c not in not_candidates]


        def handle_unit(list_of_words, candidates) -> List[Tuple[int, str]]:
            AND_list = []
            OR_list = []
            NOT_list = []

            if "&" in list_of_words and "|" in list_of_words:
                print("Invalid expression!")
                return [("",-1)]

            elif "&" in list_of_words:
                # have to consider "!" in this case 
                print("Valid expression &")
                for w in list_of_words:
                    if w == "&":
                        continue
                    elif w[0] == "!":
                        NOT_list.append(w[1:])
                    else:
                        AND_list.append(w)
                print("AND NOT",AND_list,NOT_list)
                candidates = search_and(AND_list, candidates)
                candidates = search_not(NOT_list, candidates)

            elif "|" in list_of_words:
                print("Valid expression |")
                for w in list_of_words:
                    if w == "|":
                        continue
                    elif w[0] == "!":
                        NOT_list.append(w[1:])
                    else:
                        OR_list.append(w)
                print("OR NOT",OR_list,NOT_list)
                candidates_not = search_not(NOT_list, candidates)
                candidates_or = search_or(OR_list, candidates)
                candidates = list(set(candidates_not + candidates_or))
            else:
                print("Valid expression no logic signs")
                candidates = search_and(list_of_words, candidates)

            return candidates 

            
        list_of_words = query.split(" ")
        candidates = self.list_of_tweets

        # check if the expression is balancesd
        print("test",self.seach_qls(list_of_words))

        # stack the expression and generate candidates one by one
        candidates = handle_unit(list_of_words, candidates)

        # once have it all, this is the final return part 
        heapq.heapify(candidates)
        length_candidates = len(candidates)
        if length_candidates >= 5:
            candidates = heapq.nlargest(5, candidates)
        else:
            candidates = heapq.nlargest(length_candidates, candidates)
        return candidates if len(candidates) != 0 else [("",-1)]
        

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

    # print(list_of_tweets)

    ti = TweetIndex()
    ti.process_tweets(list_of_tweets)

    # # testing no logics 
    # print(ti.search("neeva i many"),"\n")

    # # testing &
    # print(ti.search("neeva & i & many"),"\n")

    # # testing !&
    # print(ti.search("!neeva & i & many"),"\n")

    # # testing |
    # print(ti.search("i | many"),"\n")

    # testing | !
    print(ti.search("many | !neeva"),"\n")

    # testing bracket


    # assert ti.search("hello") == [('hello this is also neeva', 15)]
    # assert ti.search("hello me") == [('hello not me', 14)]
    # assert ti.search("hello bye") == [('hello bye', 3)]
    # assert ti.search("hello this bob") == [('hello neeva this is bob', 11)]
    # assert ti.search("notinanytweets") == [('', -1)]
    print("Success!")
