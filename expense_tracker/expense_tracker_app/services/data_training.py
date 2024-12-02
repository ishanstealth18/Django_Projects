import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn import preprocessing
# To be used for splitting the dataset into training and test sets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.preprocessing import OneHotEncoder


real_estate_raw_data = pd.read_excel("D:/Python_Projects/Django_Projects/expense_tracker/updated_data.xlsx")
pd.set_option('display.max_columns', None)
# Creating a dataframe which has columns with numeric values and are required. Normalization and standardization can
# be done on only numeric values
real_estate_df_copy = real_estate_raw_data[["Price($)", "Bedrooms", "Bathrooms", "Size (sqft)", "Visit Counter"]].copy()

print(real_estate_df_copy.describe())

# Divide the data into features (X) and target (Y)
# Data is converted to a panda’s dataframe
X = pd.DataFrame(real_estate_df_copy.values)

print(X.head())

X_train, X_test = train_test_split(X, test_size=0.2)

# Good practice to keep original dataframes untouched for reusability
X_real_estate_data_train_copy = X_train.copy()
X_real_estate_data_test_copy = X_test.copy()

# Fit min-max scaler on training data
norm = MinMaxScaler().fit(X_real_estate_data_train_copy)

# Transform the training data
X_train_norm = norm.transform(X_real_estate_data_train_copy)

# Use the same scaler to transform the testing set
X_test_norm = norm.transform(X_real_estate_data_test_copy)

# Create another dataframe
X_train_norm_df = pd.DataFrame(X_train_norm)
# Assign column names as in the real estate copy data
X_train_norm_df.columns = ["Price($)", "Bedrooms", "Bathrooms", "Size (sqft)", "Visit Counter"]

print(X_train_norm_df.describe())

#box_plot = X_train_norm_df.boxplot(column=["Price($)", "Bedrooms", "Bathrooms", "Size (sqft)", "Visit Counter"])
#plt.show()

# Standardization process
X_train_std = X_train.copy()
X_test_std = X_test.copy()

# Fit the standardization scaler onto the training data
stan = StandardScaler().fit(X_train_std)
# Transform the training data
X_train_stan = stan.transform(X_train_std)

# Use the same scaler to transform the testing set
X_test_stan = stan.transform(X_test_std)

# Convert the transformed data into pandas dataframe
X_train_std_df = pd.DataFrame(X_train_stan)
X_train_std_df.columns = ["Price($)", "Bedrooms", "Bathrooms", "Size (sqft)", "Visit Counter"]

print(X_train_std_df.describe())
print(X_train_std_df)

box_plot_std = X_train_std_df.boxplot(column=["Price($)", "Bedrooms", "Bathrooms", "Size (sqft)", "Visit Counter"])
#plt.show()




# Convert categorical values to numeric using One Hot Encoder
categorical_columns = real_estate_raw_data[["Building Type", "Utilities"]].copy()
print("categorical columns")
print(categorical_columns)

category_df = pd.DataFrame(categorical_columns)
print("category desc")
print(category_df.describe())
selected_column_train, selected_column_test = train_test_split(category_df, test_size=0.2)

selected_column_train_copy = selected_column_train.copy()
selected_column_test_copy = selected_column_test.copy()


selected_columns = selected_column_train_copy.select_dtypes(include=['object']).columns.to_list()
print("Selected Columns:")
print(selected_columns)

encoder = OneHotEncoder(sparse_output=False)

one_hot_encoded_train = encoder.fit_transform(selected_column_train_copy)

one_hot_encode_df = pd.DataFrame(one_hot_encoded_train, columns=encoder.get_feature_names_out(selected_columns))


# Join all dataframes
df_list = [X_train_norm_df, one_hot_encode_df]
combined_df = pd.concat(df_list,axis=1)
print(combined_df.info())
combined_df.to_excel("combined.xlsx")



