import argparse
import pickle
import re

from tqdm import tqdm
from imdb import IMDb


def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def get_top250_movies(download_list):
    if download_list:
        ia = IMDb()
        top_movies = ia.get_top250_movies()

        for movie in tqdm(top_movies):
            ia.update(movie, ['technical'])

        # save for next time
        save_object(top_movies, 'top_movies.pkl')
        return top_movies
    else:
        with open('top_movies.pkl', 'rb') as f:
            top_movies = pickle.load(f)
            return top_movies


def parse_runtime(runtime_str):
    x = re.search("[(][0-9]+[ ][m][i][n][)]", runtime_str)
    if x is None:
        x = re.search("[0-9]+[ ][m][i][n]", runtime_str)
    y = re.search("[0-9]+", x.group())
    return y.group()


def main(args):

    # create an instance of the IMDb class
    ia = IMDb()

    # get a movie and print its director(s)
    #the_matrix = ia.get_movie('0133093')
    #for director in the_matrix['directors']:
    #    print(director['name'])

    # show all information that are currently available for a movie
    #print(sorted(the_matrix.keys()))

    # show all information sets that can be fetched for a movie
    print(ia.get_movie_infoset())

    # update a Movie object with more information
    #ia.update(the_matrix, ['technical'])
    # show which keys were added by the information set
    #print(the_matrix.infoset2keys['technical'])
    # print one of the new keys
    #print(the_matrix.get('tech'))

    top_movies = get_top250_movies(args['download_list'])

    for movie in top_movies:
        tech = movie.get('tech')
        if tech is not None:
            #print(movie, parse_runtime(tech['runtime'][0]), movie['votes'])
            pass

    sorted_movies = sorted(top_movies, key=lambda movie: movie['year'], reverse=True)
    for movie in sorted_movies:
        print(movie, movie['year'], movie['votes'])

def parse_args():
    parser = argparse.ArgumentParser(description='do some imdb stuff',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--download_list', help='Download new top 250 list from IMDb. Otherwise use local .pkl file',
                        action='store_true', default=False)

    args = vars(parser.parse_args())
    return args


if __name__ == "__main__":
    main(parse_args())

# TODO:
# github repo erstellen
# Ergebnisse in Markdown schreiben
# Statistiken:
# [ ] ältester/neuester Film
# [ ] durchschnitts Erscheinungsjahr
# [ ] längster/kürzester Film
# [ ] durchschnittliche/median Laufzeit
# [ ] top 3 filme / votes
# [ ] bottom 3 filme / votes


# ältester Film: The Kid 1921
# Einteilung in new >= 1970 > old
