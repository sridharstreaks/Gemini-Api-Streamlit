# Streaks AI - Conversational Shopping Assistant V2

Welcome to the Streaks AI repository! Streaks AI is a conversational AI chatbot designed to serve as a shopping assistant, providing users with a seamless and intelligent shopping experience. Here you will find information on the features, technologies, and tools used in the development of this chatbot.

## Glimpse of Streaks Ai!
![Streaks Ai in action]()

## Features

### Version 2 (Current)
- **Internet Functionality**: Integrated DuckDuckGo for real-time information retrieval from the web.
- **Enhanced Features**: Future versions will include additional eCommerce sites and more advanced functionalities.

### Version 1
- **Product Search**: Retrieve results from Amazon and compare products.
- **Product Information**: Answer specific questions about products.

## Platforms Used

1. **Google's Gemini**: Powers the AI with fine-tuning, prompt engineering, and function calling specifically for the shopping assistant use case.
2. **DuckDuckGo**: Utilized for real-time information searches. A custom response template is employed to ensure accuracy.
3. **Amazon**: The primary eCommerce platform for product search results. Uses a specialized scraping method to fetch results, though occasional failures may occur.

## Tools and Technologies

- **Web Scraping**: For extracting data from web pages.
- **Regex and XPath**: For parsing and extracting information.
- **Prompt Engineering and LLM Function Calling**: Customizing interactions and responses.
- **Python**: Core programming language used for development.
- **Streamlit**: Framework for building the user interface.
- **Gemini Flash API**: Interface with Google's Gemini for natural language processing.
- **DuckDuckGo API**: For real-time web search functionality.
- **Requests and BeautifulSoup**: For making HTTP requests and parsing HTML content.

## Live Application

You can check out the live app [https://streaks-ai.streamlit.app/](#).

## Installation and Usage

To set up and use Streaks AI locally, follow these instructions:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/streaks-ai.git
   ```

2. Navigate to the project directory:
   ```bash
   cd streaks-ai
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Contributing

We welcome contributions to improve Streaks AI. Feel free to submit your improvements or report issues.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any inquiries or further information, please contact [sridharstreaks@gmail.com] or open an issue in this repository.

Thank you for your interest in Streaks AI. Star ⭐ my repo incase you like my work!
