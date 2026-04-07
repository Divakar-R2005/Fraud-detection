import pandas as pd
from src.preprocessor import FraudPreprocessor
from src.trainer import FraudTrainer
import os

def run_pipeline():
    # 1. Load Data
    print("Loading data...")
    # Update 'creditcard.csv' if your filename is different
    df = pd.read_csv('data/creditcard.csv') 

    # 2. Preprocess
    preprocessor = FraudPreprocessor()
    X, y = preprocessor.prepare_data(df)
    X_train, X_test, y_train, y_test = preprocessor.split_data(X, y)

    # 3. Train
    trainer = FraudTrainer()
    trainer.train(X_train, y_train)

    # 4. Evaluate
    trainer.evaluate(X_test, y_test)

    # 5. Save
    if not os.path.exists('models'):
        os.makedirs('models')
    trainer.save_model()
    preprocessor.save_scaler()

if __name__ == "__main__":
    run_pipeline()

