1. The prior is 1 in 5 for each die

2. Likelihood = P(ourData | ourHyp)
  * We have 5 such functions, 1 per hypothesis
  * In this case our data is the roll that we produced
  * Lets encode our hyp. w/ their likelihood functions
    1. we picked 4 sided -> P(rolledWhateverWeRolled | die=4sided)
    2. we picked 6 sided -> P(rolledWhateverWeRolled | die=6sided)
    3. we picked 8 sided -> P(rolledWhateverWeRolled | die=8sided)
    4. we picked 12 sided -> P(rolledWhateverWeRolled | die=12sided)
    5. we picked 20 sided -> P(rolledWhateverWeRolled | die=20sided)
3. We rolled an 8, what are the probability of each die having been chosen

```
h4:  .2 0 0
h6:  .2 0 0
h8:  .2 .125 .025
h12: .2 .083 .017
h20: .2 .05  .010

SUM to create norm const:

.025 + .017 + .01 = .052

NORMALIZE for posterior
h4: 0
h6: 0
h8: .48
h12: .32
h20: .19
Without rounding error, these sum to 1 so we are happy :)
```

4. If we had rolled 50 times, we would have continuously updated our beliefs (aka priors) to reflect the posteriors we found at each roll. Unfortunately, we've created a bad situation in that our belief about rolling a 4 and 6 have already reached 0 which means they'll never increase again. This is okay for us, because we ONLY GET ONE CHANCE TO SAMPLE anyway.

5. The second data set [10, 10, 10, 10, 8, 8] gives us more valuable data as it allows us to eliminate many more choices of die per roll.

6.

```
4-sided die: 8%    0   0
6-sided die: 12%   0   0
8-sided die: 16%  .125 0.02
12-sided die: 24% .083 0.02
20-sided die: 40% .05  0.02

SUM FOR NORM:

0+0+.02+.0199+.02 = .06

NORM:
h4: 0
h6: 0
h8: .333333333333333333
h12: .33333333333333333
h20: .33333333333333333
LEEEROY JENKINS.

Now we are not very sure which die we got... equal chances of 8,12,20.
Yes, this is different from what we got before.  
```

7. We would expect the postirors to strongly favor an 8 sided die in this case. The reason is that we could still eliminate 4 and 6 because we've rolled at least one 8. AND if we NEVER rolled a value higher than an 8 we have strong evidence to suggest that a 20 or a 12 sided die is not the one we are rolling. The likelihood for these results follow p(n<=8)^50 for each die, which are astronomically low for the d12 (~10^-9) and d20 (10^-20). 
