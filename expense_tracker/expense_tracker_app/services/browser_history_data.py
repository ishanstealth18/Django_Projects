import re
from browser_history import get_history
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

    for x in his:
        for y in x:
            url_visited_list.append(y)

    # print(url_visited_list)
    rental_link_list = []

    for x in url_visited_list:
        link_text = x[2]
        link_text = link_text.lower()
        # print(link_text)
        if "condos" in link_text or "houses" in link_text or "apartments" in link_text or "rent" in link_text or "sale" in link_text:
            if "google search" not in link_text:
                rental_link_list.append(x[1])

    print("Rental link history:", rental_link_list)
    return rental_link_list



def scrape_data(history_links):
    soup_data = None
    for links in history_links:
        request_response = requests.get(links)
        print("request response :", request_response)
        if request_response.status_code == 200:
            soup_data = BeautifulSoup(request_response.content, 'html.parser')
            # print(soup_data.prettify())
            #p_list.append(extract_price(soup_data))
            #title_list.append(clean_title_data(soup_data.find_all('title')))

            #bedroom_list.append(bedroom_info(soup_data))
        else:
            print("No response from url: ", links)


    #clean_list(p_list)
    print("****************************************************************************")
    #clean_list(bedroom_list)
    #print("Title list: ", title_list)
    #print(p_list)
    #print(bedroom_list)
    #return title_list, p_list, bedroom_list

    return soup_data


def extract_price(soup_obj):
    p_list = [extract_price_info(soup_obj)]
    #print(p_list)
    #clean_price_list.append(clean_list(p_list))
    return clean_list(p_list)


def extract_extra_data(soup_obj):
    extra_data_list = [extract_extra_data_info(soup_obj)]
    extra_data_list = clean_list(extra_data_list)
    bedroom_list = []
    for text_str in extra_data_list:
        for x in re.finditer("bedrooms", text_str):
            bedroom_list.append(text_str[x.start()-30:x.start()+30])

    for text_str in extra_data_list:
        for x in re.finditer("bathrooms", text_str):
            bedroom_list.append(text_str[x.start()-30:x.start()+30])

    for text_str in extra_data_list:
        for x in re.finditer("washrooms", text_str):
            bedroom_list.append(text_str[x.start()-30:x.start()+30])

    for text_str in extra_data_list:
        for x in re.finditer("apartment", text_str):
            bedroom_list.append(text_str[x.start()-30:x.start()+30])

    for text_str in extra_data_list:
        for x in re.finditer("house", text_str):
            bedroom_list.append(text_str[x.start()-30:x.start()+30])

    for text_str in extra_data_list:
        for x in re.finditer("condo", text_str):
            bedroom_list.append(text_str[x.start()-30:x.start()+30])

    for text_str in extra_data_list:
        for x in re.finditer("price", text_str):
            bedroom_list.append(text_str[x.start()-30:x.start()+30])

    for text_str in extra_data_list:
        for x in re.finditer("townhouse", text_str):
            bedroom_list.append(text_str[x.start()-30:x.start()+30])


    for text_str in extra_data_list:
        for x in re.finditer("basement", text_str):
            bedroom_list.append(text_str[x.start()-30:x.start()+30])

    return bedroom_list


def extract_title_data(soup_obj):
    title_list = [clean_title_data(soup_obj.find_all('title'))]
    #print("Title list:", title_list)
    return title_list


def clean_title_data(title_list_to_clean):
    cleaned_title_list = []
    if len(title_list_to_clean) > 0:
        for item in title_list_to_clean:
            #print(item)
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
    #print("price data: ", price_data)
    return price_data


def extract_extra_data_info(html_content):
    bedroom_data = html_content(text=lambda t: " bedroom" or " bathroom" in t.text)
    #print(bedroom_lst)
    return bedroom_data


def clean_list(list_to_clean):
    updated_list = []
    #print("original list: ", list_to_clean)
    for item in list_to_clean:
        for x in item:
            x = str(x)
            x = x.lower()
            x = re.sub('\W+', ' ', x)
            x = re.sub('[^a-zA-Z0-9 \n\.]', '', x)
            x = x.strip()
            updated_list.append(x)

    updated_list = list(filter(None, updated_list))
    #print("Updated list:", updated_list)
    return updated_list


#history_links_list = get_browser_history_links()
#scrape_data(history_links_list)
