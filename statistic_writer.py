from mdutils.mdutils import MdUtils

class StatisticWriter:
    def __init__(self):
        pass

    def set_movie_years_informations(self, newest_movies, oldest_movies):
        self.newest_movies = newest_movies
        self.oldest_movies = oldest_movies

    def set_movie_runtime_informations(self, longest_movies, shortest_movies):
        self.longest_movies = longest_movies
        self.shortest_movies = shortest_movies

    def set_movie_votes_informations(self, most_votes_movies, less_votes_movies):
        self.most_votes_movies = most_votes_movies
        self.less_votes_movies = less_votes_movies

    def write_statistics(self):
        mdfile = MdUtils(file_name="Statistics", title="IMDb Top 250 Statistics")
        # TODO: Write Date

        mdfile.new_header(level=1, title="Movie years")
        mdfile.new_paragraph("Newest Movies:")
        mdfile.new_list(self.newest_movies, marked_with='1')
        mdfile.new_paragraph("Oldest Movies:")
        mdfile.new_list(self.oldest_movies, marked_with='1')

        mdfile.new_header(level=1, title="Movie runtimes")
        mdfile.new_paragraph("Longest Movies:")
        mdfile.new_list(self.longest_movies, marked_with='1')
        mdfile.new_paragraph("Shortest Movies:")
        mdfile.new_list(self.shortest_movies, marked_with='1')

        mdfile.new_header(level=1, title="Movie votes")
        mdfile.new_paragraph("Movies with most votes:")
        mdfile.new_list(self.most_votes_movies, marked_with='1')
        mdfile.new_paragraph("Movies with fewest votes:")
        mdfile.new_list(self.less_votes_movies, marked_with='1')

        mdfile.new_line(mdfile.new_inline_image(text='Votes as boxplot', path='./figs/votes_boxplot.png'))

        mdfile.create_md_file()
