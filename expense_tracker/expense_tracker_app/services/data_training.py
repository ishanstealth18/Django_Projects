import pandas as pd
import numpy as np
from expense_tracker_app.services import browser_history_data
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.preprocessing import OneHotEncoder
import nltk
import geocoder
from geopy.geocoders import Nominatim
from sklearn.feature_extraction.text import CountVectorizer

# Read raw data file
real_estate_raw_data = pd.read_excel("D:/Python_Projects/Django_Projects/expense_tracker/updated_data.xlsx")
nltk.download('punkt_tab')


# Get user browse history for better recommendation
def get_browser_data():
    title_data = []
    price_data = []
    mix_data = []
    user_browse_links = [browser_history_data.get_browser_history_links()]
    #print(" User history links :", user_browse_links)
    for link in user_browse_links:
        browser_history_data.scrape_data(link)



# Function to prepare data set. Includes splitting of data into Train and Test set, Standardization and One Hot Encoding
def prepare_dataset():
    pd.set_option('display.max_columns', None)
    # Creating a dataframe which has columns with numeric values and are required. Normalization and standardization can
    # be done on only numeric values
    real_estate_df_copy = real_estate_raw_data[
        ["Price($)", "Bedrooms", "Bathrooms", "Size (sqft)", "Visit Counter"]].copy()

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
    X_train_norm_df.columns = ["Price($)", "Bedrooms", "Bathrooms", "Size (sqft)", "Visit Counter"]

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
    X_train_std_df.columns = ["Price($)", "Bedrooms", "Bathrooms", "Size (sqft)", "Visit Counter"]

    # print(X_train_std_df.describe())
    # print(X_train_std_df)

    # Convert categorical values to numeric using One Hot Encoder
    categorical_columns = real_estate_raw_data[["Building Type", "Utilities"]].copy()
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


# Convert raw address data to vector
def convert_address_to_vector():
    address_column = real_estate_raw_data[["Address"]].copy()
    address_df = pd.DataFrame(address_column)
    # print("Address desc")
    address_df.replace(',', '', regex=True)
    # print(address_df.info())

    address_column_train, address_column_test = train_test_split(address_df, test_size=0.2)
    address_column_train_copy = address_column_train.copy()
    address_column_test_copy = address_column_test.copy()

    # print("address train data")
    # print(address_column_train_copy)
    # Creating another list with all the address in clean format
    address_list = []
    for val in address_column_train_copy.values.tolist():
        if type(val) is list:
            for element in val:
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


# Function to calculate cosine similarity
def calculate_similarity(v1, v2):
    cosine = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    # print(cosine)
    return cosine


# Combined function to convert text to vector and find cosine similarity
def find_cos_similarity():
    input_address = clean_raw_location_data()

    similarity_list = []
    address_data = convert_address_to_vector()

    # print("Address Data: ", address_data)
    for item in address_data:
        item = item.replace(',', '')
        text_list = [input_address, item]
        input_vector_list = convert_text2vector(text_list)
        # print(input_vector_list)
        # print(input_vector_list[0], input_vector_list[1])
        cos_similarity = calculate_similarity(input_vector_list[0], input_vector_list[1])
        similarity_list.append(cos_similarity)

    # print(similarity_list)
    return similarity_list


# Function to store top recommended values
def call_top_values():
    cos_similar_values_list = find_cos_similarity()
    address_list_to_df = pd.DataFrame(cos_similar_values_list, columns=["Address_Cos_Similarity"])
    # print(address_list_to_df)

    address_list_to_df = address_list_to_df.loc[~(address_list_to_df["Address_Cos_Similarity"] == 0)]
    # print(address_list_to_df)

    address_list_to_df = address_list_to_df.sort_values(by="Address_Cos_Similarity", ascending=False)
    top_5_values = address_list_to_df.head(5).index.to_list()
    print(top_5_values)

    top_url_lst = []
    for x in top_5_values:
        top_url_lst.append(real_estate_raw_data.loc[x, "url"])

    print(top_url_lst)
    address_list_to_df.to_excel("similarity_url.xlsx")

    return top_url_lst






# Execute the functions
#prepare_dataset()
#convert_address_to_vector()
#get_current_location()
#convert_address_to_vector()
#find_cos_similarity()
#call_top_values()
get_browser_data()

