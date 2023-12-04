import pandas as pd
import sys 
import os
sys.path.append('src/models')
sys.path.append('src/visualization')
sys.path.append('src/data')
from support_vector_machine import support_vector_machine
from randomforest_classifier import randomforest_classifier
from decision_tree_classifier import decision_tree_classifier
from plot_results import plot_results
from combine_tables import combine_tables

def update_plot_playground(currencies, include_sp500, lag, train_size, random_seed, dtc_active, rfc_active, svm_active, dtc_long_only, rfc_long_only, svm_long_only,
                           dtc_max_depth, rfc_max_depth, rfc_trees, rfc_leaves):
    #Import our data
    log_returns_currencies = pd.read_csv("../data/processed/log_returns_currency_data.csv")
    log_returns_spx = pd.read_csv("../data/processed/log_returns_spx_data.csv")
    dataframe = pd.merge(log_returns_currencies, log_returns_spx.iloc[1:], on='DATE', how='inner')

    #Train the models that are set to active
    active_models = []
    if dtc_active == True:
        dt_accuracies, dt_results = decision_tree_classifier(dataframe, currencies, include_sp500, lag, train_size, random_seed, dtc_long_only, dtc_max_depth)
        active_models.append(dt_results)
    if rfc_active == True:
        rf_accuracies, rf_results = randomforest_classifier(dataframe, currencies, include_sp500, lag, train_size, random_seed, rfc_long_only, rfc_trees, rfc_max_depth, rfc_leaves)
        active_models.append(rf_results)
    if svm_active == True:
        svm_accuracies, svm_results = support_vector_machine(dataframe, currencies, include_sp500, lag, train_size, random_seed, svm_long_only)
        active_models.append(svm_accuracies)
    #Combine the results tables of the active trained models and plot the final results
    results = combine_tables([dt_results, rf_results, svm_results])
    plot_results(results, include_sp500)

