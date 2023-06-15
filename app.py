import streamlit as st
import matplotlib.pyplot as plt
import preprocessor, helper
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader('Choose a file')  # fileUploading
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()  # getting Value From File
    data = bytes_data.decode('utf-8')  # decoding file

    df = preprocessor.preprocessor(data)  # putting data in preprocessor function to convert in separete form
    st.dataframe(df)  # converting in date

    user_list = df['users'].unique().tolist()  # fetching unique users
    user_list.remove('Group notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox('Show analysis wrt', user_list)

    # stats of users
    if st.sidebar.button('Show Analysis'):
        num_messages, word, media_msg, links = helper.fetch_stats(selected_user, df)
        st.header('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header('Total Messages')
            st.title(num_messages)

        with col2:
            st.header('Total Words')
            st.title(len(word))

        with col3:
            st.header('Total Media')
            st.title(media_msg)

        with col4:
            st.header('Total Links')
            st.title(len(links))

    # monthly timeline
        timeline = helper.timeline_display(selected_user,df)
        st.header('Monthly Timeline')
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['messages'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    # daily timeline
        daily_timeline = helper.daily_timeline(selected_user,df)
        st.header('Daily Timeline')
        fig , ax = plt.subplots()
        ax.plot(daily_timeline['only_dates'],daily_timeline['messages'],color='blue')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    # most busy day and most busy month
        col1, col2 = st.columns(2)
        with col1:
            busy_day = helper.most_busy_day(selected_user,df)
            st.header('Busy day')
            fig , ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='grey')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            busy_month = helper.most_busy_month(selected_user, df)
            st.header('Busy month')
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='black')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

    # Heatmap - activity analysis of whole day divided by hours
        act_map = helper.activity_map(selected_user,df)
        st.header('Daily activity map in hours')
        fig,ax= plt.subplots()
        ax = sns.heatmap(act_map)
        st.pyplot(fig)

    # most busy user group level analysis
        if selected_user == 'Overall':
            name,count,allnames,percent = helper.most_busy_user(df)
            col1, col2 = st.columns(2)
            with col1:
                st.header('Most Busy User')
                fig, ax = plt.subplots()
                ax.bar(name,count,color='brown')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.header('Overall user analysis')
                fig1, ax1 = plt.subplots()
                ax1.pie(percent,labels=allnames,autopct='%1.1f%%')
                ax1.axis('equal')
                st.pyplot(fig1)

    # word cloud generating
        df_wc = helper.create_wordcloud(selected_user,df)
        st.header('Word Cloud')
        fig , ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

    # most common words used
        return_df = helper.most_common_words(selected_user,df)
        st.header('Most common words')
        fig , ax = plt.subplots()
        ax.barh(return_df[0],return_df[1],color='indigo')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

    # emoji count
        return_emojis = helper.emoji_counter(selected_user,df)
        st.header('Most frequent emojis')
        col1 ,col2 = st.columns(2)
        with col1:
            st.dataframe(return_emojis)
        with col2:
            fig,ax=plt.subplots()
            ax.bar(return_emojis[0].head(10),return_emojis[1].head(10),color='orange')
            st.pyplot(fig)


