import streamlit as st
import helpers.preprocessor as preprocessor
import helpers.helper as helper
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import emoji
import pickle


st.markdown("""
    <h1 style="text-align:center; color:#2C3E50; font-family: 'Poppins', sans-serif;">📊 WhatsApp Chat Insights</h1>
    <h5 style="text-align:center; color:#7F8C8D;">Gain detailed insights from your WhatsApp conversations.</h5>
""", unsafe_allow_html=True)


# Sidebar Styling
st.sidebar.markdown("""
    <h1 style="text-align:center; color:#2C3E50; font-family: 'Poppins', sans-serif;">📊 WhatsApp Chat Insights</h1>
""", unsafe_allow_html=True)

# File uploader with styling
uploaded_file = st.sidebar.file_uploader(
    "📂 **Upload a WhatsApp Chat File (TXT)**",
    type=['txt']
)

if uploaded_file is not None:
    try:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8", errors="ignore")  # Ignore decoding errors

        df = preprocessor.preprocess(data)

        # st.dataframe(df)

        # Fetch unique users
        user_list = df['user'].unique().tolist()
        if 'group_notification' in user_list:
            user_list.remove('group_notification')

        user_list.sort()
        user_list.insert(0, "Overall")

        selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
        # Stats area with 4 things
        st.markdown("<h1 style='color:#4CAF50; text-align:center;'>📊 Top Statistics</h1>", unsafe_allow_html=True)

        if st.sidebar.button("🚀 Show Analysis"):
            num_messages, word , num_media_messages,num_links = helper.fetch_stats(selected_user, df)
            col1, col2 ,col3 , col4 = st.columns(4)
            card_style = """
                       <div style="background-color:#f1f3f4; padding:20px; border-radius:10px; 
                                   text-align:center; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
                           <h3 style='color:#333;'>{}</h3>
                           <h1 style='color:#4CAF50;'>{}</h1>
                       </div>
                   """

            with col1:
                st.markdown(card_style.format("💬 Total Messages", num_messages), unsafe_allow_html=True)

            with col2:
                st.markdown(card_style.format("📝 Total Words", word), unsafe_allow_html=True)

            with col3:
                st.markdown(card_style.format("📸 Media Shared", num_media_messages), unsafe_allow_html=True)
            with col4:
                st.markdown(card_style.format("🔗 Links Shared", num_links), unsafe_allow_html=True)


    except Exception as e:

        st.error(f"⚠️ Error processing file: {str(e)}")  # Display error in a friendly way

    #monthly_timeline
    st.markdown("<h1 style='color:#4CAF50; text-align:center;'>📆 Monthly Timeline</h1>", unsafe_allow_html=True)

    timeline  = helper.monthly_helper(selected_user, df)
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 5))  # Adjust size for better display

    ax.plot(
        timeline['time'],
        timeline['message'],
        color='#E63946', 
        marker='o',
        linestyle='-',
        linewidth=2,
        markersize=6,
        markerfacecolor='white',
        markeredgewidth=2
    )

    # Beautify the graph
    ax.set_facecolor("#F8F9FA")  # Light gray background
    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.6)  # Soft gridlines
    ax.set_xlabel("Month", fontsize=12, fontweight='bold', color="#333")
    ax.set_ylabel("Messages", fontsize=12, fontweight='bold', color="#333")
    ax.set_title("Messages Over Time", fontsize=14, fontweight='bold', color="#2C3E50")
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, fontsize=10, color="#555")
    plt.yticks(fontsize=10, color="#555")

    # Remove unnecessary borders
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    # Display the plot in Streamlit
    st.pyplot(fig)


    # daily timeline
    st.markdown("<h1 style='color:#4CAF50; text-align:center;'>📅 Daily Timeline</h1>", unsafe_allow_html=True)

    daily_timeline = helper.daily_helper(selected_user, df)
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(
        daily_timeline['only_date'],
        daily_timeline['message'],
        color='#1E88E5',  # Soft blue color
        marker='o',
        linestyle='-',
        linewidth=2,
        markersize=6,
        markerfacecolor='white',
        markeredgewidth=2
    )
    ax.set_facecolor("#F8F9FA")  # Light gray background
    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.6)  # Soft gridlines
    ax.set_xlabel("Date", fontsize=12, fontweight='bold', color="#333")
    ax.set_ylabel("Message Count", fontsize=12, fontweight='bold', color="#333")
    ax.set_title("Daily Messages Trend", fontsize=14, fontweight='bold', color="#2C3E50")
    plt.xticks(rotation=45, fontsize=10, color="#555")
    plt.yticks(fontsize=10, color="#555")

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    # Display the plot in Streamlit
    st.pyplot(fig)



    # activity map
    st.markdown("<h1 style='color:#4CAF50; text-align:center;'>🗺️ Activity Map</h1>", unsafe_allow_html=True)

    col1,col2 = st.columns(2)
    with col1:
        st.markdown("<h3 style='color:#E63946; text-align:center;'>📆 Most Busy Day</h3>", unsafe_allow_html=True)

        busy_day = helper.week_activity_map(selected_user, df)
        fig, ax = plt.subplots(figsize=(6, 4))  # Better figure size

        ax.bar(busy_day.index, busy_day.values, color="#E63946", alpha=0.8)
        ax.set_facecolor("#F8F9FA")  # Light gray background
        ax.grid(axis='y', linestyle='--', alpha=0.5)  # Soft grid

        plt.xticks(rotation=45, fontsize=10, color="#555")
        plt.yticks(fontsize=10, color="#555")

        ax.set_xlabel("Day", fontsize=12, fontweight='bold', color="#333")
        ax.set_ylabel("Message Count", fontsize=12, fontweight='bold', color="#333")
        ax.set_title("Activity by Day", fontsize=14, fontweight='bold', color="#2C3E50")

        st.pyplot(fig)

    # 📆 Most Busy Month
    with col2:
        st.markdown("<h3 style='color:#FFA500; text-align:center;'>🗓️ Most Busy Month</h3>", unsafe_allow_html=True)

        busy_month = helper.month_activity_map(selected_user, df)
        fig, ax = plt.subplots(figsize=(6, 4))

        ax.bar(busy_month.index, busy_month.values, color="#FFA500", alpha=0.8)
        ax.set_facecolor("#F8F9FA")
        ax.grid(axis='y', linestyle='--', alpha=0.5)

        plt.xticks(rotation=45, fontsize=10, color="#555")
        plt.yticks(fontsize=10, color="#555")

        ax.set_xlabel("Month", fontsize=12, fontweight='bold', color="#333")
        ax.set_ylabel("Message Count", fontsize=12, fontweight='bold', color="#333")
        ax.set_title("Activity by Month", fontsize=14, fontweight='bold', color="#2C3E50")

        st.pyplot(fig)

    st.markdown("<h2 style='color:#1E88E5; text-align:center;'>📊 Weekly Activity Heatmap</h2>", unsafe_allow_html=True)

    user_heatmap = helper.activity_heatmap(selected_user, df)

    fig, ax = plt.subplots(figsize=(10, 5))  # Larger size for better readability

    # FIX: Use fmt=".0f" for floats to display as whole numbers
    sns.heatmap(
        user_heatmap,
        cmap="YlGnBu",
        linewidths=0.5,
        linecolor='white',
        annot=True,
        fmt=".0f",  # Correct format for floating-point numbers
        cbar=True
    )

    # Beautify the heatmap
    ax.set_xlabel("Hour of Day", fontsize=12, fontweight='bold', color="#333")
    ax.set_ylabel("Day of Week", fontsize=12, fontweight='bold', color="#333")
    st.pyplot(fig)

