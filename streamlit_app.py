import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import re
from duckduckgo_search import DDGS

def internet(query:str):
    """ Fetches search results for any real-time or present information from the internet based on keywords as input
    Args:
        query: user prompt broken down as keywords rather than the entire query
    return:
        response (list): list of dictionaries containing title, link to the search results page (herf), body 
    """
    req=DDGS()
    response=req.text(query,max_results=5)
    if response !=[]:
        return response
    else:
        return ["Connection not successful"]

def amazon_issues(query:str):
    """ Fetches search results for any help, queries, or issues related to the Amazon e-commerce store.
    Args:
        query: user prompt broken down as keywords rather than the entire query
    return:
        response (list): list of dictionaries containing title, link to the search results page (herf), body 
    """
    keyword=query+" site:amazon.in"
    req=DDGS()
    response=req.text(keyword,max_results=5,region='en-in')
    if response !=[]:
        return response
    else:
        return ["Connection not successful"]

def search_keyword(new_prompt:str)-> list:
    """ Fetches a product title from an e-commerce store based on the user query.
    Args:
        new_prompt: user prompt
    return:
        products (list): list of dictionaries containing product Index, ASIN, Title, Stars, Reviews, Current_Price, MRP, Deal, Image link, Link to the product page, or a list of string if the connection fails
    """
    #Makes the query into search keywords
    query=new_prompt.replace(" ", "+")
    
    # Makes connection to Amazon shopping site
    custom_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Accept-Language': 'da, en-gb, en',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Referer': 'https://www.google.com/'
    }
    url = f'https://www.amazon.in/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords={query}'

    response = requests.get(url, headers= custom_headers)

    if response.status_code==200:
    
        #collects the product info
        soup = BeautifulSoup(response.text, 'html.parser')
    
        products = []
        results=""
        # Define the pattern to match class names containing 's-result-item' and 's-asin' but not 'AdHolder'
        pattern_sr = re.compile(r's-result-item.*s-asin(?!.*AdHolder)')
    
        # Find all div elements with class attributes that match the pattern
        items = soup.find_all('div', class_=pattern_sr)
        count = 0

        if items is not None:
    
            for item in items:
                if count >= 5:
                    break
                
                # Skip sponsored products
                #if item.find('span', text='Sponsored'):
                #    continue
        
                product = {}
                
                if item['data-asin']==None and count==0:
                    return "No Products Found"
                elif item['data-asin']==None and count>0:
                    return products
                else:
                    # Extracting ASIN
                    asin = item['data-asin']
                    if not asin:
                        continue
        
                    # Extracting Title
                    title_elem = item.find('div', attrs={"data-cy": "title-recipe"}).find('span')
                    title = title_elem.get_text(strip=True) if title_elem else 'No Title'
        
                    # Extracting Stars Information
                    star_elem = item.find('span', class_='a-icon-alt')
                    stars = star_elem.get_text(strip=True) if star_elem else 'No Rating'
        
                    # Extracting Number of Reviews
                    reviews_elem = item.find('div', attrs={"data-cy": "reviews-block"}).find('span', class_='a-size-base s-underline-text')
                    reviews = reviews_elem.get_text(strip=True).replace(',', '') if reviews_elem else '0'
        
                    # Extracting Current Price
                    price_whole_span = item.find('span', class_='a-price-whole')
                    current_price = price_whole_span.text.strip() if price_whole_span else 'Price not found'
        
                    # Extracting MRP
                    mrp_span = item.find('span', class_='a-price a-text-price')
                    mrp = mrp_span.find('span', class_='a-offscreen').text.strip() if mrp_span else 'MRP not found'
                    mrp_value = ''.join(filter(str.isdigit, mrp))  # Extract digits from MRP
                    mrp_value = int(mrp_value) if mrp_value else 'MRP value not found'
        
                    # Check for Limited Time Deal
                    deal_badge = item.find('div', attrs={"data-cy": "price-recipe"}).find('span', class_='a-badge-text')
                    deal_status = 'On Deal' if deal_badge and 'Limited time deal' in deal_badge.text else 'Not on Deal'
        
                    # Extracting Image URL
                    image_elem = item.find('img')
                    image = image_elem['src'] if image_elem else 'No Image Found'
        
                    # Product Link
                    link = 'https://www.amazon.in/dp/' + asin
        
                    product['Index']= count
                    product['ASIN'] = asin
                    product['Title'] = title
                    product['Stars'] = stars
                    product['Reviews'] = reviews
                    product['Current_Price'] = current_price
                    product['MRP'] = mrp_value
                    product['Deal'] = deal_status
                    product['Image'] = image
                    product['Link'] = link
        
                    products.append(product)
                count += 1
            return products
        else:
            []
    else:
        ["Connection not successful"]
    
