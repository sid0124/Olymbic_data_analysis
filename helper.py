import numpy as np
def medal_tally(df):
    medal_tally = df.drop_duplicates(
        subset=['Team', "NOC", "Games", "Games", "Year", "City", "Sport", "Event", "Medal"])
    medal_tally=medal_tally.groupby("region").sum()[['Gold', 'Silver', 'Bronze']].sort_values("Gold",
                                                                                  ascending=False).reset_index().head()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally['Gold'] = medal_tally['Gold'].astype(int)
    medal_tally['Silver'] = medal_tally['Silver'].astype(int)
    medal_tally['Bronze'] = medal_tally['Bronze'].astype(int)
    medal_tally['Total'] = medal_tally['Total'].astype(int)

    return medal_tally

def contry_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, "Overall")
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, "Overall")
    return  years,country





def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x

def data_over_time(df,col):
    nation_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values("Year")
    nation_over_time.rename(columns={"Year": "Editions", "count": col}, inplace=True)

    return nation_over_time


def most_successful(df, sports):
    temp_df = df.dropna(subset=['Medal'])

    if sports != "Overall":
        temp_df = temp_df[temp_df['Sport'] == sports]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on="Name", right_on="Name", how="left")[["Name","count",'Sport','region']].drop_duplicates()
    x.rename({"Count":'Medals'})
    return x

def yearwise_model_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby("Year").count()['Medal'].reset_index()
    return final_df

def country_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    new_df = temp_df[temp_df['region'] == country]
    pt =new_df.pivot_table(index="Sport", columns="Year", values="Medal",aggfunc="count").fillna(0)
    return pt

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on="Name", right_on="Name", how="left")[["Name","count",'Sport']].drop_duplicates()
    x.rename({"Count":'Medals'},inplace=True)
    return x

def wight_v_heght(df,sport):
    athletes_df = df.drop_duplicates(subset=['Name', 'region'])
    athletes_df['Medal'].fillna("No medal", inplace=True)
    if sport != 'Overall':
        temp_df = athletes_df[athletes_df['Sport']==sport]
        return temp_df
    else:
        return athletes_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final


