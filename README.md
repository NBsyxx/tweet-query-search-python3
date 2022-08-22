# tweet-search

## Approach

### Within Preprocessing: 

Create 2 hash:

**word -> {times}** set:we can use word to find the times(time is assumed unique, so it indexes the tweet text) 

**time -> tweet** str: we can use the time to index tweet text

### Search Process
Since the infix query expression includes "(",")", it helps to use postfix: we first convert query to postfix

```python
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
```

Then we evaluate the postfix expression

```python
def eval_postfix(self, postfix):
        stack = []
        for cur in postfix:
            if isinstance(cur,set):
                stack.append(cur)
            if cur in self.Operators:
                top1 = stack.pop()
                top2 = stack.pop()
                stack.append(self.eval(top1,top2,cur))
        return list(stack[0])
```

Sort the output based on its value(time)
and return all candidates 

The search workflow for query is as follow:

``` python 
def search(self, query: str) -> List[Tuple[str, int]]:

        list_of_words = query.split(" ")
        list_of_words = self.parse_infix_to_postfix(list_of_words)
        list_of_times = self.eval_postfix(list_of_words)
        list_of_times.sort(reverse=True)
        return [(self.list_of_tweets[t],t) for t in list_of_times[0:5]]
```

## How to run it?
Just as the default, init the search engine by process tweets
For single search use 

>TweetIndex.search("your | ( query & here )")

```python
ti = TweetIndex()
ti.process_tweets(list_of_tweets)
ti.search("neeva hello")
```

## Design decisions, tradeoffs, assumptions
I decided to use memory for speed, therefore a lot of dictionaries in the code.
The whole application is built over the assumptions that time is unique to tweet.
User can input any string for the search, but everything will be processed according to rules.

## Complexity analysis
Time complexity 
We have N tweets, average tweet length L in words, and the query length Q, Average occurance for each word in all tweets C

The process_tweets() will take O(NL) for preprocessing
The query will take O(QC) for searching 

Spatial complexity
The preprocessing will take O(NLC) memory space 
Search takes negligible space. 

For the starter code, time complexity of preprocessing is O(NL) and it will take O(NLQ) for searching (very slow), it only takes O(NL) spaces

## code updated tests, and time bench marks

### query syntax
**Where is syntax**: it is the string that user put in search function of TweetIndex class, a most basic structure is as below

``` python
ti = TweetIndex()
ti.process_tweets(list_of_tweets)
ti.search("query")
```

**TYPE1 non-queries**: words without "&" and "|" will be parsed as non-queries, and we return the intersaction of each words, we allow the use of "!" to represent sentences not having this words

**TYPE2 queries**: words can be with "&" and "|", but it do require space between each word. "&" means intersaction and "|" means union, we allow the use of "!" to represent sentences not having this words. The default order for processing is prefix which is from left to right, we can adjust the order by adding "("")"

### code showcases and tests

    ** testing non-queries **
    print(ti.search("neeva this him"))
    return: [('that we him this neeva know', 9102), ('people him this neeva for', 8383), ('what by of special him this neeva a', 8128), 
    ('neeva their him this see thing they', 7644), ('can special people him this neeva be who in', 5690)]
    
    print(ti.search("neeva this him !know"))
    return:  [('people him this neeva for', 8383), ('what by of special him this neeva a', 8128), ('neeva their him this see thing they', 7644),
    ('can special people him this neeva be who in', 5690), ('take of special him this neeva', 4297)]
    
    print(ti.search("brother"))
    return:[]
    
     ** testing queries **
    print(ti.search("neeva & this & ( ( !him & know ) | ( very & because ) )"))
    return:  [('because very this neeva know', 9969), ('special it this neeva know could', 9314), ('that because very when than this neeva', 7258),
    ('time year special like those this neeva she for know', 7097), ('time it when this neeva know a', 6805)]
    
    ** testing mixing expression **
    print(ti.search("neeva | this & him"))
    return:  since it is postfix parsing so it goes from left to right  

     ** testing random things  **
    print(ti.search("neeva | & him"))
    stdout: Query Syntax Error
    return: [('', -1)]

    print(ti.search("| & "))
    stdout: Query Syntax Error
    return:  [('', -1)]

    print(ti.search("neeva&hello"))
    it will read it and parse it as a query sentence since there's no "neeva&hello"
    return: []


on 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz 
in terms of bench marks


**for starter version**
it takes 0.002s to preprocess 10000 tweet

it takes 3.05s to run 1000 times of 
```
ti.search("neeva hello")
```

**for my version**
it takes 0.03s to preprocess 10000 tweet

it takes 0.14s to run 1000 times of 
```
ti.search("neeva hello")
```

it takes 0.21s to run 1000 times of 
```
ti.search("neeva & this & ( ( !him & know ) | ( very & because ) )")
```

