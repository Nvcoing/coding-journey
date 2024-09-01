from sklearn.model_selection import GridSearchCV

def perform_grid_search(model, param_grid, X_train, y_train):
    """
    Perform GridSearchCV to find the best hyperparameters for a given model.
    
    Parameters:
        - model: The model object to tune.
        - param_grid: The parameter grid containing hyperparameters to search over.
        - X_train: The feature matrix of the training data.
        - y_train: The target vector of the training data.
        
    Returns:
        - best_model: The best model found by GridSearchCV.
        - best_params: The best parameters found by GridSearchCV.
        - best_score: The best score achieved by the best model.
    """
    # Create GridSearchCV
    grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')
    
    # Fit the GridSearchCV instance
    grid_search.fit(X_train, y_train)
    
    # Get the best parameters and best score
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    best_score = grid_search.best_score_
    
    return grid_search,best_model, best_params, best_score

# Example usage:
# best_svm, best_params_svm, best_score_svm = perform_grid_search(SVC(), param_grid, X_train, y_train)
