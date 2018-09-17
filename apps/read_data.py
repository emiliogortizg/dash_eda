# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

index = 'account_uuid'
output_name = 'convert'

# Read accounts and quotes data
df_accounts = pd.read_csv('raw/accounts_train.csv', encoding='utf8')
df_quotes = pd.read_csv('raw/quotes_train.csv', encoding='utf8')

# Merge them on 'account_uuid'
df = pd.merge(df_accounts, df_quotes, on=index)

# Clean features
df.loc[df['year_established'] < 1860, 'year_established'] = np.NaN
df.loc[df['year_established'] > 2018, 'year_established'] = 2018

# Correct types
df['carrier_id'] = df['carrier_id'].astype(object)

column_names = list(df.columns)
column_names.remove(index)
column_names.remove(output_name)