def customers_say(soup):
    return soup.find('div',id="product-summary").find('span').get_text(strip=True)

def product_insights(soup):
    elements = soup.find_all('a', id=lambda x: x and "aspect-button" in x)

    # Define a string to store results
    product_insights_string=''

    # Define regex patterns for conditions
    patterns = {
        "POSITIVE": re.compile("^POSITIVE"),
        "MIXED": re.compile("^MIXED"),
        "NEGATIVE": re.compile("^NEGATIVE"),
    }

    # Iterate through each element
    for element in elements:
        aria_value = element.get("aria-describedby")
        if patterns["POSITIVE"].match(aria_value):
            product_insights_string=product_insights_string+"POSITIVE:"+element.get_text()+', '
            #results.append({"condition": "POSITIVE", "text": element.get_text()})
        elif patterns["MIXED"].match(aria_value):
            product_insights_string=product_insights_string+"MIXED:"+element.get_text()+', '
        elif patterns["NEGATIVE"].match(aria_value):
            product_insights_string=product_insights_string+"NEGATIVE:"+element.get_text()+', '

    # Remove trailing comma if there are insights
    if product_insights_string:
        product_insights_string=product_insights_string.rstrip(', ')
    
    return product_insights_string

def product_factoid(link:str)-> list:
    """ Fetches more information about a particular product from an e-commerce store based on the user query.
    Args:
        link: product link
    return:
        product_factoid_list (list): string containing more information such as about the item, customer review summary, product insights, or a list of string if the connection fails
    """
    
    custom_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Accept-Language': 'da, en-gb, en',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Referer': 'https://www.google.com/'
    }
    
    response = requests.get(link, headers= custom_headers)
    
    if response.status_code==200:
        #collects the product info
        soup = BeautifulSoup(response.text, 'html.parser')
        
        #resulting list
        product_factoid_list=[]
        
        # Find all tags with a class containing "my-class"
        if soup.find(string=' About this item ') is not None:
            tags = soup.find(string=' About this item ').find_all_next('ul',attrs={"class":re.compile("^a-unordered-list a-vertical a-spacing")})
        elif soup.find('ul',attrs={"class":re.compile("^a-unordered-list a-vertical a-spacing")}) is not None:
            tags = soup.find('ul',attrs={"class":re.compile("^a-unordered-list a-vertical a-spacing")})
        else:
            return product_factoid_list
        for tag in tags:
            product_factoid_list.append(tag.get_text(strip=True))
        
        #calling customers_say function
        product_factoid_list.append(customers_say(soup))
        
        #calling product_insights function
        product_factoid_list.append(product_insights(soup))
        
        return product_factoid_list
    else:
        return ["Connection not successful"]
    
tool=[search_keyword,internet,amazon_issues,product_factoid]

st.set_page_config(
    page_title="Streaks Ai - Your New Shopping Assistant",
    page_icon=":sparkles:",  # Favicon emoji
    layout="centered",  # Page layout option
)

api_key=st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=api_key)  # Loading the API key into the generativeai module

# Initialize the model
# Template text IGNORE: "ASIN which is the unique product ID (don't show ASIN to the user), Title, Stars, Reviews, Current_Price, MRP, Deal, Image, Link." " or some general query out of the shopping context which may require internet search results for which you have another function called \'internet\'.So, you don't need to use the function for every query."
model = genai.GenerativeModel("gemini-1.5-flash",tools=tool,system_instruction="You are a helpful shopping assistant named Streaks. You would receive user queries related to Amazon product search, help or issues associated with Amazon customer service, and general queries (internet search) for which you need to use the provided functions which give a list of dictionaries containing relevant details. You need to use this info to give a natural response. You might also receive some follow-up questions based on the result. Based on your judgment use the functions whenever needed.")

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[],enable_automatic_function_calling=True)


# Display the chatbot's title on the page
st.title("✨ Streaks Ai - Your New Shopping Assistant", help = "This Shopping assistant is designed by Sridhar Streaks powered by Google Gemini")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Anything...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
