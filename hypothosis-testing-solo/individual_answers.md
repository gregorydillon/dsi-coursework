State which test should be used for the following scenarios to calculate p-values. Explain your choice.

1. You randomly select 50 dogs and 80 cats from a large animal shelter, and want to know if dogs and cats have the same weight.
> Here, we would be comparing mean weights of dogs and cats. I would assume that the weight of these individual dogs and the weights of the individual cats are independent (although in our case it's likely that coming from the same shelter will have an impact on these data). Because the weights of the dogs and cats individually are independent, and we're comparing the mean weights of our two samples. Additionally, because I have knowledge of dogs and cats and their relative sizes to each other, I want to assume that the variance in these two populations is different. House-cat breeds are more closely related in size than are different dog-breeds.

> In summary, I have 2 sample-populations, both greater than 40, where the true variances of each are unknown and the not equal to each other. I would suggest using the Welches t-test in this case.

1. A random sample of San Franciscans and Oaklanders were surveyed about their favorite baseball team, and you want to determine if the same proportion of people like the SF Giants.
> Once again, we'll be comparing means. In this case the means will be the proportion of the sample that say their favorite team is the SF Giants. In this case our population groups are San Franciscans and Oaklanders respectively. I want to prove that the proportions are NOT the same, so my null hypothesis is that they are the same. Under this assumption the population variances would also be the same, due to variance relying on P. Additionally, I want to assume that the two are independent -- any particular San Franciscan's preference is independent of any particular Oaklander's preference. Therefore, I would choose the pooled two sample t-test

> In summary. I have 2 sample populations (of unknown size) where samples are independent (assuming people in the study are not influencing each others preference, which is the worst assumption here I think) and that the variance within the populations is roughly equal, that is baseball fans in the two cities have roughly equal spread from their mean.

A study attempted to measure the influence of patients' astrological signs on their risk for heart failure. 12 groups of patients (1 group for each astrological sign) were reviewed and the incidence of heart failure in each group was recorded.

For each of the 12 groups, the researchers performed a z-test comparing the incidence of heart failure in one group to the incidence among the patients of all the other groups (i.e. 12 tests). The group with the highest rate of heart failure was Pisces, which had a p-value of .026 when assessing the null hypothesis that it had the same heart failure rate as the group with the lowest heart failure rate, Leo. What is the the problem with concluding from this p-value that Pisces have a higher rate of heart failure than Leos at a significance level of 0.05? How might you adjust your interpretation of this p-value?

> Because multiple tests were done, we need to fix a combined alpha value (rather than fixing the individual alpha value). p-values give us information about the likelihood of any single event occurring, but when we do multiple tests around the same feature (heart-failure:astrological sign) we are adding events. Our p-value of .026 means roughly 1/50 chance of getting this result by chance. However, we have performed 12 such experiments, which means our chance of encountering this event has increased!

> To correct for this, instead of fixing our individual alpha, we fix our family-wise alpha at the desired .05 level. In our case we'll use the Bonferroni Correction:

> `alpha_individual = comb_alpha / n_experiemnts` => `alpha_individual = .05/12` => `alpha_individual ~= .0042`

> So, our p value for both Leo's and Pisces is below the threshold for significance, and we should not reject the null hypothesis. 
