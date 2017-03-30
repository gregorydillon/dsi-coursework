** Probability **

1. The bias of a coin is 0.6 in favor of heads. What is the probability of flipping
8 or more heads in 10 flips?

> The most straight forward way to compute this is to sum the probabilities of flipping exactly 8 heads, exactly 9 heads, and exactly 10 heads. Which can be done like this:

```
(10 choose 8) * .6^8 * .4^2 +
(10 choose 9) * .6^9 * .4^1+
1 * .6^10

~= 0.1672897536
```

2. You've found a secret admirer note on your desk, and don't know
who it might've come from but you know it must've been one of your
three office mates:  Jack, John, or Jimmy.  
- As of yesterday, you thought it was twice as likely that Jimmy had a crush on you than John,
and that John and Jack were equally likely to have a crush on you.  
- However even if Jimmy liked you, you think there'd only be 5% he'd leave you a note.
- On the other hand, if Jack liked you there'd be a whopping 50% chance he'd leave you a note.
and if John liked you, there'd be a 20% chance he'd leave you a note.

What's the probability that the note came from John?

> Prior Thoughts:

```
P(JimmyCrush) = 2*P(JohnCrush) = 2*P(JackCrush)
P(JimmyNote | JimmyCrush) = .05
P(JackNote | JackCrush) = .5
P(JohnNote | JohnCrush) = .2
```

>First, lets assume that at least one person has a crush on us -- we got a note after all. Formally, our assumption is:

```
P(JimmyCrush) + 2*P(JohnCrush) + 2*P(JackCrush) = 1
P(JimmyCrush) = 1/5
P(JohnCrush) = 2/5
P(JackCrush) = 2/5
```

>So now lets use Bayes Rule and see if we can solve for P(JohnNote), since we have the left hand side and the P(JohnCrush)

```
P(JohnNote | JohnCrush) = P(JohnNote) * P(JohnCrush | JohnNote) / P(JonhCrush)
=>
P(JohnNote) = P(JohnNote | JohnCrush) * P(JohnCrush) / P(JohnCrush | JohnNote)
=>
P(JohnNote) = 1/5 * 2/5 / P(JohnCrush | JohnNote)
```

>To finish and get an answer, we have to make another (fair) assumption. If John left the note, we are saying that is evidence that he is indeed our secret admirer. So `P(JohnNote | JohnCrush) = 1`. Therefore:

```
P(JohnNote) = 1/5 * 2/5 * 1 = 2/10 = 1/5 = .2
```



** Statistics **

Below are the total number of log-ins for 20 different randomly selected users from 2014:
    [10, 25, 12, 35, 14, 18, 16, 15, 22, 10, 9, 11, 49, 20, 15, 9, 18, 19, 20, 20]

3. What is the sample mean?

> The sample mean is the sum of these numbers / 20

```python
np.mean([10, 25, 12, 35, 14, 18, 16, 15, 22, 10, 9, 11, 49, 20, 15, 9, 18, 19, 20, 20])
# 18.350000000000001

```

4. What is the sample variance?

> Variance is Sum((theseNumbers - mean)^2) / 20
```
np.var([10, 25, 12, 35, 14, 18, 16, 15, 22, 10, 9, 11, 49, 20, 15, 9, 18, 19, 20, 20])
86.927499999999995
```

5. If we randomly select another user from 2014, what is the probability that he/she
has more than 15 log-ins?  

> Although I don't think we have enough data to be very confident about this, we could compute a sample probability for this using MOM -- lets pick a poisson distribution:

> Mean = Lambda = 18.35
> Now use the PMF function:
```
l**k * np.exp(-l) / np.math.factorial(k)
Out[51]: 0.065592171211774575
```

> This number might be the probability that exactly 15 people visit.. but I am running out of time.

> REVISITING, Instead of the PDF lets use 1-CDF(15)!

```
p = 1 - st.poisson(mu=18.35).cdf(15)
p # 0.74003716855213564
```

> Which jives with my sense of reality better than that .06


6. Sales targets weren't met last year.  The sales department asserts that on average,
there were only 10 log-ins per user, however the web team thinks there were more.  
Set up a frequentist hypothesis test and compute a p-value based on your data.

```
H0 -> 10 logins per user per year
H1 -> more than 10 logins per year
```

> In this case, our data has an experimental mean of 18.35 with variance 86.97, std 9.32.

> Our Z score assuming the null hyp of finding this data is:

```
z = 18.35 - 10 / 9.32
# 0.895922746781116
p_value = scipy.stats.norm.sf(abs(.8959))

p_value
# 0.18515308708630862
```

> Given our data -- we should fail to reject the null hypothesis



7. A major charity organization is interested to see if changing the mission
statement on the website increases donations. As a pilot study, they randomly
show 1 of 10 newly drawn up mission statements to each user that comes to the site.  
As such, you set up 10 separate hypothesis tests, each testing whether or not
there was an increase in donations. What adjustments would you make to account for the 10 tests?

> We have to be sure to account for multiple testing errr. We fix the groups p value at .05 which means we have to hold the individual tests to a p-score of .05/10


**  Modeling **

8.  Generally, when we increase the flexiblity or complexity of the model, what happens to bias?  What about variance?
What do we expect to happen to the training error?  What about the test error?

> The bias goes down as the complexity goes up. The variance tends to go up as complexity goes up. This makes sense because we're giving our model MORE freedom to respond to variables -- that's a less biased model. In these cases the training error will almost always go down (due to the flexibility) but test error will likely go up (due to overfitting)

9.  You have two models:
Model 1:   Salary ~ Occupation + Height + Gender
Model 2:   Salary ~ Occupation + Region + Height + Gender

Name 2 appropriate ways to compare these two models.
Name 1 inappropriate way to compare these two models.  

> Appropriate:  
> We could compare the RMSE of these models on the test data. Or another error metric.  
> We could compare the p-values of each component

> Inappropriate:  
> We should not compare the r^2 values of these models.
