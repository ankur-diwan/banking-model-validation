"""
Synthetic Data Generator for Banking Scorecards
Generates realistic synthetic data for testing and validation
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from faker import Faker
import random


class ScorecardDataGenerator:
    """
    Generate synthetic data for different types of scorecards
    """
    
    def __init__(self, seed: int = 42):
        """
        Initialize data generator
        
        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        np.random.seed(seed)
        random.seed(seed)
        self.faker = Faker()
        Faker.seed(seed)
    
    def generate_application_scorecard_data(
        self,
        n_samples: int = 10000,
        product_type: str = "unsecured",
        default_rate: float = 0.05
    ) -> pd.DataFrame:
        """
        Generate synthetic application scorecard data
        
        Args:
            n_samples: Number of samples to generate
            product_type: Type of product (secured, unsecured, revolving)
            default_rate: Target default rate
            
        Returns:
            DataFrame with synthetic application data
        """
        data = {
            'application_id': [f'APP{i:08d}' for i in range(n_samples)],
            'application_date': [
                self.faker.date_between(start_date='-2y', end_date='today')
                for _ in range(n_samples)
            ],
            
            # Demographic features
            'age': np.random.normal(45, 15, n_samples).clip(18, 80).astype(int),
            'income': np.random.lognormal(10.5, 0.8, n_samples).clip(20000, 500000),
            'employment_length_months': np.random.exponential(60, n_samples).clip(0, 480).astype(int),
            'education_level': np.random.choice(
                ['High School', 'Some College', 'Bachelor', 'Graduate'],
                n_samples,
                p=[0.3, 0.25, 0.35, 0.1]
            ),
            'marital_status': np.random.choice(
                ['Single', 'Married', 'Divorced', 'Widowed'],
                n_samples,
                p=[0.35, 0.45, 0.15, 0.05]
            ),
            'dependents': np.random.poisson(1.2, n_samples).clip(0, 8),
            
            # Credit bureau features
            'credit_score': np.random.normal(680, 80, n_samples).clip(300, 850).astype(int),
            'num_credit_lines': np.random.poisson(5, n_samples).clip(0, 30),
            'total_credit_limit': np.random.lognormal(10, 1, n_samples).clip(1000, 200000),
            'credit_utilization': np.random.beta(2, 5, n_samples).clip(0, 1),
            'num_delinquencies_2y': np.random.poisson(0.3, n_samples).clip(0, 10),
            'num_inquiries_6m': np.random.poisson(1, n_samples).clip(0, 15),
            'oldest_account_months': np.random.exponential(100, n_samples).clip(0, 600).astype(int),
            'public_records': np.random.poisson(0.1, n_samples).clip(0, 5),
            
            # Application specific
            'requested_amount': self._generate_requested_amount(n_samples, product_type),
            'loan_purpose': np.random.choice(
                ['debt_consolidation', 'home_improvement', 'major_purchase', 
                 'medical', 'vacation', 'other'],
                n_samples,
                p=[0.35, 0.20, 0.15, 0.10, 0.05, 0.15]
            ),
            'dti_ratio': np.random.beta(3, 5, n_samples).clip(0, 0.8),
            'housing_status': np.random.choice(
                ['Own', 'Mortgage', 'Rent'],
                n_samples,
                p=[0.25, 0.45, 0.30]
            ),
        }
        
        # Add product-specific features
        if product_type == "secured":
            data['collateral_value'] = data['requested_amount'] * np.random.uniform(1.2, 2.0, n_samples)
            data['ltv_ratio'] = data['requested_amount'] / data['collateral_value']
        
        df = pd.DataFrame(data)
        
        # Generate target variable (default) based on risk factors
        df['default'] = self._generate_default_target(df, default_rate)
        
        # Generate derived features
        df['income_to_loan_ratio'] = df['income'] / df['requested_amount']
        df['months_since_oldest_account'] = df['oldest_account_months']
        
        return df
    
    def generate_behavioral_scorecard_data(
        self,
        n_samples: int = 10000,
        product_type: str = "unsecured",
        default_rate: float = 0.03
    ) -> pd.DataFrame:
        """
        Generate synthetic behavioral scorecard data
        
        Args:
            n_samples: Number of samples to generate
            product_type: Type of product
            default_rate: Target default rate
            
        Returns:
            DataFrame with synthetic behavioral data
        """
        data = {
            'account_id': [f'ACC{i:08d}' for i in range(n_samples)],
            'observation_date': [
                self.faker.date_between(start_date='-1y', end_date='today')
                for _ in range(n_samples)
            ],
            'account_age_months': np.random.exponential(24, n_samples).clip(1, 120).astype(int),
            
            # Account balance features
            'current_balance': np.random.lognormal(9, 1.5, n_samples).clip(0, 100000),
            'credit_limit': np.random.lognormal(10, 1, n_samples).clip(1000, 100000),
            'utilization_rate': np.random.beta(2, 5, n_samples).clip(0, 1),
            'available_credit': lambda: data['credit_limit'] * (1 - data['utilization_rate']),
            
            # Payment behavior
            'months_since_last_payment': np.random.exponential(1, n_samples).clip(0, 12).astype(int),
            'num_payments_last_12m': np.random.poisson(11, n_samples).clip(0, 12),
            'avg_payment_amount': np.random.lognormal(6, 1, n_samples).clip(50, 10000),
            'payment_to_balance_ratio': np.random.beta(3, 2, n_samples).clip(0, 1),
            
            # Delinquency features
            'days_past_due': np.random.choice(
                [0, 30, 60, 90, 120],
                n_samples,
                p=[0.85, 0.08, 0.04, 0.02, 0.01]
            ),
            'num_delinquencies_12m': np.random.poisson(0.2, n_samples).clip(0, 12),
            'max_delinquency_12m': np.random.choice(
                [0, 30, 60, 90, 120],
                n_samples,
                p=[0.80, 0.10, 0.05, 0.03, 0.02]
            ),
            
            # Transaction features
            'num_transactions_3m': np.random.poisson(15, n_samples).clip(0, 100),
            'avg_transaction_amount': np.random.lognormal(5, 1, n_samples).clip(10, 5000),
            'num_cash_advances_6m': np.random.poisson(0.5, n_samples).clip(0, 20),
            'total_cash_advance_amount_6m': np.random.lognormal(5, 2, n_samples).clip(0, 10000),
            
            # Trend features
            'balance_trend_3m': np.random.normal(0, 0.2, n_samples).clip(-0.5, 0.5),
            'utilization_trend_3m': np.random.normal(0, 0.1, n_samples).clip(-0.3, 0.3),
            'payment_trend_6m': np.random.normal(0, 0.15, n_samples).clip(-0.4, 0.4),
            
            # External bureau updates
            'credit_score_current': np.random.normal(700, 70, n_samples).clip(300, 850).astype(int),
            'credit_score_change_6m': np.random.normal(0, 30, n_samples).clip(-150, 150).astype(int),
            'num_new_inquiries_3m': np.random.poisson(0.5, n_samples).clip(0, 10),
        }
        
        df = pd.DataFrame(data)
        
        # Calculate derived features
        df['available_credit'] = df['credit_limit'] * (1 - df['utilization_rate'])
        df['months_on_book'] = df['account_age_months']
        
        # Generate target variable
        df['default_next_12m'] = self._generate_behavioral_default(df, default_rate)
        
        return df
    
    def generate_collections_scorecard_data(
        self,
        n_samples: int = 5000,
        stage: str = "early",  # early or late
        recovery_rate: float = 0.4
    ) -> pd.DataFrame:
        """
        Generate synthetic collections scorecard data
        
        Args:
            n_samples: Number of samples to generate
            stage: Collections stage (early or late)
            recovery_rate: Target recovery rate
            
        Returns:
            DataFrame with synthetic collections data
        """
        # Adjust delinquency based on stage
        if stage == "early":
            dpd_mean, dpd_std = 60, 20
            min_dpd, max_dpd = 30, 120
        else:  # late stage
            dpd_mean, dpd_std = 180, 60
            min_dpd, max_dpd = 120, 720
        
        data = {
            'account_id': [f'COL{i:08d}' for i in range(n_samples)],
            'collections_date': [
                self.faker.date_between(start_date='-6m', end_date='today')
                for _ in range(n_samples)
            ],
            
            # Delinquency information
            'days_past_due': np.random.normal(dpd_mean, dpd_std, n_samples).clip(min_dpd, max_dpd).astype(int),
            'delinquent_amount': np.random.lognormal(8, 1.5, n_samples).clip(100, 50000),
            'original_balance': np.random.lognormal(9, 1.5, n_samples).clip(500, 100000),
            'months_since_default': np.random.exponential(6, n_samples).clip(1, 36).astype(int),
            
            # Account history
            'account_age_months': np.random.exponential(36, n_samples).clip(6, 180).astype(int),
            'num_previous_delinquencies': np.random.poisson(2, n_samples).clip(0, 20),
            'max_previous_dpd': np.random.choice(
                [0, 30, 60, 90, 120],
                n_samples,
                p=[0.2, 0.3, 0.25, 0.15, 0.1]
            ),
            
            # Customer information
            'customer_age': np.random.normal(42, 14, n_samples).clip(21, 75).astype(int),
            'income_estimated': np.random.lognormal(10.3, 0.9, n_samples).clip(15000, 300000),
            'employment_status': np.random.choice(
                ['Employed', 'Self-Employed', 'Unemployed', 'Retired'],
                n_samples,
                p=[0.60, 0.15, 0.15, 0.10]
            ),
            
            # Contact information
            'num_contact_attempts': np.random.poisson(8, n_samples).clip(0, 50),
            'num_successful_contacts': np.random.poisson(3, n_samples).clip(0, 30),
            'days_since_last_contact': np.random.exponential(10, n_samples).clip(0, 90).astype(int),
            'num_broken_promises': np.random.poisson(1.5, n_samples).clip(0, 10),
            'contact_rate': np.random.beta(3, 5, n_samples).clip(0, 1),
            
            # Payment behavior in collections
            'num_partial_payments': np.random.poisson(1, n_samples).clip(0, 10),
            'total_payments_received': np.random.lognormal(6, 2, n_samples).clip(0, 20000),
            'payment_to_balance_ratio': np.random.beta(2, 8, n_samples).clip(0, 1),
            'days_since_last_payment': np.random.exponential(30, n_samples).clip(0, 180).astype(int),
            
            # Legal and external factors
            'bankruptcy_flag': np.random.choice([0, 1], n_samples, p=[0.92, 0.08]),
            'legal_action_flag': np.random.choice([0, 1], n_samples, p=[0.85, 0.15]),
            'dispute_flag': np.random.choice([0, 1], n_samples, p=[0.90, 0.10]),
            
            # External bureau
            'current_credit_score': np.random.normal(580, 70, n_samples).clip(300, 750).astype(int),
            'num_other_delinquent_accounts': np.random.poisson(1.5, n_samples).clip(0, 10),
        }
        
        df = pd.DataFrame(data)
        
        # Calculate derived features
        df['delinquency_rate'] = df['delinquent_amount'] / df['original_balance']
        df['contact_success_rate'] = df['num_successful_contacts'] / (df['num_contact_attempts'] + 1)
        df['recovery_ratio'] = df['total_payments_received'] / df['delinquent_amount']
        
        # Generate target variable (recovery)
        df['recovered'] = self._generate_recovery_target(df, recovery_rate, stage)
        df['recovery_amount'] = df['recovered'] * df['delinquent_amount'] * np.random.uniform(0.3, 1.0, n_samples)
        
        return df
    
    def _generate_requested_amount(
        self,
        n_samples: int,
        product_type: str
    ) -> np.ndarray:
        """Generate requested loan amounts based on product type"""
        if product_type == "secured":
            # Higher amounts for secured loans
            return np.random.lognormal(11, 0.8, n_samples).clip(10000, 500000)
        elif product_type == "revolving":
            # Credit card limits
            return np.random.lognormal(9, 0.7, n_samples).clip(1000, 50000)
        else:  # unsecured
            return np.random.lognormal(9.5, 1, n_samples).clip(1000, 100000)
    
    def _generate_default_target(
        self,
        df: pd.DataFrame,
        target_rate: float
    ) -> np.ndarray:
        """Generate default target based on risk factors"""
        # Calculate risk score based on features
        risk_score = (
            -0.3 * (df['credit_score'] - 680) / 100 +
            0.2 * df['dti_ratio'] +
            0.3 * df['credit_utilization'] +
            0.4 * (df['num_delinquencies_2y'] > 0).astype(int) +
            0.2 * (df['num_inquiries_6m'] / 5) +
            -0.2 * (df['income'] / 50000).clip(0, 2) +
            0.3 * (df['public_records'] > 0).astype(int)
        )
        
        # Convert to probability
        prob = 1 / (1 + np.exp(-risk_score))
        
        # Adjust to match target rate
        adjustment = target_rate / prob.mean()
        prob_adjusted = (prob * adjustment).clip(0, 1)
        
        # Generate binary outcome
        return (np.random.random(len(df)) < prob_adjusted).astype(int)
    
    def _generate_behavioral_default(
        self,
        df: pd.DataFrame,
        target_rate: float
    ) -> np.ndarray:
        """Generate behavioral default target"""
        risk_score = (
            0.5 * (df['days_past_due'] > 0).astype(int) +
            0.3 * df['utilization_rate'] +
            0.4 * (df['num_delinquencies_12m'] > 0).astype(int) +
            -0.2 * (df['payment_to_balance_ratio']) +
            0.2 * (df['num_cash_advances_6m'] / 5) +
            0.3 * (df['balance_trend_3m'] > 0.2).astype(int) +
            -0.2 * (df['credit_score_current'] - 700) / 100
        )
        
        prob = 1 / (1 + np.exp(-risk_score))
        adjustment = target_rate / prob.mean()
        prob_adjusted = (prob * adjustment).clip(0, 1)
        
        return (np.random.random(len(df)) < prob_adjusted).astype(int)
    
    def _generate_recovery_target(
        self,
        df: pd.DataFrame,
        target_rate: float,
        stage: str
    ) -> np.ndarray:
        """Generate recovery target for collections"""
        recovery_score = (
            -0.4 * (df['days_past_due'] / 100) +
            0.3 * df['contact_success_rate'] +
            -0.3 * (df['bankruptcy_flag']) +
            -0.2 * (df['legal_action_flag']) +
            0.2 * (df['num_partial_payments'] / 5) +
            0.3 * (df['income_estimated'] / 50000).clip(0, 2) +
            -0.2 * (df['num_other_delinquent_accounts'] / 5) +
            0.2 * (df['employment_status'] == 'Employed').astype(int)
        )
        
        # Late stage has lower recovery probability
        if stage == "late":
            recovery_score -= 1.0
        
        prob = 1 / (1 + np.exp(-recovery_score))
        adjustment = target_rate / prob.mean()
        prob_adjusted = (prob * adjustment).clip(0, 1)
        
        return (np.random.random(len(df)) < prob_adjusted).astype(int)
    
    def generate_validation_dataset(
        self,
        scorecard_type: str,
        product_type: str,
        n_train: int = 10000,
        n_test: int = 3000,
        n_oot: int = 2000
    ) -> Dict[str, pd.DataFrame]:
        """
        Generate complete validation dataset with train, test, and out-of-time samples
        
        Args:
            scorecard_type: Type of scorecard
            product_type: Type of product
            n_train: Number of training samples
            n_test: Number of test samples
            n_oot: Number of out-of-time samples
            
        Returns:
            Dictionary with train, test, and oot DataFrames
        """
        if scorecard_type == "application":
            train = self.generate_application_scorecard_data(n_train, product_type)
            test = self.generate_application_scorecard_data(n_test, product_type)
            oot = self.generate_application_scorecard_data(n_oot, product_type)
        elif scorecard_type == "behavioral":
            train = self.generate_behavioral_scorecard_data(n_train, product_type)
            test = self.generate_behavioral_scorecard_data(n_test, product_type)
            oot = self.generate_behavioral_scorecard_data(n_oot, product_type)
        elif scorecard_type in ["collections_early", "collections_late"]:
            stage = "early" if "early" in scorecard_type else "late"
            train = self.generate_collections_scorecard_data(n_train, stage)
            test = self.generate_collections_scorecard_data(n_test, stage)
            oot = self.generate_collections_scorecard_data(n_oot, stage)
        else:
            raise ValueError(f"Unknown scorecard type: {scorecard_type}")
        
        return {
            "train": train,
            "test": test,
            "out_of_time": oot
        }

# Made with Bob
