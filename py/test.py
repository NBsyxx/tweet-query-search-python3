"""
Please use Python version 3.7+
"""

'''
The starter code cannot pass the test cases.
The starter code itself have bug lie in:
class TweetIndex:
process_tweets, both the parameter sending in are wrong in order.
search, the return type is different from the assert code in main function.
'''
import csv
from typing import List, Tuple
from collections import defaultdict
import time
from itertools import combinations
from random import randint

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

    # Starter code--please override
    def process_tweets(self, list_of_timestamps_and_tweets: List[Tuple[int, str]]) -> None:
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

    # Starter code--please override
    def search(self, query: str, topk: int = 5, qls: bool = True) -> List[Tuple[str, int]]:
        """
        :param query: the given query string
        :param topk: return top k recent results, not used for non-qls (Query language specification) search
        :param gls: if use qls please make sure it's true, otherwise treated as general cases.
        :return: a list of tuples of the form (tweet text, tweet timestamp), ordered by highest timestamp tweets first. 
        If no such tweet exists, returns empty list.
        """
        if qls:
            query = self.preprocess(query)
            print("preprocessed query",query)
            ans_list = self.seach_qls(query)
            print("ans_list",ans_list)
            if not ans_list:
                return [('', -1)]
            return [(self.list_of_tweets[i], i) for i in ans_list[:topk]]
        list_of_words = query.split(" ")
        list_of_timestamps = [sorted(list(self.word_to_list_of_times[i]), key=lambda x: -x) for i in list_of_words]
        if [] in list_of_timestamps:
            return [('', -1)]
        ans_idx, ans_timestamp = 0, list_of_timestamps[0][0]
        # Only return the top #1 result
        for i in list_of_timestamps:
            while ans_timestamp not in i:
                ans_idx += 1
                ans_timestamp = list_of_timestamps[0][ans_idx]
        return [(self.list_of_tweets[ans_timestamp], ans_timestamp)]

    def preprocess(self, query: str) -> List[str]:
        """
        Make query to be list of words & signs.
        :param query: the original str.
        :return: list of words without space.
        """
        ans = ""
        for idx, i in enumerate(query):
            if i == '(':
                ans += ' ( '
            elif i == ')':
                ans += ' ) '
            elif i == '!':
                ans += ' ! '
            else:
                ans += i
        rt = ans.split(" ")
        while "" in rt:
            rt.remove("")
        return rt

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
        print(stack)
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


if __name__ == "__main__":
    # A full list of tweets is available in data/tweets.csv for your use.
    #tweet_csv_filename = "../data/small.csv"
    tweet_csv_filename = "../data/tweets.csv"
    list_of_tweets = []
    with open(tweet_csv_filename, "r") as f:
        csv_reader = csv.reader(f, delimiter=",")
        for i, row in enumerate(csv_reader):
            if i == 0:
                continue
            timestamp = int(row[0])
            tweet = str(row[1])
            list_of_tweets.append((timestamp, tweet))

    ti = TweetIndex()
    ti.process_tweets(list_of_tweets)
    # From starter codes
    '''assert ti.search("hello") == [('hello this is also neeva', 15)]
    assert ti.search("hello me") == [('hello not me', 14)]
    assert ti.search("hello bye") == [('hello bye', 3)]
    assert ti.search("hello this bob") == [('hello neeva this is bob', 11)]
    assert ti.search("notinanytweets") == [('', -1)]
    print("Success!")'''
    # Simple printing to test correction
    # print(ti.search("neeva", qls=True))
    # print(ti.search("neeva & could", qls=True))
    # print(ti.search("neeva & (could | they)", qls=True))
    print(ti.search("neeva & (could & !(they & two))", qls=True))

    # # for benchmarking
    # word_lib = set()
    # for eachline in list_of_tweets:
    #     for eachword in eachline[1].split(" "):
    #         word_lib.add(eachword)
    # complexity = 4
    # # heavily time consuming, if you are using py3.9.7, use math.comb and iterator instead of len
    # cases = list(combinations(word_lib, complexity))
    # # total_test_runs = total_runs * 4
    # total_runs = 100
    # all_test_cases = []
    # for _ in range(total_runs):
    #     choose = randint(0, len(cases) - 1)
    #     all_test_cases.append(' & '.join(cases[choose]))
    #     all_test_cases.append(' | '.join(cases[choose]))
    # start = time.time()
    # for each in all_test_cases:
    #     ti.search(each, qls=True)
    # end = time.time()
    # print("Time benchmark for "+str(len(all_test_cases))+" Test cases.")
    # print("Of complexity level (num of different words): "+str(complexity)+".")
    # print("result: "+str(end-start)+" seconds.")
