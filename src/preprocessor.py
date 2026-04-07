import pandas as pd
import joblib
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split

class FraudPreprocessor:
    def __init__(self):
        # We use RobustScaler because it is less sensitive to outliers
        self.scaler = RobustScaler()

    def save_scaler(self, path='models/scaler.pkl'):
        joblib.dump(self.scaler, path)
        print(f"Scaler saved to {path}")

    def prepare_data(self, df):
        """
        Cleans and scales the raw dataframe.
        """
        # 1. Scale 'Amount' and 'Time' 
        df['scaled_amount'] = self.scaler.fit_transform(df['Amount'].values.reshape(-1, 1))
        df['scaled_time'] = self.scaler.fit_transform(df['Time'].values.reshape(-1, 1))

        # 2. Drop original unscaled columns
        df.drop(['Time', 'Amount'], axis=1, inplace=True)

        # 3. Define Features (X) and Target (y)
        X = df.drop('Class', axis=1)
        y = df['Class']

        return X, y

    def split_data(self, X, y):
        """
        Splits data into train and test sets.
        """
        return train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)