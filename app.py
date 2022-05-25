import streamlit as st
import pandas as pd
import os

file_list = []


def make_clickable(username):
    # target _blank to open new window
    # extract clickable text to display for your link
    
    link = f"https://twitter.com/{username}"
    return f'<a target="_blank" href="{link}">Twitter url</a>'




@st.cache
def load_data():
    # popular_df = pd.read_pickle(
    #     "/Users/nlotan/code/university/SocialVec/auxiliary/users_with_over_200_DETAILS.pkl")
    
    popular_df = pd.read_pickle("https://www.dropbox.com/s/8w6m7o2qwfp3du1/users_with_over_200_DETAILS.pkl?dl=1")
    
    popular_df = popular_df[(popular_df['user_id'] != "nan") & (
        popular_df['user_id'] != "False") & (popular_df['user_id'] != "True") & (
        popular_df['followers_count'].isna() == False)]
    popular_df.user_id = popular_df.user_id.astype(int)
    popular_df.followers_count = popular_df.followers_count.astype(int)
    # link is the column with hyperlinks
    popular_df['link'] = popular_df['screen_name'].apply(make_clickable)
    
    wiki = pd.read_csv("https://www.dropbox.com/s/b4i77itlghso5fg/users_with_wikidata.csv.gz?dl=1",compression="gzip")
    wiki.user_id = wiki.user_id.astype(int)
    wiki['wikipedia'] = wiki['wikipedia'].apply(lambda link: f'<a target="_blank" href="{link}">wiki url</a>')
    
    popular_df = popular_df.merge(wiki, on="user_id",how="left")
    
    return popular_df

st.set_page_config(layout="wide")

popular_df = load_data()


for path, subdirs, files in os.walk("data"):
    for file in files:
        if file.endswith(".csv"):
            file_list.append(file)


selected_file = st.selectbox("select file", file_list)

df = pd.read_csv(os.path.join("data", selected_file))
cic_filter = st.slider("Filter users that appear less than:", 1, 30)
sort_pmi = st.selectbox("Sort PMI by:",['Accending','Decending'])

df.user2 = df.user2.astype(int)
df.count_in_class = df.count_in_class.astype(int)
df.drop(df.columns[df.columns.str.contains(
    'unnamed', case=False)], axis=1, inplace=True)
df.rename(columns={'user2': 'user_id'}, inplace=True)

merged_df = pd.merge(df, popular_df, on="user_id", how="left")

merged_df = merged_df[['category', 'pmi',
        'count_in_class',
        'user_id',
        'name',
        'screen_name',
        'description',
        'link',
        'followers_count',
        'wikipedia'
        ]]


merged_df.drop_duplicates(inplace=True)

merged_df = merged_df[merged_df['count_in_class'] >= cic_filter]
#df = 
if sort_pmi == "Accending":
    merged_df.sort_values(by=['pmi'], ascending=True, inplace=True)
else:
    merged_df.sort_values(by='pmi', ascending=False, inplace=True)
#st.write(df.to_html(escape=False)
st.write(merged_df.to_html(escape=False, index=False), unsafe_allow_html=True)

# st.dataframe(popular_df)
