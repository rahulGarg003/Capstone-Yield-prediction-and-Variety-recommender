import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
from pandas.plotting import scatter_matrix
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import time
from datetime import datetime

import multiprocessing as mp
from sklearn.model_selection import train_test_split, GridSearchCV

#from bs4 import BeautifulSoup
#from urllib.request import urlopen
import csv

#from selenium import webdriver
#from selenium.webdriver.support.ui import Select
#from selenium.webdriver.common.keys import Keys
#import selenium
import time

class MyModel():
    '''
    '''

    def __init__(self):

        self.lr = LinearRegression()
        self.gbr = GradientBoostingRegressor()
        self.rf = RandomForestRegressor()

    def fit(self, X, y):

        processes = [mp.Process(target=self.lr.fit,
                                args=(X, y)),
                     mp.Process(target=self.gbr.fit,
                                args=(X, y)),
                     mp.Process(target=self.rf.fit,
                                args=(X, y))]
        for p in processes:
            p.start()

        for p in processes:
            p.join()

    def predict(self, X):

        (self.predictions_lr, self.predictions_gbr, self.predictions_rf
        = self.lr.predict(X), self.gbr.predict(X), self.rf.predict(X))

        return self.predictions_lr, self.predictions_gbr, self.predictions_rf

    def score(self, y):

        self.score_lr = mean_squared_error(self.predictions_lr, y)
        self.score_gbr = mean_squared_error(self.predictions_gbr, y)
        self.score_rf = mean_squared_error(self.predictions_rf, y)

        return self.score_lr, self.score_gbr, self.score_rf

    def cv_params(self, X, y, param_grid_rf, param_grid_gb, cv=5):

        cv_params_rf = GridSearchCV(estimator=self.rf, param_grid=param_grid_rf,
                                    scoring=mean_squared_error, n_jobs=-1)

        cv_params_gbr = GridSearchCV(estimator=self.gbr, param_grid=param_grid_gb,
                                    scoring=mean_squared_error, n_jobs=-1)

        processes = [mp.Process(target=cv_params_rf.fit,
                                args=(X, y)),
                     mp.Process(target=cv_params_gbr.fit,
                                args=(X, y))]
        for p in processes:
            p.start()

        for p in processes:
            p.join()

        rf_best_params = cv_params_rf.best_estimator_,
                         cv_params_rf.best_score_ ** 0.5,
                         cv_params_rf.best_params_

        gbr_best_params = cv_params_gbr.best_estimator_,
                         cv_params_gbr.best_score_ ** 0.5,
                         cv_params_gbr.best_params_

        return rf_best_params, gbr_best_params

    def cv(self, X_train, y_train, k=5):

        RMS = []
        kf = KFold(n_splits=k)

        for train_index, test_index in kf.split(X_train):

            x_train, x_test = X_train[train_index], X_train[test_index]
            Y_train, Y_test = y_train[train_index], y_train[test_index]

            linear =  LinearRegression()
            linear.fit(x_train, Y_train)

            train_predicted = linear.predict(x_train)
            test_predicted = linear.predict(x_test)

            RMS.append(mean_squared_error(Y_test, test_predicted) ** 0.5)
            #RMS.append(np.sqrt(mean_squared_error(Y_test, test_predicted)))
        return np.mean(RMS)

    def cv_score(self, X_train, y_train, k=5):

        RMS = []
        kf = KFold(n_splits=k)

        for train_index, test_index in kf.split(X_train):

            x_train, x_test = X_train[train_index], X_train[test_index]
            Y_train, Y_test = y_train[train_index], y_train[test_index]

            linear =  LinearRegression()
            linear.fit(x_train, Y_train)

            train_predicted = linear.predict(x_train)
            test_predicted = linear.predict(x_test)

            RMS.append(mean_squared_error(Y_test, test_predicted) ** 0.5)
            #RMS.append(np.sqrt(mean_squared_error(Y_test, test_predicted)))
        return np.mean(RMS)
