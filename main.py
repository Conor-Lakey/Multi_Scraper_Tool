# Setup working environment
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep
import tkinter as tk
from random import randint
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# Setup Tkinter Instance
root = tk.Tk()
root.title('My Scraper Tool')
root.geometry('300x200')


# Runs the Box Office Mojo Scraper when button is clicked
def box_office_mojo():
    """Opens a new window for testing functionality"""

    mojo_movies = {}
    mojo_data_frames = []

    mojo_window = tk.Toplevel(root)
    mojo_window.title('Box Office Mojo Scraper')
    mojo_window.geometry('400x300')

    # TV Show Name Label
    movie_name_label = tk.Label(mojo_window, text='Movie Name: ')
    movie_name_label.pack()

    # TV Show Name Entry Box
    movie_name_entry = tk.Entry(mojo_window)
    movie_name_entry.pack()

    # TV Show ID Label
    movie_id_label = tk.Label(mojo_window, text='Movie ID: ')
    movie_id_label.pack()

    # TV Show ID Entry Box
    movie_id_entry = tk.Entry(mojo_window)
    movie_id_entry.pack()

    def print_movie_name():
        """Prints user input movie Name"""
        # Stores Movie details into Nested Dictionary
        movie_name = movie_name_entry.get()
        movie_id = movie_id_entry.get()
        movie_dict = {'name': movie_name, 'id': movie_id}
        mojo_movies[movie_name] = movie_dict

        # Clears Entry boxes for new data
        movie_name_entry.delete(0, 'end')
        movie_id_entry.delete(0, 'end')

        # Prints entered Movies for the User
        movies = tk.Label(mojo_window, text=f'{movie_name}')
        movies.pack()
        print(mojo_movies)

    def box_office_mojo_scraper():
        """Scrapes Box Office Data from BoxOfficeMojo with Pandas"""
        for i in mojo_movies:
            movie_name = i
            movie_id = mojo_movies[i]['id']

            url = f'https://www.boxofficemojo.com/release/{movie_id}/'
            df = pd.read_html(url)
            df = df[0]

            # Clean DataFrame
            del df['Estimated']
            df = df.replace({'\$': '', ',': ''}, regex=True)
            df['Date'] = df.replace(' ', '/', regex=True)
            df['Daily'] = pd.to_numeric(df['Daily'], downcast='float')
            df['Avg'] = pd.to_numeric(df['Avg'], downcast='float')
            df['To Date'] = pd.to_numeric(df['To Date'], downcast='float')

            # Renames Dataframe based on user input & saves to CSV. Adds to DataFrames list.
            df.name = movie_name
            mojo_data_frames.append(df)
            df.to_csv(f'{movie_name}_Box_Office_Data.csv', index=False, encoding="cp1252")

        # Opens new window stating that downloads are now finished.
        mojo_finished_window = tk.Toplevel(root)
        mojo_finished_window.title('Downloads Complete')
        finished = tk.Label(mojo_finished_window, text='Thank you, your downloads\n are now complete!')
        finished.pack()
        mojo_window.destroy()

    def save_xlsx(list_dfs):
        """Saves Data Frames in one Excel file, each in a unique sheet"""
        writer = pd.ExcelWriter(f'Merged_Box_Office_Data.xlsx', engine='openpyxl')
        for df in list_dfs:
            df.to_excel(writer, df.name, index=False)
        writer.save()

    def scrape_and_merge():
        """Combines IMDB Scraper Function and Save_xlsx Function into one"""
        box_office_mojo_scraper()
        save_xlsx(mojo_data_frames)

    # Button to run function which saves user input into Dictionaries
    save_data_button = tk.Button(mojo_window, text='Save Movie', command=print_movie_name)
    save_data_button.pack()

    # Button to start downloads once user has filled dictionary
    start_downloads_button = tk.Button(mojo_window, text='Start Downloads', command=scrape_and_merge)
    start_downloads_button.pack()

    # Label for Prints list of input TV Show Names
    list_label = tk.Label(mojo_window, text='\nSelected Movies: ')
    list_label.pack()


