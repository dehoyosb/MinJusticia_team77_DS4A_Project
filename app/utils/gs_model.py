from sklearn.model_selection import GridSearchCV

# Gridsearch 
def model_search(X_train, y_train, models, params):
    results = dict()
    for name in models.keys():
        print(name)
        mcv = GridSearchCV(estimator = models[name], param_grid = params[name], cv = 5, n_jobs = -1)
        mcv.fit(X_train, y_train)
        results[name] = mcv.best_estimator_
    return results