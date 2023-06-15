import re
import pandas as pd


def preprocessor(data):
    #datetime_pattern = "\d{1,2}/\d{1,2}/\d{1,2}, \d{1,2}:\d{1,2}:\d{1,2} [AP]M:"
    pattern = "\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{1,2}\s[ap]m\s-\s"

    # separating messages from dates and vice-versa
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # making table with labels
    df = pd.DataFrame({'user_messages': message, 'message_date': dates})

    # formatting datetime
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # putting names in separate array and messages in separate array
    users = []
    messages = []
    for message in df['user_messages']:
        expression = '([\w\W]+?):\s'
        entry = re.split(expression, message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group notification')
            messages.append(entry[0])

    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['user_messages'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['dates'] = df['date'].dt.day
    df['day'] = df['date'].dt.day_name()
    df['only_dates'] = df['date'].dt.date
    df['hours'] = df['date'].dt.hour
    df['minutes'] = df['date'].dt.minute
    df['seconds'] = df['date'].dt.second

    period = []
    for hour in df[['day', 'hours']]['hours']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 00:
            period.append(str(hour) + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df