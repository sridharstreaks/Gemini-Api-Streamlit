#from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import re
from duckduckgo_search import DDGS

#load_dotenv()  # Loading all the environment variables from .env file
# Configure Streamlit page settings

def internet(query:str):
    """Fetches search results for real-time information from internet based on keywords as input
    Args:
        query: user prompt broken down as keywords rather than the entire query
    return:
        response (list): list of dictionaries containing title,link to the search results page (herf),body 
    """
    req=DDGS()
    response=req.text(query,max_results=10)
    return response

def all_in_one(new_prompt:str)-> str:
    """Fecthes a product title from an ecommerce store based on user query.
    Args:
        new_prompt: user prompt
    return:
        results (list): list of dictionaries containing ASIN, Title, Stars, Reviews, Current_Price, MRP, Deal, Image link, Link to product page or a string if no products is found
    """
    #Makes the query into search keywords
    query=new_prompt.replace(" ", "+")
    
    # Makes connection to amazon shopping site
    custom_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Accept-Language': 'da, en-gb, en',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Referer': 'https://www.google.com/'
    }
    url = f'https://www.amazon.in/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords={query}'

    response = requests.get(url, headers= custom_headers)
    #print(response.status_code)
    
    #collects the product info
    soup = BeautifulSoup(response.text, 'html.parser')

    products = []
    results=""
    # Define the pattern to match class names containing 's-result-item' and 's-asin' but not 'AdHolder'
    pattern_sr = re.compile(r's-result-item.*s-asin(?!.*AdHolder)')

    # Find all div elements with class attributes that match the pattern
    items = soup.find_all('div', class_=pattern_sr)
    count = 0

    for item in items:
        if count >= 3:
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
    
tool=[all_in_one,internet]

st.set_page_config(
    page_title="Streaks Ai - Your New Shopping Assistant",
    page_icon=":sparkles:",  # Favicon emoji
    layout="centered",  # Page layout option
)

#api_key = os.getenv("GOOGLE_API_KEY")  # Accessing the environment variables
api_key=st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=api_key)  # Loading the API key into the generativeai module

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash",tools=tool,system_instruction="You are a helpful shopping assistant named Streaks. You would receive user queries for which you need to use the provided function which gives a list of dictionaries containing ASIN which is the unique product ID (don't show ASIN to the user), Title, Stars, Reviews, Current_Price, MRP, Deal, Image, Link. You need to use this info to provide a natural response. You might also receive some follow up questions based on the result or some general query out of the shopping context which may require internet search results for which you have another function called \'internet\'.So, you don't need to use the function for every query. Based on your judgment use the functions whenever needed.")

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