# 🏆 Most Busy Users (Group Level)
    if selected_user == "Overall":
        st.markdown("<h1 style='color:#FF9800; text-align:center;'>🏆 Most Busy Users</h1>", unsafe_allow_html=True)

        # Get busiest users data
        x, new_df = helper.most_busy_user(df)

        # Create columns with custom width ratio for better layout
        col1, col2 = st.columns([2, 1])  # col1 takes more space, col2 less

        # 📊 Bar Chart (Top Users)
        with col1:
            st.markdown("<h3 style='text-align:center; color:#FF5722;'>Top Active Users</h3>", unsafe_allow_html=True)

            fig, ax = plt.subplots(figsize=(6, 4))  # Better figure size
            ax.bar(x.index, x.values, color="#FF9800", alpha=0.85)  # Orange bars

            # Beautify the chart
            ax.set_facecolor("#F8F9FA")  # Light gray background
            ax.grid(axis='y', linestyle='--', alpha=0.5)  # Subtle grid
            ax.set_xlabel("Users", fontsize=12, fontweight='bold', color="#333")
            ax.set_ylabel("Message Count", fontsize=12, fontweight='bold', color="#333")
            ax.set_title("Top Contributors", fontsize=14, fontweight='bold', color="#2C3E50")

            # Improve x-axis readability
            plt.xticks(rotation=45, fontsize=10, color="#555")
            plt.yticks(fontsize=10, color="#555")

            # Remove unnecessary borders
            for spine in ["top", "right"]:
                ax.spines[spine].set_visible(False)

            st.pyplot(fig)

        # 📋 Data Table (Detailed Statistics)
        with col2:
            st.markdown("<h3 style='text-align:left; color:#4CAF50;'>User Statistics</h3>", unsafe_allow_html=True)

            # Aligning DataFrame to the right by using empty space
            st.markdown("<div style='text-align:right;'>", unsafe_allow_html=True)
            st.dataframe(new_df.style.set_properties(**{
                'background-color': '#F8F9FA',
                'color': '#333',
                'border-color': 'black',
                'font-size': '14px',
                'text-align': 'center'
            }))
            st.markdown("</div>", unsafe_allow_html=True)


    # WordCloud
        st.markdown("""
            <h1 style='color:#4CAF50; text-align:center;'>🌥️ Word Cloud Generator</h1>
        """, unsafe_allow_html=True)
        df_wc = helper.create_wordcloud(selected_user, df)


        # Ensure the word cloud is generated correctly
        if df_wc is not None:
            fig, ax = plt.subplots()
            ax.imshow(df_wc, interpolation="bilinear")  # Fix: Ensure correct image format
            ax.axis("off")  # Hide axes
            st.pyplot(fig)
        else:
            st.warning("Word cloud could not be generated. Try using more text data.")


    # Most Common Words Section
        st.markdown("<h1 style='color:#4CAF50; text-align:center;'>🔤 Most Common Words</h1>", unsafe_allow_html=True)
        most_common_df = helper.most_common_words(selected_user, df)

        if most_common_df is not None and not most_common_df.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=most_common_df[1], y=most_common_df[0], palette="viridis", ax=ax)
            ax.set_xlabel("Count", fontsize=14, color="#333")
            ax.set_ylabel("Words", fontsize=14, color="#333")
            plt.xticks(rotation=45, fontsize=12)
            plt.yticks(fontsize=12)
            st.pyplot(fig)
        else:
            st.warning("⚠️ Not enough data to display most common words.")


    # Emoji Analysis
        st.markdown("<h1 style='color:#4CAF50; text-align:center;'>😀 Emoji Analysis</h1>", unsafe_allow_html=True)
        emoji_df = helper.emoji_helper(selected_user, df)

        if emoji_df is not None and not emoji_df.empty:
                st.dataframe(emoji_df, use_container_width=True)

        else:
            st.warning("⚠️ Not enough data to display emoji analysis.")

