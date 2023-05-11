import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
import time

# basic input instructions

st.info("👈 Please export your whatsapp chats excluding the media files and upload it to the sidebar then click the show analysis button")



st.sidebar.title(":blue[Chat Analyzer] 🕵")


uploaded_file = st.sidebar.file_uploader("Upload your file here")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    with st.spinner('`Almost there ... Read something interesting while we process your request `'):
        time.sleep(2)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis:blue[(Switch users from dropdown menu)]",user_list)

    if st.sidebar.button("Show Analysis🔍"):

        st.snow()

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.title(":blue[Overall Statistics]📈")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("`Total Messages`")
            st.title(num_messages)
        with col2:
            st.header("`Total Words`")
            st.title(words)
        with col3:
            st.header("`Media Shared`")
            st.title(num_media_messages)
        with col4:
            st.header("`Links Shared`")
            st.title(num_links)

        st.markdown('''----''')

        # monthly timeline
        st.title(":blue[Monthly Timeline]📅")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # daily timeline
        st.title(":blue[Daily Timeline]📅")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.markdown('''----''')

        # activity map
        st.title(':blue[Activity Map]')
        col1,col2 = st.columns(2)

        with col1:
            st.header("`Most busy day`⏱")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("`Most busy month`⏱")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)



        st.title(":blue[Weekly Activity Heat Map📝]")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        st.markdown('''----''')

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title(':blue[Most Busy Users]🧑‍💻')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)


        # WordCloud
        st.title(":blue[Wordcloud]  💭")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.markdown('''
        
        ----''')

        # generating a sentiment analysis baised piechart

        data = df.dropna()
        from nltk.sentiment.vader import SentimentIntensityAnalyzer

        sentiments = SentimentIntensityAnalyzer()
        data["positive"] = [sentiments.polarity_scores(i)["pos"] for i in data["message"]]
        data["negative"] = [sentiments.polarity_scores(i)["neg"] for i in data["message"]]
        data["neutral"] = [sentiments.polarity_scores(i)["neu"] for i in data["message"]]

        x = sum(data["positive"])
        y = sum(data["negative"])
        z = sum(data["neutral"])


        st.error("⚠️ The sentiment analysis shown below depicts the sentiments of overall group members not any particular individual")

        st.markdown('''### :blue[SENTIMENT ANALYSIS RESULTS] (😡😄😐) ''')

        st.markdown('''#### `Expandable Dataframe`''')

        st.dataframe(data)

        def score(a, b, c):

            if (a > b) and (a > c):
                st.markdown('''#### **The overall sentiment is :** `Positive` ''')
            if (b > a) and (b > c):
                st.markdown('''#### **The overall sentiment is :** `Negative`''')
            if (c > a) and (c > b):
                st.markdown('''### **The overall sentiment is :** `Neutal`''')


        score(x, y, z)

        st.markdown('''## `[Pie chart]` ''')

        user_Emotions = ["Positive", "Negative", "Neutral"]
        user_Ratings = [x, y, z]
        plt.pie(user_Ratings, labels=user_Emotions, startangle=0, shadow=True, colors=["green", "red", "lightblue"],
                autopct="%2.1f%%")
        plt.legend(title="Sentiments")
        st.set_option('deprecation.showPyplotGlobalUse', False)
        fig = plt.show()
        st.pyplot(fig)

        st.markdown('''----''')

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis 🔍")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title(':blue[Most commmon words]📋')
        st.pyplot(fig)

        st.markdown('''----''')

#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------

    st.markdown('## *`About project Nina`*  ', unsafe_allow_html=True)
    st.info('''
    - Nina is a simple  yet effective tool for (***Data Analysis***)  which can be used in the field of data science for data analytics and representation.
    - Nina uses the feature of (***Sentiment Analysis***) using the python (***nltk (Natural Language Toolkit)***) which uses Natural Language Processing libraries. 
    - Feel free to navigate around and explore  the various features ,functionalities ,applications  and libraries of this project.
    - These tools can be used in the fields of machine learning , deep learning , and artificial intelligence. 
    - These types of software are high in demand as these are used along with the cutting edge technologies and are used by the most of the big tech giants (Google,Microsoft,Meta,Reddit,LinkedIn,Twitter,Twitch ,etc..) as well as non tech firms sice decades.
    ''')

    st.error('''
    #### *Libraries & modules used in the project :*

    - **Pandas** , **Streamlit** ,**Regular Expressions** ,**Matplotlib** ,**Seaborn**, **Natural Language Toolkit** 
    - **Urlextract**, **Wordcloud**, **Collections** ,**Emoji** ,**Python Imaging Library** ,**Time**
    ''')
    st.warning('''
    #### *Areas where project Nina can be used :*

    - Medical research 
    - Social media and other entertainment industries 
    - Education (ED-TECH industries) & Innovation 
    - E-Commerce & Businesses,Startups
    - Scientific research and Experiments
    - Basic surveillance and monitering 
    - And " MANY MORE "
    
    ''')

    def txt2(a, b):
        col1, col2 = st.columns([2, 4])
        with col1:
            st.markdown(f'`{a}`')
        with col2:
            st.markdown(b)


    st.markdown('''
    ### ***:blue[Reach out to me :]***
    ------------------------
    ''')
    txt2('Download the source code ', 'https://github.com/X4B3RB6T/Project-Nina')
    txt2('Email  ', 'adityasighamber7@gmail.com')
    txt2('Instagram ', 'https://www.instagram.com/aditya_singhamber/')
    txt2('LinkedIn ', 'https://in.linkedin.com/in/aditya-singh-amber-6b6b3a1b6')
    txt2('Github Profile link', 'https://github.com/X4B3RB6T')




















