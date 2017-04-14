import graphlab

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

data = np.genfromtxt('recommendation-systems-files/data/u.data')

data2 = pd.DataFrame(data)

data = data2

data.describe()

data.shape

data.columns = ['user_id', 'item_id', 'rating', 'timestamp']

data = data.drop('timestamp', axis = 1)
data.user_id = data.user_id.astype(int)
data.item_id = data.item_id.astype(int)

data.head()

df = graphlab.SFrame(data)

df.head()

def create_violins(model):
    one_datapoint_sf = graphlab.SFrame({'user_id': [1], 'item_id': [100]})

    model.predict(one_datapoint_sf) # 5.02 (THEY WILL REALLY LOVE IT!)

    model.list_fields()

    coef = model.get('coefficients')
    dir(coef)
    coef.keys()

    movie_100 = coef.get('item_id')[100]
    movie_100_factors = np.array(movie_100['factors'])

    user_1 = coef.get('user_id')[1]
    user_1_factors = np.array(user_1['factors'])

    pred = movie_100_factors.dot(user_1_factors)
    pred

    pred + coef['intercept'] # 4.98 (calling it good)

    coef['intercept']

    predictions = model.predict(df)

    predictions[:3]
    predictions[:50]

    model['training_rmse']

    pred_summary = pd.Series(predictions).describe()

    pred_summary


    data.rating.describe()


    pred_df = pd.Series(predictions)
    more_than_5 = pred_df[pred_df > 5]
    len(more_than_5)

    ones = df[df['rating'] == 1]
    len(ones)

    # plt.scatter(df['rating'], predictions, alpha=.2)
    pos = [1,2,3,4,5]

    violin_data = [ predictions[df['rating'] == true_rating] for true_rating in pos]
    plt.violinplot(violin_data, pos)
    plt.show()



model = graphlab.recommender.factorization_recommender.create(df, target = 'rating', solver='als')

model2 = graphlab.recommender.factorization_recommender.create(df, target = 'rating', solver='als', regularization=0.0003)


model3 = graphlab.recommender.factorization_recommender.create(df, target = 'rating', solver='als', regularization=0)

fig, ax_list = plt.subplot(3)
create_violins(model)

create_violins(model2)

create_violins(model3)

# NEED TO CREATE TRAINING/VALIDATION
training, validation = df.random_split(0.8)

params = {'regularization': [1e-7, 1e-8, 1e-9], 'num_factors': [5, 8, 10, 15], 'target': ['rating']}
best = graphlab.model_parameter_search.create((training, validation), graphlab.recommender.factorization_recommender.create, params)
