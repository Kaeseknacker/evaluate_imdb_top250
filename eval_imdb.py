import argparse
import pickle
import re
import statistics

import matplotlib.pyplot as plt
from tqdm import tqdm
from imdb import IMDb

from statistic_writer import StatisticWriter


def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def get_top250_movies(download_list):
    ia = IMDb()
    print(ia.get_movie_infoset())
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


def eval_years(top_movies, sw):
    sorted_movies_year = sorted(top_movies, key=lambda movie: movie['year'], reverse=True)

    years = [movie['year'] for movie in sorted_movies_year]
    print("mean release year =", statistics.mean(years))
    print("median release year =", statistics.median(years))

    newest_movies = [f"{movie}, {movie['year']}" for movie in sorted_movies_year[:3]]
    oldest_movies = [f"{movie}, {movie['year']}" for movie in sorted_movies_year[:-4:-1]]
    sw.set_movie_years_informations(newest_movies, oldest_movies)


def eval_runtime(top_movies, sw):
    sorted_movies = sorted(top_movies, key=lambda movie: parse_runtime(movie['tech']['runtime'][0]), reverse=True)

    runtimes = [parse_runtime(movie['tech']['runtime'][0]) for movie in sorted_movies]
    print("mean runtime =", statistics.mean(runtimes), "min")
    print("median runtime =", statistics.median(runtimes), "min")

    longest_movies = [f"{movie}, {parse_runtime(movie['tech']['runtime'][0])} min" for movie in sorted_movies[:3]]
    shortest_movies = [f"{movie}, {parse_runtime(movie['tech']['runtime'][0])} min" for movie in sorted_movies[:-4:-1]]
    sw.set_movie_runtime_informations(longest_movies, shortest_movies)


def eval_votes(top_movies, sw):
    sorted_movies = sorted(top_movies, key=lambda movie: movie['votes'], reverse=True)

    most_votes_movies = [f"{movie}, {movie['votes']} votes" for movie in sorted_movies[:3]]
    less_votes_movies = [f"{movie}, {movie['votes']} votes" for movie in sorted_movies[:-4:-1]]
    sw.set_movie_votes_informations(most_votes_movies, less_votes_movies)

    plt.clf()
    #plt.hist([m['votes'] for m in top_movies], bins=30, color="#179c7d", edgecolor="#000000")
    #plt.plot([i for i in range(1, 251)], [m['votes'] for m in sorted_movies])
    #plt.plot([i for i in range(1, 251)], [m['votes'] for m in sorted(top_movies, key=lambda movie: movie['year'])])
    tmp = sorted(top_movies, key=lambda movie: movie['year'])
    # TODO: mean und std-err für jedes Jahr berechnen
    year_dict = {m['year']: [] for m in tmp}
    for m in tmp:
        year_dict[m['year']].append(m['votes'])
    print(year_dict)
    x = year_dict.keys()
    y = [statistics.mean(v) for v in year_dict.values()]
    yerr = [statistics.stdev(v) if len(v) > 1 else 0 for v in year_dict.values()]
    plt.errorbar(x=x, y=y, yerr=yerr, fmt='-o')
    #plt.plot([m['year'] for m in tmp], [m['votes'] for m in tmp], 'x-')
    plt.ylabel('votes')
    plt.xlabel("year")
    plt.title("votes per year")
    plt.show()

    plt.clf()
    tmp = sorted(top_movies, key= lambda movie: movie['top 250 rank'])
    plt.plot([m['top 250 rank'] for m in tmp], [m['votes'] for m in tmp], 'x')
    plt.ylabel('votes')
    plt.xlabel("movie rank")
    plt.title("votes per movie")
    plt.show()

    plt.clf()
    plt.boxplot([m['votes'] for m in top_movies])
    plt.show()

    plt.clf()
    plt.hist2d([m['year'] for m in tmp], [m['votes'] for m in tmp], bins=(10, 20), cmap='hot')
    plt.show()


def main(args):

    top_movies = get_top250_movies(args['download_list'])

    sw = StatisticWriter()

    print(top_movies[0].keys())
    #for movie in top_movies:
        #print(movie['title'])
    #ia = IMDb()
    #the_matrix = ia.get_movie('0133093')
    #print(the_matrix.keys())
    #for i in the_matrix.items():
    #    print(i)
    #print(the_matrix.items())

    eval_years(top_movies, sw)

    eval_runtime(top_movies, sw)

    eval_votes(top_movies, sw)

    sw.write_statistics()


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
# [ ] Dekaden Histogramm
# [ ] filmeinteilung nach genres
# [ ] Sortierung nach Top1000 Voters
# [ ] Sortierung nach Male/Female
# [ ] Abweichung zwischen normalem Rating und Rating der Top1000 Users. Wo gibt es die größten Differenzen?

# Einteilung in new >= 1970 > old
