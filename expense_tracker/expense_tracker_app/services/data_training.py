import operator
import re
import sys

import pandas as pd
import numpy as np
from numpy.linalg import norm

from expense_tracker_app.services import browser_history_data
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.preprocessing import OneHotEncoder
import nltk
import geocoder
from geopy.geocoders import Nominatim
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import logging

# Read raw data file
real_estate_raw_data = pd.read_excel("D:/Python_Projects/Django_Projects/expense_tracker/updated_data.xlsx")
nltk.download('punkt_tab')
np.set_printoptions(threshold=sys.maxsize)
logging.basicConfig(filename="logs.txt", filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# Get user browse history for better recommendation
def get_browser_data():
    title_data = []
    price_data = []
    mix_data = []
    user_browse_links = [browser_history_data.get_browser_history_links()]
    # print(" User history links :", user_browse_links)
    for link in user_browse_links:
        soup_obj = browser_history_data.scrape_data(link)
        # print("soup obj:", soup_obj)
        mix_data.append(browser_history_data.extract_extra_data(soup_obj))

    print("Mix data:", mix_data)
    return convert_user_history_data_to_vector(mix_data)


# Function to prepare data set. Includes splitting of data into Train and Test set, Standardization and One Hot Encoding
def prepare_dataset():
    pd.set_option('display.max_columns', None)
    # Creating a dataframe which has columns with numeric values and are required. Normalization and standardization can
    # be done on only numeric values
    # real_estate_df_copy = real_estate_raw_data[["Price($)", "Bedrooms", "Bathrooms", "Size (sqft)", "Visit Counter"]].copy()
    real_estate_df_copy = real_estate_raw_data[
        ["Bedrooms", "Bathrooms"]].copy()
    print(real_estate_df_copy.describe())
    # Divide the data into features (X) and target (Y)
    # Data is converted to a panda’s dataframe
    X = pd.DataFrame(real_estate_df_copy.values)

    print(X.head())
    # Split dataset into train and test set
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
    # X_train_norm_df.columns = ["Price($)", "Bedrooms", "Bathrooms", "Size (sqft)", "Visit Counter"]
    X_train_norm_df.columns = ["Bedrooms", "Bathrooms"]
    # print(X_train_norm_df.describe())

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
    # X_train_std_df.columns = ["Price($)", "Bedrooms", "Bathrooms", "Size (sqft)", "Visit Counter"]
    X_train_std_df.columns = ["Bedrooms", "Bathrooms"]

    X_train_std_df_list = X_train_std_df.values.tolist()
    # print(X_train_std_df.describe())
    print("X_train_std_df_list", X_train_std_df_list)

    # Convert categorical values to numeric using One Hot Encoder
    # categorical_columns = real_estate_raw_data[["Building Type", "Utilities"]].copy()
    categorical_columns = real_estate_raw_data[["Building Type"]].copy()
    # print("categorical columns")
    # print(categorical_columns)

    category_df = pd.DataFrame(categorical_columns)
    # print("category desc")
    # print(category_df.describe())
    selected_column_train, selected_column_test = train_test_split(category_df, test_size=0.2)

    selected_column_train_copy = selected_column_train.copy()
    selected_column_test_copy = selected_column_test.copy()

    selected_columns = selected_column_train_copy.select_dtypes(include=['object']).columns.to_list()

    encoder = OneHotEncoder(sparse_output=False)

    one_hot_encoded_train = encoder.fit_transform(selected_column_train_copy)

    one_hot_encode_df = pd.DataFrame(one_hot_encoded_train, columns=encoder.get_feature_names_out(selected_columns))
    building_type_list = one_hot_encode_df.values.tolist()
    print("building type list:", building_type_list)


# Convert raw address data to vector
def filter_address_data():
    address_column = real_estate_raw_data[["Address"]].copy()
    address_df = pd.DataFrame(address_column)
    address_df.replace(',', '', regex=True)
    # print(address_df.info())

    address_column_train, address_column_test = train_test_split(address_df, test_size=0.2)
    address_column_train_copy = address_column_train.copy()
    # address_column_test_copy = address_column_test.copy()

    # Creating another list with all the address in clean format
    address_list = []
    for val in address_column_train_copy.values.tolist():
        if type(val) is list:
            for element in val:
                element = element.replace(',', '')
                address_list.append(element.lower())
        else:
            address_list.append(val)

    return address_list


# def join_df():
# Join all dataframes
# df_list = [X_train_norm_df, one_hot_encode_df, vector_df]
# combined_df = pd.concat(df_list, axis=1)
# print(combined_df.info())
# combined_df.to_excel("combined.xlsx")


# Function to get current location which will be used for recommendation in case there is no user data history
def get_current_location():
    # get current location
    g = geocoder.ip('me')
    coordinates = g.latlng
    geolocator = Nominatim(user_agent="expense_tracker_app")
    lat = str(coordinates[0])
    lng = str(coordinates[1])
    location = geolocator.reverse(lat + "," + lng)
    location = str(location)
    # print(location)
    return location


# convert raw location address to vector for cosine similarity with item matrix
def clean_raw_location_data():
    location = get_current_location()
    location = location.lower()
    location = location.replace(',', '')
    return location


# Function to convert text list to vector using count vector
def convert_text2vector(text_lst):
    # print("text list:", text_lst)
    vectorizer = CountVectorizer(stop_words="english")
    vectorizer.fit(text_lst)
    vector = vectorizer.transform(text_lst)
    vector = vector.toarray()
    # print("vector: ", vector)
    return vector


def prepare_title_data():
    title_dataset = real_estate_raw_data[
        ["Title"]].copy()
    # print(title_dataset.describe())
    # Divide the data into features (X) and target (Y)
    # Data is converted to a panda’s dataframe
    X = pd.DataFrame(title_dataset.values)

    # Split dataset into train and test set
    X_title_train, X_title_test = train_test_split(X, test_size=0.2)
    # Good practice to keep original dataframes untouched for re-usability
    X_title_data_train_copy = X_title_train.copy()

    title_dataset_list = X_title_data_train_copy.values
    clean_title_data_lst = []
    for item in title_dataset_list:
        for x in item:
            x = re.sub('[^a-zA-Z0-9 \n\.]', '', x)
            x = x.replace('.', '')
            x = x.strip()
            x = x.lower()
            # print("After clean:", x)
            clean_title_data_lst.append(x)

    # print("Clean title data:", clean_title_data_lst)
    return convert_title_to_vector(clean_title_data_lst)


def convert_title_to_vector(input_title_lst):
    # print("input title list:", len(input_title_lst))
    tfidf_result = None
    tfidf = TfidfVectorizer()
    tfidf_result = tfidf.fit_transform(input_title_lst)
    tfidf_result = tfidf_result.toarray()

    return tfidf_result


# Function to convert user history data text into vector using TF-IDF method.
def convert_user_history_data_to_vector(user_history_data_list):
    # logger.debug(user_history_data_list)
    tfidf = TfidfVectorizer()
    tfidf_result = tfidf.fit_transform(user_history_data_list[0])
    tfidf_result = tfidf_result.toarray()

    return tfidf_result


# Function to calculate cosine similarity
def calculate_similarity(v1, v2):
    cosine = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    #print("Cosine simliarity value:", cosine)
    return cosine


# Combined function to convert text to vector and find cosine similarity
def find_address_cos_similarity():
    input_address = clean_raw_location_data()
    similarity_list = []
    address_data = filter_address_data()

    # print("Address Data: ", address_data)
    for item in address_data:
        item = item.replace(',', '')
        text_list = [input_address, item]
        input_vector_list = convert_text2vector(text_list)
        # print(input_vector_list)
        #print(input_vector_list[0], input_vector_list[1])
        cos_similarity = calculate_similarity(input_vector_list[0], input_vector_list[1])
        similarity_list.append(cos_similarity)

    call_top_values(similarity_list)

    # print(similarity_list)
    return similarity_list


# This function will calculate cosine similarity between user history data and existing real estate dataset 'Title' columns
def user_history_title_cosine_similarity():
    user_history_data = get_browser_data()
    # print("User history data:", user_history_data)
    # logger.debug(user_history_data)
    print("user history shape:", user_history_data.shape)

    title_list = prepare_title_data()
    print("title shape:", title_list.shape)
    #print("Title list:", title_list)
    # logger.debug(title_list)
    address_data = filter_address_data()

    cos_similarity_lst = []
    cos_similarity_title_index_val = {}

    for x in user_history_data:
        temp = 0
        for y in range(len(title_list) - 1):
            # print(x)
            # print(title_list[y])
            user_history_appended_arr, title_appended_arr = reshape_arrays(x, title_list[y])
            cos_similarity = calculate_similarity(user_history_appended_arr, title_appended_arr)
            address_vector = convert_text2vector([address_data[y]])
            user_history_appended_arr, address_appended_arr = reshape_arrays(x, address_vector[0])
            address_mix_data_cos_similarity = calculate_similarity(user_history_appended_arr, address_appended_arr)
            total_cos_similarity = cos_similarity + address_mix_data_cos_similarity
            if total_cos_similarity > temp:
                temp = cos_similarity
                cos_similarity_title_index_val = {"cos_value": temp, "index": y+1}

        cos_similarity_lst.append(cos_similarity_title_index_val)
        print("Total cos value length: ", len(cos_similarity_lst))

    # print("cos similarity:", cos_similarity_lst)

    for x in cos_similarity_lst:
        if len(x) == 0:
            cos_similarity_lst.remove(x)
    cos_similarity_lst = sorted(cos_similarity_lst, key=lambda i: i["cos_value"], reverse=True)
    #print(cos_similarity_lst)
    print(cos_similarity_lst[:10])
    top_cos_values = cos_similarity_lst[:10]
    for x in top_cos_values:
        print(real_estate_raw_data.loc[x["index"]-2, "url"])

    # logger.debug(cos_similarity_lst)
    # logger.debug(call_top_values(cos_similarity_lst))
    #print(call_top_values(cos_similarity_lst))
    # logger.debug(cos_similarity_lst)


# This function is to reshape arrays in case if the dimensions are not equal for cos similarity function
def reshape_arrays(arr1, arr2):
    appended_arr1 = arr1
    appended_arr2 = arr2
    arr1_shape = appended_arr1.shape
    arr2_shape = appended_arr2.shape
    # print("arr1 shape : ", arr1_shape)
    # print("arr2 shape : ", arr2_shape)

    if appended_arr1.shape > appended_arr2.shape:
        shape_difference = arr1_shape[0] - arr2_shape[0]
        # print("Shape difference:", shape_difference)
        for x in range(shape_difference):
            appended_arr2 = np.append(appended_arr2, [0])

        # print("arr1 shape after append:", appended_arr1.shape)

    elif appended_arr1.shape < appended_arr2.shape:
        shape_difference = arr2_shape[0] - arr1_shape[0]
        # print("Shape difference:", shape_difference)
        for x in range(shape_difference):
            appended_arr1 = np.append(appended_arr1, [0])

        # print("arr2 shape after append:", appended_arr2.shape)

    return appended_arr1, appended_arr2


# Function to store top recommended values
def call_top_values(cos_similarity_values_lst):
    # cos_similar_values_list = find_address_cos_similarity()
    address_list_to_df = pd.DataFrame(cos_similarity_values_lst, columns=["Address_Cos_Similarity"])
    print(address_list_to_df.index)

    #address_list_to_df = address_list_to_df.loc[~(address_list_to_df["Address_Cos_Similarity"] == 0)]
    # print(address_list_to_df)


    top_5_values = None
    address_list_to_df = address_list_to_df.sort_values(by="Address_Cos_Similarity", ascending=False)
    print(address_list_to_df.head(5))

    if len(address_list_to_df) >= 5:
        top_5_values = address_list_to_df.head(5).index.to_list()
        print(top_5_values)

    top_url_lst = []
    for x in top_5_values:
        top_url_lst.append(real_estate_raw_data.loc[x-2, "url"])

    print(top_url_lst)


    return top_url_lst


def experiment():
    lst = [{'cos_value': 0.9357720613681751, 'index': 961}, {'cos_value': 0.9103754199297753, 'index': 1206},
           {'cos_value': 0.9103754199297753, 'index': 1206}, {'cos_value': 0.9103754199297753, 'index': 1206},
           {'cos_value': 0.9103754199297753, 'index': 1206}]

    address_data = filter_address_data()
    #print(address_data)

    cos_values = [672, 1451, 46, 1159, 127]
    for x in cos_values:
        print(x)
        print(real_estate_raw_data.loc[x-2, "url"])

    for y in range(len(address_data) - 1):
        address_vector = convert_text2vector([address_data[y]])
        #print(address_vector[0])


    #for i in lst:
    #    if len(i) == 0:
    #        lst.remove(i)


# Execute the functions
# prepare_dataset()
# convert_address_to_vector()
# get_current_location()
# convert_address_to_vector()
#find_address_cos_similarity()
#call_top_values()
# get_browser_data()
# prepare_title_data()
user_history_title_cosine_similarity()
#experiment()