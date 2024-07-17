import re
import pandas as pd


def preprocess(data):
    pattern = r'\b\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}\u202f[APMapm]{2}\b'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    if len(messages) != len(dates):
        raise ValueError("The number of messages does not match the number of dates.")

    df = pd.DataFrame({"user_messages": messages, "message_date": dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format="%m/%d/%y, %I:%M %p")
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Safely split user and message
    user_message_split = df['user_messages'].apply(
        lambda text: text.split(': ', 1) if ': ' in text else ["group notification", text]
    )

    # Convert list to DataFrame
    user_message_df = pd.DataFrame(user_message_split.tolist(), columns=['user', 'message'])

    df = pd.concat([df, user_message_df], axis=1)

    df.drop(columns=['user_messages'], inplace=True)

    df["year"] = df['date'].dt.year
    df['only_date'] = df['date'].dt.date
    df["month"] = df['date'].dt.month_name()
    df['day_name'] = df['date'].dt.day_name()
    df["month_num"] = df['date'].dt.month
    df["day"] = df["date"].dt.day
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
