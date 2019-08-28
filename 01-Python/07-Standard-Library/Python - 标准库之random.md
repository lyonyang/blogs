# Python之路 - 标准库之random

## 介绍  🍀

`random`模块为我们提供了各种分布的伪随机数生成器

`random`模块功能分为以下几个部分 : 

- Bookkeeping functions
- Functions for integers
- Functions for sequences
- Real-valued distributions

## Bookkeeping functions  🍀

```python
random.seed(a=None, version=2):
    """
    Initialize the random number generator.
    """
random.getstate():
    """
    Return an object capturing the current internal state of the generator.
    This object can be passed to setstate() to restore the state.
    """
random.setstate(state):
    """
    State should hava been obtained from a previous call to getstate(),
    and setstate() restores the internal state of the generator to what it was at the time getstate() was called.
    """
random.getrandbits(k):
    """
    Returns a Python integer with k random bits.
    This method is supplied with the Mersenne Twister generator and some other generators may also provide it as an optional part of the API.
    When available, getrandbits() enables randrange() to handle arbitrarily large ranges.
    """
```

## Functions for integers  🍀

```python
random.randrange(stop)
random.randrange(start, stop[, step]):
    """
    Return a randomly selected element from range(start, stop, step).
    This is equivalent to choice(range(start, stop, step)),
    but doesn't actually build a range object.
    """
random.randint(a, b):
    """
    Return a random integer N such that a <= N <= b. 
    Alias for randrange(a, b+1).
    """
```

## Functions for sequences  🍀

```python
random.choice(seq):
    """
    Return a random element from the non-empty sequence seq. 
    If seq is empty, raises IndexError.
    """
random.choices(population, weights=None, *, cum_weights=None, k=1):
    """
    Return a k sized list of elements chosen from the population with replacement. 
    If the population is empty, raises IndexError.
    """
random.shuffle(x[, random]):
    """
    Shuffle the sequence x in place.
    """
random.sample(population, k):
    """
    Return a k length list of unique elements chosen from the population sequence or set. 
    Used for random sampling without replacement.
    """
```

## Real-valued distributions  🍀

```python
random.random():
    """
    Return the next random floating point number in the range [0.0, 1.0).
    """
random.uniform(a, b):
    """
    Return a random floating point number N such that a <= N <= b for a <= b and b <= N <= a for b < a.
    """
random.triangular(low, high, mode):
    """
    Return a random floating point number N such that low <= N <= high and with the specified mode between those bounds.
    """
random.betavariate(alpha, beta):
    """
    Beta distribution. 
    Conditions on the parameters are alpha > 0 and beta > 0. 
    Returned values range between 0 and 1.
    """
random.expovariate(lambd):
    """
    Exponential distribution. lambd is 1.0 divided by the desired mean. 
    """
random.gammavariate(alpha, beta):
    """
    Gamma distribution. 
    (Not the gamma function!) Conditions on the parameters are alpha > 0 and beta > 0.
    """
random.gauss(mu, sigma):
    """
    Gaussian distribution. 
    mu is the mean, and sigma is the standard deviation. 
    This is slightly faster than the normalvariate() function defined below.
    """
random.lognormvariate(mu, sigma):
    """
    Log normal distribution.
    """
random.normalvariate(mu, sigma):
    """
    Normal distribution. mu is the mean, and sigma is the standard deviation.
    """
random.vonmisesvariate(mu, kappa):
    """
    mu is the mean angle, expressed in radians between 0 and 2*pi, 
    and kappa is the concentration parameter, 
    which must be greater than or equal to zero. 
    If kappa is equal to zero, 
    this distribution reduces to a uniform random angle over the range 0 to 2*pi.     
    """
random.paretovariate(alpha):
    """
    Pareto distribution. alpha is the shape parameter.
    """
random.weibullvariate(alpha, beta):
    """
    Weibull distribution. 
    alpha is the scale parameter and beta is the shape parameter.
    """
```

## Examples and Recipes  🍀

Basic examples : 

```python
>>> import random
>>> random.random()                             # Random float:  0.0 <= x < 1.0
0.37444887175646646
>>> random.uniform(2.5, 10.0)                   # Random float:  2.5 <= x < 10.0
3.1800146073117523
>>> random.expovariate(1 / 5)                   # Interval between arrivals averaging 5 seconds
5.148957571865031
>>> random.randrange(10)                        # Integer from 0 to 9 inclusive
7
>>> random.randrange(0, 101, 2)                 # Even integer from 0 to 100 inclusive
26
>>> random.choice(['win', 'lose', 'draw'])      # Single random element from a sequence
'draw'
>>> deck = 'ace two three four'.split()
>>> random.shuffle(deck)                        # Shuffle a list
>>> deck
['four', 'two', 'ace', 'three']
>>> random.sample([10, 20, 30, 40, 50], k=4)    # Four samples without replacement
[40, 10, 50, 30]
```

Simulations :

```python
>>> # Six roulette wheel spins (weighted sampling with replacement)
>>> random.choices(['red', 'black', 'green'], [18, 18, 2], k=6)
['red', 'green', 'black', 'black', 'red', 'black']

>>> # Deal 20 cards without replacement from a deck of 52 playing cards
>>> # and determine the proportion of cards with a ten-value
>>> # (a ten, jack, queen, or king).
>>> import collections
>>> deck = collections.Counter(tens=16, low_cards=36)
>>> seen = random.sample(list(deck.elements()), k=20)
>>> seen.count('tens') / 20
0.15
>>> # Estimate the probability of getting 5 or more heads from 7 spins
>>> # of a biased coin that settles on heads 60% of the time.
>>> trial = lambda: random.choices('HT', cum_weights=(0.60, 1.00), k=7).count('H') >= 5
>>> sum(trial() for i in range(10000)) / 10000
0.4169
>>> # Probability of the median of 5 samples being in middle two quartiles
>>> trial = lambda : 2500 <= sorted(random.choices(range(10000), k=5))[2]  < 7500
>>> sum(trial() for i in range(10000)) / 10000
0.7958
```

更多random相关 : [random](https://docs.python.org/3/library/random.html?highlight=random#module-random) — Generate pseudo-random numbers