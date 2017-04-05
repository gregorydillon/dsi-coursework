1. You fit a linear regression to predict SAT score with many predictors, one of which is whether or not the student was homeschooled. `Beta_homeschool = -40`. How do you interpret the coefficient? How do you justify the validity of this finding?  What might compromise the validity of the finding?

> One unit of change (being homeschooled to not being homeschooled) would result in 40 units of change in the SAT score. In this case it seems likely that *being* home schooled contributes -40 whereas *not being home schooled* is our baseline. In terms of justification, we would want to know more about the beta coefficient, and about our model in general. We should start by asking some questions:
  * Does the homeschooled_beta have a good R-squared value?
    * If not -- we may not __want__ to justify this finding.
    * If so, it's more likely that being home-schooled contributes to SAT scores negatively
  * Does our model have low or high cross-validation errors?
    * If the model is really BAD at predicting SAT scores then we shouldn't justify this specific finding either.
    * If the model does very well, we might still be picking up on a signal due to common cause or other types of confounding variables
  * What does our intuition say?
    * This finding makes sense -- traditional schools target topics that are on the SAT and parents who are home-schooling are much less likely to teach those topics.

> If we're still quite skeptical about this, we could design an experiment or study to JUST examine the impact of homeschooling on SAT scores.


2. You fit a logistic regression to predict whether or not a student was admitted to a 4-year university. This time `Beta_homeschool = -0.3`. Do we predict that more or less homeschoolers are admitted? Are 30% more/less homeschoolers admitted? How do you justify this finding?

> While the beta coefficients do have meaning in logistic regression, they aren't as interpretable as they are in linear regression. Generally speaking people talk about logistic regression parameters in terms of the odds ratio, or the log odds ratio, rather than the coefficients directly. So the odds ratio for this Beta is e^-.3 which is:

```
In [2]: np.exp(-.3)
Out[2]: 0.74081822068171788
```

> So, our odds ratio for homeschool is .7408 which means that the odds of being admitted are ~.74 as large as the odds otherwise. This isn't *quite* the same as saying that a homeschooled person is 3/4ths as likely to get into college as someone who was not homeschooled, but it DOES suggest that they are less likely to be admitted. Justifying this finding is harder as the log(odds) is tougher to interpret and the r-squared values are less meaningful in logistic regression.

> As before, if we're still quite skeptical about this, we could design an experiment or study to JUST examine the impact of homeschooling on SAT scores.

3. Give an example of a confusion matrix with precision > 90% and recall < 10%.

```
[         Predictions:  P   , N
  actually_positive -> [ 10 , 1  ]
  actually_negative -> [ 2  , 499 ]
]
```

> In the above example we have a sample size of 512, 12 positive classifications (two of which were false positives); 500 negative classifications (one of which was a false negative).

> Recall is concerned with how many real positive values we detected out of the space of positive samples: 10 / 11  
> Precision is concerned with what percent of our positive classifications were correct: 10/12

4. Give an example of a confusion matrix with accuracy > 90%, but both precision < 10% and recall < 10%.

```
[         Predictions:  P   , N
  actually_positive -> [ 1  , 10  ]
  actually_negative -> [ 11 , 500 ]
]
```

> We've only made some slight modifications to our previous matrix. This time, 501/521 were classified correctly (accuracy). However, our recall and precision were both atrocious!

> Recall: 1/11  
> Precision: 1/12

> We relied on the fact that MOST of our data is negative and we mostly classed things negatively to drive up accuracy. We could have even achieved this result by NEVER classifying positive (we only made one such classification). This is a good example of why 'accuracy' alone is not a very useful metric.


5. Take a look at this ROC plot. Assume that we're building a model for a spam filter. We prefer to let spam messages go to the inbox rather than to let nonspam go to the spam folder. Interpreting a true positive as correctly identifying spam, which model should we choose?

> Neither of these models behave very well for this particular purpose. Both are relatively close to the "flip a coin" line and I would not suggest using either in production software. With that out of the way, I would choose model B (red line) with a threshold associated with the left hand side of the curve -- with spam we really cannot afford a high false negative rate, so by the time that model A achieves a higher true positive rate we are already getting too many false positives.


6. Looking at the same ROC plot, assume that we're building a model for a fraud detector. There is a huge cost to missing potential fraud. If we suspect something as fraud we will investigate it further.  Interpreting a true positive as correctly identifying fraud which model should we choose?

> In this case I would choose model B somewhere near the right hand side of the space (after the two curves intersect). Model B gets a nice little peak around .7-.8 on the X axis -- picking a threshold near there would allow us to nearly always catch true fraud and our customer service team would be making a healthy number of calls to innocent people who are not being defrauded or committing fraud -- which is fine.


7. Say I'm building a Decision Tree Classifier on this dataset.

    | color | number | label |
    | ----- | ------ | ----- |
    | blue  | 1      | 0     |
    | blue  | 2      | 1     |
    | red   | 1      | 0     |
    | red   | 5      | 1     |

    Splitting on what feature and value has the best information gain? Use your intuition rather than calculating all the entropy values.

> Splitting on number <= 1 gives us perfect homogeny in labels. We should do that.


8. Say I'm building a Decision Tree Regressor. What is the information gain of this split of the data?

    ```
    Split A: 6, 5, 8, 8
    Split B: 5, 4, 2, 4, 4
    ```
