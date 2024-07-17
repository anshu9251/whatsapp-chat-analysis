from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != "overall":

        df = df[df['user']==selected_user]

    #total messages
    t_msg = df.shape[0]

    # no of words
    words = []
    for i in df['message']:
        words.extend(i.split())


    #no of media
    num_media = df[df["message"] == '<Media omitted>\n'].shape[0]

    #no of Links
    url = []
    for i in df["message"]:
        url.extend(extract.find_urls(i))

    return t_msg, len(words),num_media,len(url)

def most_active_user(df):
    x = df['user'].value_counts().head()
    per = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={"count": "percent"})
    return x,per

def create_wordcloud(selected_user,df):
    if selected_user != "overall":
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color="white")
    df_wc = wc.generate(df["message"].str.cat(sep = " "))

    return df_wc

def most_commmon_words(selected_user,df):
    f = open("stop_hinglish.txt", "r")
    stop_words = f.read()

    if selected_user != "overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != "group notification"]
    temp = temp[temp['message'] != "<Media omitted>\n"]

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    word_df = pd.DataFrame(Counter(words).most_common(20))

    return word_df

def emoji_analysis(selected_user,df):
    if selected_user != "overall":
        df = df[df['user'] == selected_user]

    emojis = []
    for i in df['message']:
        emojis.extend([c for c in i if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(20))

    return emoji_df

def timeline(selected_user,df):
    if selected_user != "overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):
    if selected_user != "overall":
        df = df[df['user'] == selected_user]

    d_timeline = df.groupby('only_date').count()['message'].reset_index()

    return d_timeline

def week_activity(selected_user,df):
    if selected_user != "overall":
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity(selected_user,df):
    if selected_user != "overall":
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_map(selected_user,df):
    if selected_user != "overall":
        df = df[df['user'] == selected_user]

    user_map = df.pivot_table(index="day_name",columns="period",values="message",aggfunc="count").fillna(0)

    return user_map
