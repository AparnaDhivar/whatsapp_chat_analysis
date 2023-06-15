import string

import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji

extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user == 'Overall':
        num_messages = df.shape[0]
        word = []
        for messagess in df['messages']:
            word.extend(messagess.split())
        media_messages = df[df['messages'] == '<Media omitted>\n']
        media_msg = media_messages.shape[0]
        links = []
        for message in df['messages']:
            links.extend(extract.find_urls(message))
        return num_messages, word, media_msg, links

    else:
        new_df = df[df['users'] == selected_user]
        num_messages = new_df.shape[0]
        word = []
        for messagess in new_df['messages']:
            word.extend(messagess.split())
        media_messages = new_df[df['messages'] == '<Media omitted>\n']
        media_msg = media_messages.shape[0]
        links = []
        for message in new_df['messages']:
            links.extend(extract.find_urls(message))
        return num_messages, word, media_msg, links


def most_busy_user(df):
    x = df['users'].value_counts().head()
    y = round((df['users'].value_counts() * 100) / df.shape[0])
    name = x.index
    count = x.values
    allnames = y.index
    percent = y.values
    return name,count ,allnames , percent


def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    temp = df[df['users'] != 'Group notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    def remove_stop_words(message):
        cloudwords = []
        for words in message.lower().split():
            if words not in stop_words:
                cloudwords.append(words)
        return " ".join(cloudwords)

    wc = WordCloud(height=500,width=500,min_font_size=10)
    temp['messages'] = temp['messages'].apply(remove_stop_words)
    df_wc = wc.generate(temp['messages'].str.cat(sep =" "))
    return df_wc


def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    temp = df[df['users'] != 'Group notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    topwords = []
    for message in temp['messages']:
        for word in message.lower().split():
            new_word = word.translate(str.maketrans('', '', string.punctuation))
            # print(new_word)
            if new_word not in stop_words:
                topwords.append(word)

    return_df = pd.DataFrame(Counter(topwords).most_common(20))
    return return_df


def emoji_counter(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    all_emojis = []
    for messages in df['messages']:
        all_emojis.extend([c for c in messages if c in emoji.UNICODE_EMOJI['en']])

    return_emojis = pd.DataFrame(Counter(all_emojis).most_common(len(Counter(all_emojis))))
    return return_emojis


# monthly timeline
def timeline_display(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline


def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    daily_timeline = df.groupby('only_dates').count()['messages'].reset_index()
    return daily_timeline


def most_busy_day(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    busy_day = df['day'].value_counts()
    return busy_day


def most_busy_month(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    busy_month = df['month'].value_counts()
    return busy_month


def activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    act_map = (df.pivot_table(index='day', columns='period', values='messages', aggfunc='count').fillna(0))

    return act_map



