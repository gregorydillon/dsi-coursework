# Assessment 5: Profit Curves, Web Scraping, NLP, Naive Bayes and Clustering

1. Complete this function that will give the number of jobs on indeed from a search result.

    ```python
    import requests
    from bs4 import BeautifulSoup

    def number_of_jobs(query):
        '''
        INPUT: string
        OUTPUT: int

        Return the number of jobs on the indeed.com for the search query.
        '''

        url = "http://www.indeed.com/jobs?q=%s" % query.replace(' ', '+')

        ### YOUR CODE HERE ###
        r = requests.get(url)
        html = r.content
        soup = BeautifulSoup(html, 'html.parser')
        sc_div = soup.select('#searchCount')[0]
        blank_of_blank = sc_div.text

        return blank_of_blank.split('of')[-1].strip()
    ```

2. Say I am detecting fraud. If I identify a user as fraud, I will call them to confirm their identity. This costs $10. Catching fraud saves us $100. What does my cost benefit matrix look like?

> One way to think about this is:
```
                 predictedFraud     predictedNot
actuallyFraud        $90                 0
actuallyNot         -$10                 0
```

> An alternative that assumes a different baseline, but that should be equivalent:
```
                 predictedFraud     predictedNot
actuallyFraud       -$10               -$100
actuallyNot         -$10                 0
```

> In both these cases, the difference between missing fraud and catching fraud is $90, and in both cases the cost of predicting fraud when there is none, is $10. In the first, we assume we "make money" against our baseline by predicting fraud, in the second our baseline doesn't assume frauds are already losses, and so we can really only "lose less money" rather than earning. I'd take the former to the Board of Directors or CEO -- they like to MAKE money more than then like to "not lose" money. ;)

3. We've built two different models for fraud which result in the following two confusion matrices.

    ```
            Model 1:                          Model 2:
                    Actual                            Actual
                    Y    N                            Y    N
                  -----------                       -----------
               Y | 150 | 150 |                   Y | 200 | 500 |
    Predicted     -----------         Predicted     -----------
               N |  50 | 650 |                   N |   0 | 300 |
                  -----------                       -----------
    ```

    Using your cost-benefit matrix from above, which model gives us the most profit?

> I did these two computations based on my profit matrix from above:

```
In [11]: 90*150 + 150* -10
Out[11]: 12000

In [12]: 200*90 + 500*-10
Out[12]: 13000
```

> I conclude that the matrix on the right is better for us. Capturing the extra 50 true positives made up for the additional 450 false positives.

4. Consider a corpus made up of the following four documents:

```
  Doc 1: Dogs like dogs more than cats.
  Doc 2: The dog chased the bicycle.
  Doc 3: The cat rode in the bicycle basket.
  Doc 4: I have a fast bicycle.
```

  We assume that we are lowercasing everything, lemmatizing, and removing stop words and punctuation. These are the features you should have:

  `dog, like, cat, chase, bicycle, ride, basket, fast`

  For these questions, don't worry about normalizing the results.

  * What is the term frequency vector for Document 1?
  > Parallel to the features extracted:
  ```
   dog, like, cat, chase, bicycle, ride, basket, fast
  [ 2,    1    1    0       0       0      0       0]
  ```

  * What is the document frequency vector for all the words in the corpus?
  > again, this will be parallel to the vocabulary:
  dog, like, cat, chase, bicycle, ride, basket, fast
 [ 2,    1    2    1       3       1      1       1]

5. Given the same documents, use python to build the tf-idf vectors and calculate the cosine similarity of each document with each other document. For your convenience, here's the data in a python list:

    ```python
    documents = ["Dogs like dogs more than cats.",
                 "The dog chased the bicycle.",
                 "The cat rode in the bicycle basket.",
                 "I have a fast bicycle."]
    ```

    Which two documents are the most similar?

    Please include your code in your solution.
```python
documents = ["Dogs like dogs more than cats.",
             "The dog chased the bicycle.",
             "The cat rode in the bicycle basket.",
             "I have a fast bicycle."]
vect = TfidfVectorizer()
X = vect.fit_transform(documents)
from scipy.spatial.distance import cosine
dense_X = X.todense()
for i, v in enumerate(dense_X):
for j, v2 in enumerate(dense_x):
    d = cosine(v, v2)
    print d, i, j
for i, v in enumerate(dense_X):
for j, v2 in enumerate(dense_X):
    d = cosine(v, v2)
    print d, i, j

    ```

    Results in:

```

1.0 0 1
1.0 0 2
1.0 0 3
0.50178745699 1 2
0.881304369244 1 3
0.899993493364 2 3
```

> these results look wrong... document 0 is evidently exactly similar to everything? I would say it looks like documents 2 and 3 are the most similar. 

6. What is wrong with this approach to building my feature matrix?

    We assume that `documents` is a list of the text of emails, each as a string. `y` is an array of 0, 1 labels of whether or not the email is spam.

    ```python
    vect = TfidfVectorizer(stop_words='english')
    X = vect.fit_transform(documents)
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    log_reg = LogisticRegression()
    log_reg.fit(X_train, y_train)
    print "Accuracy on test set:", log_reg.score(X_test, y_test)
    ```

    Redo the code to fix the issue.

7. Why do we need to do Laplace Smoothing in Naive Bayes?

> If we do not, we may end up with 0 probabilities because not every feature occurs in every data-point. If we encounter such a point when doing the bayesian update we will send our probabilities instantly to 0 and never recover.

8.  Suppose N = 100 represents a dense sample for a three dimensional feature space.  
To achieve same density in an eight dimensional feature space, how many points would we need?

9.  The first step in the K-means algorithm involves randomly assigning data points
to clusters, and as such, only finds local minimums.  How do we typically deal with this?

> A simplistic solution is to pick several starting initializations and choose the one that performs best. There are multiple ways to choose the initial locations (randomly, furthest away ... ) so pick a few of these and perform K-means for each initialization. Note that if your choice is stochastic, you can choose multiple without changing the paradigm for picking and still get different results.

10.  Describe the process of varying K in K-means.  Contrast this with the process of
varying K in the hierarchical clustering setting.  

> In K-Means varying the number of centroids must be done prior to training/fitting the data. We select the number of centroids and then shuffle them around according to the algorithm. If we wish to pick a new K, we must refit the data. For hierarchical clustering, the algorithm builds the clusters up from "clusters" of size 1 (from the individual datapoints), and joins the set of clusters one cluster at a time. As a result of this process, setting K in hierarchical clustering can be done AFTER the data has been fit. We choose K by setting a threshold in the height of the dendrogram.
