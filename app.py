import streamlit as st
import pandas as pd
import preprocessor,helper
from helper import medal_tally, most_successful
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


df = pd.read_csv("athlete_events.csv")
region = pd.read_csv("noc_regions.csv")

df_1 = preprocessor.preprocess(df, region)
st.sidebar.header('Olympics Analysis')
user_choice = st.sidebar.radio(
    'Select options',
    ('Medal Tally','Over-all Analysis','Country-wise Analysis','Athlete wise Analysis')
)

if user_choice == "Medal Tally":
    st.sidebar.header("Medal Tally")
    years,country = helper.contry_year_list(df_1)
    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country",country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")


    medal_tally= helper.fetch_medal_tally(df_1,selected_year,selected_country)
    st.dataframe(medal_tally)

if user_choice == "Over-all Analysis":
    editions = df_1["Year"].unique().shape[0] - 1
    athletes = df_1["Name"].unique().shape[0]
    cities = df_1["City"].unique().shape[0]
    sports = df_1["Sport"].unique().shape[0]
    events = df_1["Event"].unique().shape[0]
    nations = df_1["region"].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3 :
        st.header("Sports")
        st.title(sports)

    col4,col5,col6 = st.columns(3)
    with col4 :
        st.header("Nation")
        st.title(nations)
    with col5:
        st.header("Events")
        st.title(events)
    with col6:
        st.header("Athletes")
        st.title(athletes)

    nation_over_time = helper.data_over_time(df_1,"region")
    st.title("Participating Nation Over The Time")
    fig = px.line(nation_over_time, x="Editions", y="region")
    st.plotly_chart(fig)

    event_over_time = helper.data_over_time(df_1, "Event")
    st.title("Events Over The Time")
    fig = px.line(event_over_time, x="Editions", y="Event")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df_1, "Name")
    st.title("Athletes Over The Time")
    fig = px.line(athletes_over_time, x="Editions", y="Name")
    st.plotly_chart(fig)

    st.title("No. of event over time(Every Sports)")
    fig,ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Sport', 'Year', 'Event'])
    heatmap_data = x.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count").fillna(0).astype(int)
    sns.heatmap(heatmap_data, annot=True, ax=ax)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sports_list = df_1['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,"Overall")
    selected_sports = st.selectbox("select sports", sports_list)
    most_successful_athletes = helper.most_successful(df_1,selected_sports)
    st.table(most_successful_athletes)

if user_choice == "Country-wise Analysis":
    st.sidebar.title("Country-Wise Analysis")
    country_list = df_1['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox("Select the country", country_list)
    country_df = helper.yearwise_model_tally(df_1,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country+" Medal tally over the years")
    st.plotly_chart(fig)

    pt = helper.country_heatmap(df_1,selected_country)
    st.title(selected_country + " excels in the following sports")
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(pt, annot=True, ax=ax)
    st.pyplot(fig)

    st.title("Top 10 Athletes in "+selected_country)
    top_10_athletes= helper.most_successful_countrywise(df_1,selected_country )
    st.table(top_10_athletes)

if user_choice =='Athlete wise Analysis':
    athletes_df = df_1.drop_duplicates(subset=['Name', 'region'])
    x1 = athletes_df['Age'].dropna()
    x2 = athletes_df[athletes_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athletes_df[athletes_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athletes_df[athletes_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ["Overall", "Gold Medalist", "Silver medalist", "Bronze Medalist"],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height =800)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        athlete_df = df_1.drop_duplicates(subset=['Name', 'region'])

        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    
    sports_list = df_1['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, "Overall")
    st.title("Weight vs Height")
    selected_sports = st.selectbox("select sports", sports_list)
    temp_df= helper.wight_v_heght(df_1,selected_sports)
    fig,ax = plt.subplots(figsize=(10,10))
    ax = sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df_1)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
