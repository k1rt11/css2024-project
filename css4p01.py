# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 14:21:29 2024

@author: Kirti
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file = pd.read_csv("movie_dataset.csv", index_col = 0)

file.columns = file.columns.str.replace(" ", "")

#show all rows and columns
#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)

#remove duplicates
file.drop_duplicates(inplace = True)  #there are no duplicates 

#replace empty values with mean of column or drop rows- the only columns with empty values are 'Revenue' and 'Metascore'

mean_revenue = file['Revenue(Millions)'].mean()
file['Revenue(Millions)'].fillna(mean_revenue, inplace = True)

#cannot drop empty metascore rows because then the number of movies released in 2016 and the answer of some other questions is incorrect 
mean_metascore = file['Metascore'].mean()
file['Metascore'].fillna(mean_metascore, inplace = True)

print(file.info())
print(file.describe())
print(file)


highest_rated_movie = file[file['Rating'] == file['Rating'].max()]
print("\nHighest rated movie: ", highest_rated_movie['Title'].values[0])

avg_movie_revenue = file['Revenue(Millions)'].mean()
print("\nAverage movie revenue(Millions): ", avg_movie_revenue)

df_2015_to_2017 = file[(file['Year'] >= 2015) & (file['Year'] <= 2017)]
avg_movie_revenue_2015_to_2017 = df_2015_to_2017['Revenue(Millions)'].mean()
print("\nAverage movie revenue(Millions) from 2015 to 2017: ", avg_movie_revenue_2015_to_2017)

movies_2016_df = file[file['Year'] == 2016]
num_movies_2016 = len(movies_2016_df)
print("\nNumber of movies released in 2016: ", num_movies_2016)

christopher_nolan_movies_df = file[file['Director'] == "Christopher Nolan"]
print("\nNumber of Christopher Nolan movies: ", len(christopher_nolan_movies_df))      

movies_rating_atleast_8_df = file[file['Rating'] >= 8.0] 
print("\nNumber of movies with a rating of atleast 8.0: ", len(movies_rating_atleast_8_df))  

print("\nMedian rating of Christopher Nolan movies: ", christopher_nolan_movies_df['Rating'].median())                           

year_group = file.groupby('Year')
mean_ratings = year_group['Rating'].mean()
highest_avg_rating_year_idx = mean_ratings.idxmax()
print("\nYear with highest average rating: ", highest_avg_rating_year_idx)

movies_2006_df = file[file['Year'] == 2006]
num_movies_2006 = len(movies_2006_df)
percent_increase = ((num_movies_2016 - num_movies_2006)/num_movies_2006) * 100
print("\nPercentage increase in number of movies made between 2006 and 2016: ", percent_increase)

#put all actors of all movies together in a single string separated by a comma
all_actors = ', '.join(file['Actors'])


actors_dict = {} #dictionary to store actors and the number of movies they occured in

for movie_actors in file['Actors']:
    #split actors by a comma to get a list of all actors in the specific movie
    movie_actors_list = movie_actors.split(', ')
    
    for actor in movie_actors_list:
        #for each new actor in the dictionary, add one to the count - the default if the actor is new is 0
        actors_dict[actor] = actors_dict.get(actor, 0) + 1

print("\nThe most common actor in all the movies: ", max(actors_dict, key = actors_dict.get))

genres_set = set() #creating a set for genres

for movie_genre in file['Genre']:
    movie_genres_list = movie_genre.split(",")
    
    for genre in movie_genres_list:
        genres_set.add(genre)
print("\nNumber of unique genres in the dataset: ", len(genres_set))

sns.pairplot(file)

#correlation
# Select only numeric columns for correlation analysis
numeric_columns = file.select_dtypes(include=['number'])

plt.figure(figsize=(12,9))
sns.heatmap(numeric_columns.corr(),annot=True,linewidths=2)

#number of movies per year
movies_per_year = file['Year'].value_counts().sort_index()

#bar graph
plt.figure(figsize=(12, 6))
movies_per_year.plot(kind='bar', color='orange')
plt.xlabel('Year')
plt.ylabel('Number of movies')
plt.title('Number of movies per year')
plt.show()

#revenue per year
revenue_per_year = year_group['Revenue(Millions)'].sum()

#bar graph
plt.figure(figsize=(12, 6))
movies_per_year.plot(kind='bar', color='blue')
plt.xlabel('Year')
plt.ylabel('Revenue (Millions)')
plt.title('Revenue (Millions) per year')
plt.show()