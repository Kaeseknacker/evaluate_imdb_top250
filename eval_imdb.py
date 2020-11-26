import argparse
import pickle
import re
import statistics

import matplotlib.pyplot as plt
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
    return int(y.group())


def eval_years(top_movies):
    sorted_movies_year = sorted(top_movies, key=lambda movie: movie['year'], reverse=True)
    print("Newest Movies:")
    for movie in sorted_movies_year[:3]:
        print(movie, movie['year'])
    print("Oldest Movies:")
    for movie in sorted_movies_year[:-4:-1]:
        print(movie, movie['year'])
    years = [movie['year'] for movie in sorted_movies_year]
    print("mean release year =", statistics.mean(years))
    print("median release year =", statistics.median(years))


def eval_runtime(top_movies):
    sorted_movies = sorted(top_movies, key=lambda movie: parse_runtime(movie['tech']['runtime'][0]), reverse=True)
    print("Longest Movies:")
    for movie in sorted_movies[:3]:
        print(movie, parse_runtime(movie['tech']['runtime'][0]))
    print("Shortest Movies:")
    for movie in sorted_movies[:-4:-1]:
        print(movie, parse_runtime(movie['tech']['runtime'][0]), "min")
    runtimes = [parse_runtime(movie['tech']['runtime'][0]) for movie in sorted_movies]
    print("mean runtime =", statistics.mean(runtimes), "min")
    print("median runtime =", statistics.median(runtimes), "min")


def eval_votes(top_movies):

    sorted_movies = sorted(top_movies, key=lambda movie: movie['votes'], reverse=True)
    print("Most votes:")
    for movie in sorted_movies[:3]:
        print(movie, movie['votes'])
    print("less votes:")
    for movie in sorted_movies[:-4:-1]:
        print(movie, movie['votes'])

    plt.clf()
    #plt.hist([m['votes'] for m in top_movies], bins=30, color="#179c7d", edgecolor="#000000")
    #plt.plot([i for i in range(1, 251)], [m['votes'] for m in sorted_movies])
    #plt.plot([i for i in range(1, 251)], [m['votes'] for m in sorted(top_movies, key=lambda movie: movie['year'])])
    tmp = sorted(top_movies, key=lambda movie: movie['year'])
    plt.plot([m['year'] for m in tmp], [m['votes'] for m in tmp], 'x-')
    plt.ylabel('votes')
    plt.xlabel("year")
    plt.title("votes per year")
    plt.show()

    plt.clf()
    tmp = sorted(top_movies, key= lambda movies: movie['top 250 rank'])
    plt.plot([m['top 250 rank'] for m in tmp], [m['votes'] for m in tmp], 'x')
    plt.ylabel('votes')
    plt.xlabel("movie rank")
    plt.title("votes per movie")
    plt.show()

    plt.clf()
    plt.boxplot([m['votes'] for m in top_movies])
    plt.show()


def main(args):

    top_movies = get_top250_movies(args['download_list'])

    print(top_movies[0].keys())

    eval_years(top_movies)

    eval_runtime(top_movies)

    eval_votes(top_movies)
    

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
# Ergebnisse in Markdown schreiben
# Statistiken:
# [x] ältester/neuester Film
# [x] durchschnitts Erscheinungsjahr
# [x] längster/kürzester Film
# [x] durchschnittliche/median Laufzeit
# [x] top 3 filme / votes
# [x] bottom 3 filme / votes
# [x] votes diagram

# ältester Film: The Kid 1921
# Einteilung in new >= 1970 > old
