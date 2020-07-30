# Libraries
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors    import KNeighborsClassifier
from sklearn.tree         import DecisionTreeClassifier
from sklearn.ensemble     import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes  import GaussianNB

# Models
# Define models
models = dict()
models['LR' ] = LogisticRegression()
models['NB' ] = GaussianNB()
models['KNN'] = KNeighborsClassifier()
models['DT' ] = DecisionTreeClassifier()
models['RF' ] = RandomForestClassifier(random_state = 10)
models['GB' ] = GradientBoostingClassifier(random_state = 10)

# Define parameters for GridSearch
params = dict()

params['LR' ] = {'penalty':['l1','l2'], 
                 'C'      :[0.1, 0.4, 0.8, 1.0], 
                 'solver' :['saga']}

params['NB' ] = {} # no hyperparameters to tune

params['KNN'] = {'n_neighbors':[3, 5, 10], 
                 'leaf_size'  :[5,15,30],
                 'p'          :[1,2]}

params['DT' ] = {'max_depth'   :[3, 20, 100, 150]  , 
                 'max_features':['auto','sqrt','log2']}

params['RF' ] = {'n_estimators'    :[20,50,100],
                 'max_depth'       :[3, 20, 100], 
                 'max_features'    :['auto','sqrt','log2'], 
                 'min_samples_leaf':[2,4,8]}

params['GB' ] = {}