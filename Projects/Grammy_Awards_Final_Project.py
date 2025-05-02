# Import libraries
import pandas as pd
import plotly.express as px
import numpy as np

# RUN THIS CELL - DO NOT MODIFY
# this formats numbers to two decimal places when shown in pandas
pd.set_option('display.float_format', lambda x: '%.2f' % x)

# Read in dataframes
full_df = pd.read_csv("datasets/grammy_live_web_analytics.csv")
rec_academy = pd.read_csv("datasets/ra_live_web_analytics.csv")

# preview full_df dataframe
full_df.head()

# preview rec_academy dataframe
rec_academy.head()

# Plot a line chart of the visitors on the site.
px.line(full_df, x = "date", y = "visitors")

average_award_night = full_df.groupby("awards_night").agg({'visitors' : 'mean'})
print(average_award_night)

# Split the data to separate the full_df into two new dataframes.
# One for before the switch of the websites and one for after
date = '2022-02-01'
combined_site = full_df[full_df['date'] < date]
grammys = full_df[full_df['date'] >= date]

# Run the following cell - DO NOT MODIFY
# .copy() prevents pandas from printing a scary-looking warning message
combined_site = combined_site.copy()
grammys = grammys.copy()

# print the shape of the combined_site dataframe
combined_site.shape

# create the list of dataframes
frames = [combined_site, rec_academy, grammys]

# create the `pages_per_session` column for all 3 dataframes.
for frame in frames:
    frame['pages_per_session'] = frame['pageviews'] / frame['sessions']

# combined_site graph
px.line(combined_site, x = 'date', y = 'pages_per_session')

# grammys graph
px.line(grammys, x = 'date', y = 'pages_per_session')

# rec_academy graph
px.line(rec_academy, x = 'date', y = 'pages_per_session')

def bounce_rate(dataframe):
    '''
    Calculates the bounce rate for visitors on the website.
    input: dataframe with bounced_sessions and sessions columns
    output: numeric value from bounce rate
    '''
    # WRITE YOUR CODE BELOW
    # Remember, the input for the function is called `dataframe`
    # So all calculations should reference that variable.
    
    sum_bounced = dataframe['bounced_sessions'].sum()
    sum_sessions = dataframe['sessions'].sum()
    
    return 100 * sum_bounced / sum_sessions

# Calculate the Bounce Rate for each site. Use the frames list you created in Task 6.
frames = [
    ('Combined Site', combined_site), 
    ('Recording Academy', rec_academy), 
    ('Grammys', grammys)
    ]

for name, frame in frames:
    rate = bounce_rate(frame)
    
    print(f'{name} bounce rate is: {rate: 0.2f} %')

for name, frame in frames:
    session_avg = frame['avg_session_duration_secs'].mean()
    
    print(f'The average session on {name} is {session_avg: 0.2f} seconds.')

# read in the files
age_grammys = pd.read_csv('datasets/grammys_age_demographics.csv')
age_tra = pd.read_csv('datasets/tra_age_demographics.csv')

# preview the age_grammys file. the age_tra will look very similar.
age_grammys.head()

# create the website column
age_grammys['website'] = 'Grammys'
age_tra['website'] = 'Recording Academy'

# use pd.concat to join the two datasets
age_df = pd.concat([age_grammys, age_tra], axis = 0)

print(age_df.shape)
print(age_df)

# Create bar chart

px.bar(age_df, x = 'age_group', y = 'pct_visitors', color = 'website', barmode = 'group')

# Load in the data

desktop_users = pd.read_csv('datasets/desktop_users.csv')
mobile_users = pd.read_csv('datasets/mobile_users.csv')

# preview the desktop_users file
desktop_users.tail()

# preview mobile_users file
mobile_users.head()

# change name of the visitors column to indicate which category it comes from
desktop1 = desktop_users.rename(columns = {'visitors': 'desktop_visitors'})

mobile1 = mobile_users.rename(columns = {'visitors': 'mobile_visitors'})

# drop the segment column from each dataframe
desktop2 = desktop1.drop(columns = 'segment')

mobile2 = mobile1.drop(columns = 'segment')

# join the two dataframes and preview the dataframe

segment_df = pd.merge(desktop2, mobile2, how = 'inner')

segment_df.tail()

# create total_visitors column
segment_df['total_visitors'] = segment_df['desktop_visitors'] + segment_df['mobile_visitors']
segment_df.tail()

# filter and calculate the percentage share
filtered_df = segment_df[segment_df['date'] >= '2023-04-01']

desktop_sum = filtered_df['desktop_visitors'].sum()
total_sum = filtered_df['total_visitors'].sum()

desktop_per = (desktop_sum / total_sum) * 100
mobile_per = 100 - desktop_per

print(f'Total Visitors: {total_sum}')
print(f'Desktop Visitors: {desktop_per: 0.2f}%')
print(f'Mobile Visitors: {mobile_per: 0.2f}%')
