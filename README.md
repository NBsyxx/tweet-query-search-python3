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


## Complexity analysis


## code updated tests, and time bench marks