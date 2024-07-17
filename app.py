import streamlit as st
import preproccesing,helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preproccesing.preprocess(data)

    user_list = df['user'].unique().tolist()
    user_list.remove("group notification")
    user_list.sort()
    user_list.insert(0,'overall')
    selected_user = st.sidebar.selectbox("Select a user",user_list)

    if st.sidebar.button("Show analysis"):

        #stats
        num_msg,words,num_media,num_url = helper.fetch_stats(selected_user,df)
        st.title("Top statistics")
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.subheader("Total messages")
            st.header(num_msg)

        with col2:
            st.subheader("No of words")
            st.header(words)

        with col3:
            st.subheader("No of media")
            st.header(num_media)

        with col4:
            st.subheader("No of links")
            st.header(num_url)

        #timeline
        st.title("Monthly Timeline")
        timeline = helper.timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color = "green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Timeline")
        d_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(d_timeline['only_date'], d_timeline['message'], color="black")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        #weekly activity and monthly activity
        st.title('Activity Map')
        col1,col2 = st.columns(2)
        with col1:
            busy_day = helper.week_activity(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            busy_month = helper.month_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color = "Orange")
            plt.xticks(rotation = "vertical")
            st.pyplot(fig)

        #Heatmap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        #To find out most active users

        if selected_user=='overall':
            st.title("Most active users")
            x,per= helper.most_active_user(df)
            fig,ax = plt.subplots()
            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color = "red")
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(per)


        #word cloud

        st.title("Word Cloud")

        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common 20 words
        word_df = helper.most_commmon_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(word_df[0],word_df[1])
        st.title("Most common words")
        st.pyplot(fig)

        #emoji analysis

        emoji_df = helper.emoji_analysis(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)


        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1],labels=emoji_df[0],autopct="%0.2f")
            st.pyplot(fig)



                










