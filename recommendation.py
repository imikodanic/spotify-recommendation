from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
import pandas


def scale_music_features(dataframe):
    scaler = MinMaxScaler()
    music_features = dataframe[['Danceability', 'Energy', 'Key',
                                'Loudness', 'Mode', 'Speechiness', 'Acousticness',
                                'Instrumentalness', 'Liveness', 'Valence', 'Tempo']].values
    return scaler.fit_transform(music_features)


def calculate_weighted_popularity(release_date):
    # Convert the release date to datetime object
    release_date = datetime.strptime(release_date, '%Y-%m-%d')

    # Calculate the time span between release date and today's date
    time_span = datetime.now() - release_date

    # Calculate the weighted popularity score based on time span (e.g., more recent releases have higher weight)
    weight = 1 / (time_span.days + 1)
    return weight


def content_based_recommendations(input_song_name, dataframe, num_recommendations=5):
    if input_song_name not in dataframe['Track Name'].values:
        print(f"'{input_song_name}' not found in the dataset. Please enter a valid song name.")
        return

    music_features_scaled = scale_music_features(dataframe)

    # Get the index of the input song in the music DataFrame
    input_song_index = dataframe[dataframe['Track Name'] == input_song_name].index[0]

    # Calculate the similarity scores based on music features (cosine similarity)
    similarity_scores = cosine_similarity([music_features_scaled[input_song_index]], music_features_scaled)

    # Get the indices of the most similar songs
    similar_song_indices = similarity_scores.argsort()[0][::-1][1:num_recommendations + 1]

    # Get the names of the most similar songs based on content-based filtering
    content_based_songs = dataframe.iloc[similar_song_indices][
        ['Track Name', 'Artists', 'Album Name', 'Release Date', 'Popularity']]

    return content_based_songs


def hybrid_recommendations(input_song_name, dataframe, num_recommendations=5, alpha=0.5):
    if input_song_name not in dataframe['Track Name'].values:
        print(f"'{input_song_name}' not found in the dataset. Please enter a valid song name.")
        return

    # Get content-based recommendations
    content_based_rec = content_based_recommendations(input_song_name, dataframe, num_recommendations)

    # Get the popularity score of the input song
    popularity_score = dataframe.loc[dataframe['Track Name'] == input_song_name, 'Popularity'].values[0]

    # Calculate the weighted popularity score
    weighted_popularity_score = popularity_score * calculate_weighted_popularity(
        dataframe.loc[dataframe['Track Name'] == input_song_name, 'Release Date'].values[0])

    # Combine content-based and popularity-based recommendations based on weighted popularity

    new_song_row = {
        'Track Name': input_song_name,
        'Artists': dataframe.loc[dataframe['Track Name'] == input_song_name, 'Artists'].values[0],
        'Album Name': dataframe.loc[dataframe['Track Name'] == input_song_name, 'Album Name'].values[0],
        'Release Date': dataframe.loc[dataframe['Track Name'] == input_song_name, 'Release Date'].values[0],
        'Popularity': weighted_popularity_score
    }
    recommendation_songs = pandas.concat([content_based_rec, pandas.DataFrame([new_song_row])], ignore_index=True)

    # Sort the hybrid recommendations based on weighted popularity score
    recommendation_songs = recommendation_songs.sort_values(by='Popularity', ascending=False)

    # Remove the input song from the recommendations
    recommendation_songs = recommendation_songs[recommendation_songs['Track Name'] != input_song_name]

    return recommendation_songs
