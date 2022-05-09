# importing the requests library
import requests
import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

endpoint = "http://127.0.0.1:5000/"

st.title('Social Media Analytics')


st.header('Recommend content to a specific user (you need to put the name of of an existing follower of Equinox: https://www.linkedin.com/company/equinox-ai-lab)')
st.subheader('This collaborative recommendation takes into account users with similar taste and recommend unseen content')
user = st.text_input('User you would like to recommend (case sensitive):')

if user != '':
    req = {'user':user}
    r = requests.post(endpoint + 'recommend_post', json=req)
    st.write('Recommended content for ' + user, r.json())

st.header('Who is interested in a specific topic? How influential are they?')
topic = st.text_input('Find people interested in:')

if topic != '':
    req = {'topic':topic}
    r = requests.post(endpoint + 'people_interested', json=req)

    data = pd.DataFrame(r.json())

    st.table(data)

st.header('Find common interests in followers with specific key-words in profile description')
profile = st.text_input('Find common interests in profiles that contain the key-word:')

if profile != '':
    req = {'profile':profile}
    r = requests.post(endpoint + 'common_interests', json=req)

    dict = r.json()

    text = ''

    for post in dict['post']:
        text = text + ' ' + post

    wordcloud = WordCloud().generate(text)

    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(fig)

    st.write('Common interests' , dict)

st.header('How many followers have a specific key-word in description?')
profile2 = st.text_input('Number of followers with the following key-word in description:')

if profile2 != '':
    req = {'profile':profile2}
    r = requests.post(endpoint + 'num_followers', json=req)

    st.write(r.json())

st.header('What is the reach per type of profile?')
st.subheader('The reach is the sum of followers per type of profile ')
profile3 = st.text_input('Reach of followers with following key-word in description:')

if profile3 != '':
    req = {'profile':profile3}
    r = requests.post(endpoint + 'followers_reach', json=req)

    st.write(r.json())

st.header('What do the most influential people like')
r4 = requests.get(endpoint + 'influential_taste')
dict4 = r4.json()

text = ''

for post in dict4['post']:
    text = text + ' ' + post

wordcloud4 = WordCloud().generate(text)

fig4, ax4 = plt.subplots()
ax4.imshow(wordcloud4, interpolation='bilinear')
plt.axis("off")
st.pyplot(fig4)

st.write('Posts liked by most influential people' , dict4)













