## Probability Exercises

1. Suppose two cards are drawn from a standard 52 card deck.
  * What's the probability that the first is a queen and the second is a king?
  > (4/52 * 4/51)

  * What's the probability that both cards are queens?
  > 4/52 * 3/51

  * Suppose that before the second card was drawn, the first was inserted back into the deck and the deck reshuffled. What's the probability that both cards are queens?
  > (4/52)^2

2. A Store Manager wants to understand how his customers use different payment methods, and suspects that the size of the purchase is a major deciding factor. He organizes the table below.

   |           | Cash | Debit | Credit |
   |-----------|:----:|------:|--------|
   | Under $20 |  400 |   150 | 150    |
   | $20 - $50 |  200 |  1200 | 800    |
   | Over $50  |  100 |   600 | 1400   |

   * Given that a customer spent over $50, what's the probability that the customer used a credit card?
   > 1400 / (100 + 600 + 1400) =  
   > 1400 / 2100 =  
   > 14/21

   * Given that a customer paid in cash, what's the probability that the customer spent less than $20?
   > 400 / (400 + 200 + 100) =  
   > 400 / 700 = 4/7

   * What's the probability that a customer spent under $20 using cash?
     > Since it's no longer conditional, we need to take into account ALL transactions.   
     > P(under 20 AND cash) = 400 / sum(transactions)  
     > 400 / (400+200+100+150+1200+600+150+800+1400)  
     > 400/5000 = 4/50 = 2/25

3. A Galvanize grad is looking for her first job!  Given that she is freaked out, her chances of not getting an offer are 70%.  Given that she isn't freaked out, her chances of not getting an offer are 30%.  Suppose that the probability that she's freaked out is 80%. What's the probability that she gets an offer?

  > P(offer) = P(offer|freaked) \* P(freaked) + P(offer|notFreaked) \* P(notFreaked)  
  > P(offer) = .3 * .8 + .7 * .2 = .38

4. Google decides to do random drug tests for heroin on their employees.
   They know that 3% of their population uses heroin. The drug test has the
   following accuracy: The test correctly identifies 95% of the
   heroin users (sensitivity) and 90% of the non-users (specificity).

   |                | Uses heroin | Doesn't use heroin |
   | -------------- | ----------: | -----------------: |
   | Tests positive |        0.95 |               0.10 |
   | Tests negative |        0.05 |               0.90 |

   Alice gets tested and the test comes back positive. What is the probability
   that she uses heroin?

   > P(aliceIsAJunkey|positiveTest) = P(aliceIsAJunkey)P(positiveTest|aliceIsAJunkey)/P(positiveTest)  

   > Before we can compute that formula we need to know what P(positiveTest) is in general.  
   > P(positiveTest) = P(positiveTest|user)P(user) + P(positiveTest|notUser)P(notUser) =  
   > P(positiveTest) = .95*.03 + .1*.03 = .0315  

   > Plugging in the rest of our known values now to the above  
   > P(aliceIsAJunkey|positiveTest) = .03*.95 / .0315 =  
   > .904

   > Sanity Check -- this is pretty damn close to 1-P(positiveTest|doesn'tUse), which should make us feel good.

5. The Birthday Problem.  Suppose there are 23 people in a data science class, lined up in a single file line. Let A_i be the event that the i'th person doesn't have the same birthday as the j'th person for any j < i.  
Use the chain rule from probability to calculate the probability that at least 2 people share the same birthday.

> Chain rule p(x1)p(x2|x1)p(x3|x1 AND x2) ...  
> We have 23 people. To compute the likelihood that any 2 people share a birthday, we sum the probabilities that any one individual shares a birthday with at least on other individual.

> P(anyOnePersonI shares birthday with anyOnePersonJ) = (1/365)^2  
> What about person I person J and another person K ... it starts to get tricky. Instead, lets compute the chance that NO people in the room share a birthday. This is much nicer to compute, applying the chain rule:  

> 1 * 364/365 * 363/365 * 362/365 ... 23 times.  
> We can understand this as the first person has a birthday with P = 1, the next person can pick 364 days to be born on, the next person has 363 days to be born on (can't be born the same day as EITHER p1 or p2) ... so on.  Lets use python to compute this for us:  


```python
# 365 - 343 (23 people)
numerators = range(365 - 22, 366)

prod = 1
for numerator in numerators:
    prod *= numerator/365.0

print 1-prod
# 0.5072972343239853

```