```
Information Gain == entropy_before_split - entropy_after_split
Entropy_after_split == (elementsInLeft/AllElements)*entropy_left + (elementsInRight/allElements)*entropy)right
 => (4.0/9)*entropy([6, 5, 8, 8]) + (5.0/9)*entropy([5, 4, 2, 4, 4]) => 1.4812641101513417 # scipy.stats.entropy

 entopy_before = entropy([6,5,8,8,5,4,2,4,4]) => 2.12999297689898  # scipy.stats.entropy
 entropy_after = 1.4812641101513417

 information_gain = 2.12 - 1.48 =~ 0.648
```

9. You build a Decision Tree and get these stats:

    ```
    train set accuracy:  90%
    train set precision: 92%
    train set recall:    87%

    test set accuracy:   60%
    test set precision:  65%
    test set recall:     52%
    ```

    What's going on? What tactic(s) do we have to modify our Decision Tree to fix the issue?

> Unfortunately, we seem to be overfitting our data. We might want to restrict the tree depth somehow (max splits, min_samples required to split, min_samples required in a leaf ... ). That said, decision trees do have a propensity to overfit -- we might want to use a Random Forest or a Boosting tactic in concert with this single tree to improve outcomes.


10. How are the Decision Trees in Random Forests different from standard Decision Trees?

> Typically, they will be trained on a bootstraped sample of the original data, and they will also not have every feature available to them for splitting at each branch -- instead a *random* subset of the features will be chosen before splitting, and the split will only be able to consider those selected features.


11. Why are we able to cross validate our Random Forest with our training set (OOB error)? I.e. Why doesn't this count as testing on my training set?

> It would be wrong to say that we don't still *need* a test set for our final model score. As with cross validation we are leaving data points out of training, and validating on the subset of points that were left out. With Out Of Bag error, because we are using bootstrapping-with-replacement, some of our datapoints are already left out of the training set. Testing on these "out of bag" data points is the same as intentionally slicing out some of our data ahead of time -- in both cases the algorithm has not trained on the left out data-points, the mechanism for leaving them out has just changed somewhat.


12. Say I have 50 machines that I can use to build my model. Which of these ensemble methods can utilize multiple machines?

    * Random Forest
    * Gradient Boosting
    * AdaBoost

> Only the random forest can be efficiently parallelized -- GradientBoosting and AdaBoost both rely on the result of the previous weak-predictor to begin the training of the subsequent weak-predictor. Because random forests are made with independent trees and rely on consensus at the end, we can train the trees independently (and therefore in a cluster).


13. In binary decision tree scikit-learn boosting, how many total leaf nodes are produced with a `max_depth` hyperparameter set to n?  Would we expect our prediction score to improve or be reduced if we instead used the `max_leaf_nodes` hyperparameter set to the previous answer for the total number of leaf nodes produced?

> In a max depth 1, we have *up-to* 3 nodes. 2 depth -> *up-to* 8... The number of leafs in a binary tree for depth n is __less than or equal to__ 2^n. If the tree is forced to be complete, it will be exactly 2^n.

> Setting max_leaf_nodes might cause some branches to split VERY DEEP and some other branches to not split very deeply at all. A tree that always split the deepest left most node with a max_leaf_nodes of 8 would end up with a max_depth of 7 (much greater than 3), and 8 leaf nodes. This gives the tree more opportunity to overfit our data since it can slice a single group into many more buckets.


14. In boosting, what is the relationship between the hyperparameters `learning_rate` and `n_estimators`?

> The learning rate applies to each estimator in n_estimators. When we have more estimators, we'll often choose a smaller learning rate to reduce the impact at each tree and converge to an answer more slowly.


15. In boosting, why might we want to tune `max_features` and `sub_sample`? What purpose does it serve?

> Similarly to Random Forests, we want to use these methods to give variability to our individual estimators. Doing so allows the individual estimators to "focus" on a particular portion of the data or a particular portion of the feature space. Since we're relying on "the wisdom of the crowds" we want our individual estimators to have a little bit of specialty.


16. In Random Forests, what do you expect to happen to the test error as you build more trees? How is this different from increasing the number of trees in Boosting?

> In forests, more trees are typically going to be better for random forests. The trees "average each other out" in random forests -- they each have a slightly different take and form consensus at the end. With boosting -- we still risk overfitting if we have too many estimators. Because each estimator BUILDS ON the solution from the previous estimator, we can build enough weak-estimators that by the end they have completely fine-tuned the residuals, causing our test error to go up.


17. Name the tuning parameters for the following algorithms and describe what you'd expect to happen with bias and variance as you increase the tuning parameter.

    * Lasso / Ridge
    > The regularization constant, alpha. We essentially use this value to punish high variance models. A larger alpha value adds a higher penalty for higher beta coefficients -- as we make alpha larger we should see models with more bias, with lower models we should see higher variance.

    * SVM
    > Slack, the squiggle. Slack is the "amount we can be wrong by". It's hard for me to talk about bias and variance in SVM's still, but my understanding of slack is that as our slack increases, we're considering more points "Support Vectors" which are the values that affect our predicitons. In this way I would say increasing slack will increase the variance of the model by causing it to consider more values when picking the decision boundary.