# Runs the IMDB Scraper when button is clicked
def imdb():
    """Opens a new window for testing functionality"""

    imdb_shows = {}
    imdb_data_frames = []

    imdb_window = tk.Toplevel(root)
    imdb_window.title('IMDB TV Show Scraper')
    imdb_window.geometry('400x300')

    # TV Show Name Label
    tv_show_name_label = tk.Label(imdb_window, text='TV Show Name: ')
    tv_show_name_label.pack()

    # TV Show Name Entry Box
    tv_show_name_entry = tk.Entry(imdb_window)
    tv_show_name_entry.pack()

    # TV Show ID Label
    tv_show_id_label = tk.Label(imdb_window, text='TV Show ID: ')
    tv_show_id_label.pack()

    # TV Show ID Entry Box
    tv_show_id_entry = tk.Entry(imdb_window)
    tv_show_id_entry.pack()

    # TV Show Seasons Label
    tv_show_seasons_label = tk.Label(imdb_window, text='Number of Seasons: ')
    tv_show_seasons_label.pack()

    # TV Show Seasons Entry Box
    tv_show_seasons_entry = tk.Entry(imdb_window)
    tv_show_seasons_entry.pack()

    def print_tv_show_name():
        """Prints user input TV Show Name"""
        # Stores TV Show details into Nested Dictionary
        show_name = tv_show_name_entry.get()
        show_id = tv_show_id_entry.get()
        show_seasons = tv_show_seasons_entry.get()
        show_dict = {'name': show_name, 'id': show_id, 'seasons': int(show_seasons)}
        imdb_shows[show_name] = show_dict

        # Clears Entry boxes for new data
        tv_show_name_entry.delete(0, 'end')
        tv_show_id_entry.delete(0, 'end')
        tv_show_seasons_entry.delete(0, 'end')

        # Prints entered TV Show Names for the User
        shows = tk.Label(imdb_window, text=f'{show_name}')
        shows.pack()
        print(imdb_shows)

    def imdb_scraper_loop():
        """IMDB Scraper Function for all Dictionary Values"""
        for i in imdb_shows:

            # initiate data storage
            titles_list = []
            years_list = []
            imdb_ratings_list = []
            votes_list = []
            seasons_list = []
            episodes_list = []
            plots_list = []

            tv_show_name = i
            tv_show_id = imdb_shows[i]['id']
            number_of_seasons = (imdb_shows[i]['seasons'])

            pages = np.arange(1, int(number_of_seasons + 1), 1)

            for season_number, page in enumerate(pages, 1):
                page = requests.get(f'https://www.imdb.com/title/{tv_show_id}/episodes?season={str(page)}')
                soup = BeautifulSoup(page.text, 'html.parser')
                episode_div = soup.find_all('div', class_='list_item')
                sleep(randint(2, 10))

                for episode_number, container in enumerate(episode_div, 1):
                    # Extract Season #
                    season = season_number
                    seasons_list.append(season)

                    # Extract Episode #
                    episode = episode_number
                    episodes_list.append(episode)

                    # Extract Episode Name
                    name = container.strong.a.text
                    titles_list.append(name)

                    # Extract Air Date
                    year = container.find('div', class_='airdate').text if container.find('div',
                                                                                          class_='airdate') else ''
                    years_list.append(year)

                    # Extract IMDB Rating
                    imdb_rating = container.find('span', class_='ipl-rating-star__rating').text \
                        if container.find('span', class_='ipl-rating-star__rating') else ''
                    imdb_ratings_list.append(imdb_rating)

                    # Extract # of Votes
                    vote = container.find('span', class_='ipl-rating-star__total-votes').text \
                        if container.find('span', class_='ipl-rating-star__total-votes') else ''
                    votes_list.append(vote)

                    # Extract Plot
                    plot = container.find('div', class_='item_description').text \
                        if container.find('div', class_='item_description') else ''
                    plots_list.append(plot)

            # Builds a Pandas Dataframe
            df = pd.DataFrame({
                'Episode': titles_list,
                'Air Date': years_list,
                'IMDB Rating': imdb_ratings_list,
                'Votes': votes_list,
                'Season': seasons_list,
                'Episode #': episodes_list,
                'Plot': plots_list
            })

            # Cleans DataFrame
            df['Air Date'] = df['Air Date'].str.strip().str.replace('.', '')
            df['Plot'] = df['Plot'].str.strip()
            df['Votes'] = df['Votes'].str.replace('(', '').str.replace(')', '').str.replace(',', '')

            df['Votes'] = pd.to_numeric(df['Votes'], downcast='float')
            df['Season'] = pd.to_numeric(df['Season'], downcast='float')
            df['Episode #'] = pd.to_numeric(df['Episode #'], downcast='float')
            df['IMDB Rating'] = pd.to_numeric(df['IMDB Rating'], downcast='float')

            # Renames Dataframe based on user input & saves to CSV. Adds to DataFrames list.
            df.name = tv_show_name
            imdb_data_frames.append(df)
            df.to_csv(f'{tv_show_name}.csv', index=False, encoding="cp1252")

        # Opens new window stating that downloads are now finished.
        imdb_finished_window = tk.Toplevel(root)
        imdb_finished_window.title('Downloads Complete')
        finished = tk.Label(imdb_finished_window, text='Thank you, your downloads\n are now complete!')
        finished.pack()
        imdb_window.destroy()

    def save_xlsx(list_dfs):
        """Saves Data Frames in one Excel file, each in a unique sheet"""
        writer = pd.ExcelWriter(f'merged_data.xlsx', engine='openpyxl')
        for df in list_dfs:
            df.to_excel(writer, df.name, index=False)
        writer.save()

    def scrape_and_merge():
        """Combines IMDB Scraper Function and Save_xlsx Function into one"""
        imdb_scraper_loop()
        save_xlsx(imdb_data_frames)

    # Button to run function which saves user input into Dictionaries
    save_data_button = tk.Button(imdb_window, text='Save TV Show', command=print_tv_show_name)
    save_data_button.pack()

    # Button to start downloads once user has filled dictionary
    start_downloads_button = tk.Button(imdb_window, text='Start Downloads', command=scrape_and_merge)
    start_downloads_button.pack()

    # Label for Prints list of input TV Show Names
    list_label = tk.Label(imdb_window, text='\nSelected TV Shows: ')
    list_label.pack()


# Label for Main Screen Scraper Choice
scraper_label = tk.Label(root, text='\nWhat Scraper would you like to use?\n')
scraper_label.pack()

# Button to initiate the Box Office Mojo Scraper Program
new_window_button = tk.Button(text='Box Office \nMojo Scraper', command=box_office_mojo)
new_window_button.pack()

# Label for Main Screen Scraper Choice
spacer_label = tk.Label(root, text=' ')
spacer_label.pack()

# Button to initiate the IMDB Scraper Program
new_window_button = tk.Button(text='IMDB \nTV Show Scraper', command=imdb)
new_window_button.pack()

root.mainloop()  # Runs Tkinter GUI
