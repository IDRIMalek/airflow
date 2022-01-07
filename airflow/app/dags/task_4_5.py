import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from joblib import dump


#def Xydatas():
#    X=pd.read_csv(os.path.join('/app/clean_data', 'X.csv'))
#    y=pd.read_csv(os.path.join('/app/clean_data', 'y.csv'))
#    return X, y

def func_4p(task_instance):
    #Score pour LinearRegression
    #X, y = Xydatas()
    score_lr = compute_model_score(LinearRegression(), X, y)
    task_instance.xcom_push(key='model_accuracy', value=score_lr)


def func_4pp(task_instance):
    #Score pour DecisionTreeRegressor
    #X, y =prepare_data('/app/clean_data/fulldata.csv')
    score_dt = compute_model_score(DecisionTreeRegressor(), X, y)
    task_instance.xcom_push(key='model_accuracy', value=score_dt)


def func_4ppp(task_instance):
    #Score pour RandomForestRegressor
    #X, y =prepare_data('/app/clean_data/fulldata.csv')
    score_rfr = compute_model_score(RandomForestRegressor(), X, y)
    task_instance.xcom_push(key='model_accuracy', value=score_rfr)

def func_5(task_instance):
    #X, y =prepare_data('/app/clean_data/fulldata.csv')
    #Lise des scores des model_accuracy
    list_scores=task_instance.xcom_pull(
    key="model_accuracy",
    task_ids=["LinearRegression", "DecisionTreeRegressor", "RandomForestRegressor"]
    )
    #Selection du meilleur model accuracy
    score_max=max(list_scores)
    print('score_max =>',score_max)
    list_ml=[LinearRegression(),DecisionTreeRegressor(),RandomForestRegressor()]
    #Reentrainnement du model et sauvegarde de ce model dans clean_data/best_model.pickle
    train_and_save_model(
        list_ml[list_scores.index(score_max)],
        X,
        y,
        '/app/clean_data/best_model.pickle'
    )

def compute_model_score(model, X, y):
    # computing cross val
    cross_validation = cross_val_score(
        model,
        X,
        y,
        cv=3,
        scoring='neg_mean_squared_error')

    model_score = cross_validation.mean()

    return model_score


def train_and_save_model(model, X, y, path_to_model='/app/clean_data/model.pckl'):
    # training the model
    model.fit(X, y)
    # saving model
    print(str(model), 'saved at ', path_to_model)
    dump(model, path_to_model)




