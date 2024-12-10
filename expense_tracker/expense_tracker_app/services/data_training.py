import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from nltk import SyllableTokenizer
from sklearn import preprocessing
from sklearn.metrics.pairwise import cosine_similarity
# To be used for splitting the dataset into training and test sets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.preprocessing import OneHotEncoder

from gensim.models import Word2Vec
import gensim
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk

import geocoder
from geopy.geocoders import Nominatim

# count vector
from sklearn.feature_extraction.text import CountVectorizer

from numpy.linalg import norm

nltk.download('punkt_tab')

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

# box_plot = X_train_norm_df.boxplot(column=["Price($)", "Bedrooms", "Bathrooms", "Size (sqft)", "Visit Counter"])
# plt.show()

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
# plt.show()


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

# Convert Address column into vector using Word2Vec
address_column = real_estate_raw_data[["Address"]].copy()

address_df = pd.DataFrame(address_column)
print("Address desc")
address_df.replace(',', '', regex=True)
print(address_df.info())

address_column_train, address_column_test = train_test_split(address_df, test_size=0.2)
address_column_train_copy = address_column_train.copy()
address_column_test_copy = address_column_test.copy()

print("address train data")
print(address_column_train_copy)

selected_address_column = address_column_train_copy.select_dtypes(include=['object']).columns.to_list()
print("selected address column")
print(selected_address_column)

address_list = []
for val in address_column_train_copy.values.tolist():
    if type(val) is list:
        for element in val:
            address_list.append(element)
    else:
        address_list.append(val)

for i in address_list:
    if i == ',':
        i = ''

# print(address_list)

data = []

for i in address_list:
    sent_tokenize(i)
    temp = []

    for j in word_tokenize(i):
        if j == ",":
            j = ""
        temp.append(j.lower())

    data.append(temp)

print("Data: ")
print(data)

vector_df = pd.DataFrame(address_column_train_copy, columns=["Address"])
print("vector df")
print(vector_df)

# Join all dataframes
df_list = [X_train_norm_df, one_hot_encode_df, vector_df]
combined_df = pd.concat(df_list, axis=1)
print(combined_df.info())
combined_df.to_excel("combined.xlsx")

# get current location
g = geocoder.ip('me')
current_city = g.city
coordinates = g.latlng
print(coordinates)
geolocator = Nominatim(user_agent="expense_tracker_app")
lat = str(coordinates[0])
lng = str(coordinates[1])
location = geolocator.reverse(lat + "," + lng)
location = str(location)
print(location)

print(current_city)

# convert city to vector for cosine similarity with item matrix
input_vector_lst = [location]
print(input_vector_lst)
tokenize_current_address = []

for i in input_vector_lst:
    sent_tokenize(i)
    temp = []

    for j in word_tokenize(i):
        if j == ",":
            j = ""
        temp.append(j.lower())

    tokenize_current_address.append(temp)

print(tokenize_current_address)
print(tokenize_current_address[0])


#############################################################


def convert_text2vector(text_lst):
    print("text list:", text_lst)
    vectorizer = CountVectorizer(stop_words="english")
    vectorizer.fit(text_list)
    print("vocab:", vectorizer.vocabulary_)
    vector = vectorizer.transform(text_list)
    vector = vector.toarray()
    # print("vector: ", vector)
    return vector


def calculate_similarity(v1, v2):
    cosine = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    # print(cosine)
    return cosine


# text to vector using count vector method

input_address = "376 athol street east central oshawa durham region golden horseshoe ontario l1g 6c5 canada"
address_dataset = "101 cosburn street central avenue golden horseshoe toronto on m4k 2g3"

similarity_list = []

for item in address_list:
    text_list = [input_address, item]
    input_vector_list = convert_text2vector(text_list)
    print(input_vector_list[0], input_vector_list[1])
    cos_similarity = calculate_similarity(input_vector_list[0], input_vector_list[1])
    similarity_list.append(cos_similarity)

print(similarity_list)
print(len(similarity_list))



# convert list of cosine similarity into data frame and integrate with indices and url column

address_list_to_df = pd.DataFrame(similarity_list, columns=["Address_Cos_Similarity"])
print(address_list_to_df)

url_column = real_estate_raw_data["url"].loc[:1815].copy()


url_df = pd.DataFrame(url_column.values, columns=["url"])
print("url shape:", url_df.shape)

combined_similarity_url_list = [address_list_to_df, url_column]
combined_similarity_url_df = pd.concat(combined_similarity_url_list, axis=1)

print(combined_similarity_url_df.info())
combined_similarity_url_df.to_excel("similarity_url.xlsx")
