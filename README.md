# 📊WhatsApp Chat Insights

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Render](https://img.shields.io/badge/Render-4DBA87?style=for-the-badge&logo=render&logoColor=white)](https://render.com/)


Welcome to the **WhatsApp Chat Insights** project! This tool provides in-depth analysis and visualizations of your WhatsApp chat data. By processing an exported chat file from WhatsApp, it generates various statistics, such as message counts, word clouds, user activity, emojis, and more. The goal of this project is to provide you with meaningful insights from your WhatsApp conversations, whether for fun or data analysis purposes.

## Features

This project provides the following features:

1. **Message Statistics**: 
   - Displays the total number of messages in the chat.
   - Counts the number of media files (e.g., images, videos) shared.
   - Counts the number of links shared in the chat.

2. **Most Active Users**:
   - Identifies the users who are most active in the chat based on message counts.
   - Provides a detailed report on the percentage of activity per user.

3. **Word Cloud**:
   - Generates a word cloud of the most frequently used words in the chat, excluding stop words (such as common filler words).

4. **Emoji Analysis**:
   - Displays the most frequently used emojis in the chat, giving insight into the emotional tone of the conversation.

5. **Activity Heatmap**:
   - Visualizes the distribution of messages across different days of the week and times of the day, helping to identify active periods.

6. **Monthly/Daily Reports**:
   - Provides activity reports broken down by day and month to show how chat activity evolves over time.

## Requirements

Before you can use or deploy this project, you need to install the necessary dependencies. The following libraries are required:

- **Streamlit**: For building the interactive web application.
- **Matplotlib**: For generating visualizations such as graphs and charts.
- **Seaborn**: For improved visualizations and styling of charts.
- **Urlextract**: For extracting links from chat messages.
- **Wordcloud**: For generating word clouds from chat messages.
- **Pandas**: For data manipulation and analysis.
- **Emoji**: For analyzing emojis used in the chat.

### To Install Dependencies:

You can easily install all required libraries via the `requirements.txt` file:

  ```sh
pip install -r requirements.txt
  ```

## How to Run the Project Locally
### 1. Prepare Your WhatsApp Chat File
Make sure your WhatsApp chat is exported in text format.

Export the chat from WhatsApp by going to the chat > clicking the three dots on the top right > More > Export chat > Without Media.
The exported file will be a .txt file.
### 2. Run the Streamlit Application
In the project directory, run the following command:
  ```sh
streamlit run app.py
  ```
This will start the Streamlit server and you can view the app in your browser.

## Contributing
If you'd like to contribute to this project, feel free to fork the repository, make changes, and create a pull request. Any improvements, bug fixes, or feature additions are welcome.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


