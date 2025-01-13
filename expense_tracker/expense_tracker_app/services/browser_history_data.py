import re
from browser_history.browsers import Chrome
import requests
from bs4 import BeautifulSoup


# Get browser history of the system
def get_browser_history_links():
    browser = Chrome()
    output = browser.fetch_history()
    his = output.histories
    his = [his]

    url_visited_list = []

    # create list of all visited links
    for x in his:
        for y in x:
            url_visited_list.append(y)

    if len(url_visited_list) > 0:
        rental_link_list = []
        for x in url_visited_list:
            # get url from whole text
            link_text = x[2]
            link_text = link_text.lower()

            # condition to check if below keywords are in url, if yes, then add it to the list else ignore.
            if "condos" in link_text or "houses" in link_text or "apartments" in link_text or "rent" in link_text or "sale" in link_text:
                if "google search" not in link_text:
                    rental_link_list.append(x[1])

        return rental_link_list
    else:
        return None


# function to scrape data from th user browse links
def scrape_data(history_links):
    soup_data = None
    # get request response for user links
    for links in history_links:
        request_response = requests.get(links)
        # if request response is successful, get HTML data of that webpage user visited
        if request_response.status_code == 200:
            soup_data = BeautifulSoup(request_response.content, 'html.parser')

        else:
            print("No response from url: ", links)

    return soup_data


def extract_price(soup_obj):
    p_list = [extract_price_info(soup_obj)]
    return clean_list(p_list)


# function to extract all data from HTML content got from url visited by user
def extract_extra_data(soup_obj):
    extra_data_list = [extract_extra_data_info(soup_obj)]
    extra_data_list = clean_list(extra_data_list)
    bedroom_list = []
    # iterate through data list and get text with 25 characters before and after keyword 'bedrooms'
    for text_str in extra_data_list:
        for x in re.finditer("bedrooms", text_str):
            bedroom_list.append(text_str[x.start()-25:x.start()+25])

    # iterate through data list and get text with 25 characters before and after keyword 'bathrooms'
    for text_str in extra_data_list:
        for x in re.finditer("bathrooms", text_str):
            bedroom_list.append(text_str[x.start()-25:x.start()+25])

    # iterate through data list and get text with 25 characters before and after keyword 'washrooms'
    for text_str in extra_data_list:
        for x in re.finditer("washrooms", text_str):
            bedroom_list.append(text_str[x.start()-25:x.start()+25])

    # iterate through data list and get text with 25 characters before and after keyword 'apartment'
    for text_str in extra_data_list:
        for x in re.finditer("apartment", text_str):
            bedroom_list.append(text_str[x.start()-25:x.start()+25])

    # iterate through data list and get text with 25 characters before and after keyword 'house'
    for text_str in extra_data_list:
        for x in re.finditer("house", text_str):
            bedroom_list.append(text_str[x.start()-25:x.start()+25])

    # iterate through data list and get text with 25 characters before and after keyword 'condo'
    for text_str in extra_data_list:
        for x in re.finditer("condo", text_str):
            bedroom_list.append(text_str[x.start()-25:x.start()+25])

    # iterate through data list and get text with 25 characters before and after keyword 'price'
    for text_str in extra_data_list:
        for x in re.finditer("price", text_str):
            bedroom_list.append(text_str[x.start()-25:x.start()+25])

    # iterate through data list and get text with 25 characters before and after keyword 'townhouse'
    for text_str in extra_data_list:
        for x in re.finditer("townhouse", text_str):
            bedroom_list.append(text_str[x.start()-25:x.start()+25])

    # iterate through data list and get text with 25 characters before and after keyword 'basement'
    for text_str in extra_data_list:
        for x in re.finditer("basement", text_str):
            bedroom_list.append(text_str[x.start()-25:x.start()+25])

    return bedroom_list


def extract_title_data(soup_obj):
    title_list = [clean_title_data(soup_obj.find_all('title'))]
    return title_list


def clean_title_data(title_list_to_clean):
    cleaned_title_list = []
    if len(title_list_to_clean) > 0:
        for item in title_list_to_clean:
            item = str(item)
            item = item.lower()
            item = item.replace('<title>', '')
            item = item.replace('</title>', '')
            item = re.sub('[^a-zA-Z0-9 \n\.]', '', item)
            item = item.strip()
            cleaned_title_list.append(item)

        # remove null values from the list
        cleaned_title_list = list(filter(None, cleaned_title_list))

    if len(cleaned_title_list) > 0:
        return cleaned_title_list[0]


def extract_price_info(html_content):
    price_data = html_content(text=lambda t: "$ " in t.text)
    return price_data


# function to extract data where keywords 'bedroom' and 'bathroom' is present in text
def extract_extra_data_info(html_content):
    bedroom_data = html_content(text=lambda t: " bedroom" or " bathroom" in t.text)
    return bedroom_data


# function to clean data extracted from HTML
def clean_list(list_to_clean):
    updated_list = []
    for item in list_to_clean:
        for x in item:
            x = str(x)
            x = x.lower()
            x = re.sub('\W+', ' ', x)
            x = re.sub('[^a-zA-Z0-9 \n\.]', '', x)
            x = x.strip()
            updated_list.append(x)

    updated_list = list(filter(None, updated_list))
    return updated_list

