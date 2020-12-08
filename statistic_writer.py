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

    def write_statistics(self):
        mdfile = MdUtils(file_name="Statistics", title="IMDb Top 250 Statistics")
        # TODO: Write Date

        mdfile.new_header(level=1, title="Evaluate movie years")
        mdfile.new_paragraph("Newest Movies:")
        mdfile.new_list(self.newest_movies, marked_with='1')
        mdfile.new_paragraph("Oldest Movies:")
        mdfile.new_list(self.oldest_movies, marked_with='1')

        mdfile.new_header(level=1, title="Evaluate movie runtimes")
        mdfile.new_paragraph("Longest Movies:")
        mdfile.new_list(self.longest_movies, marked_with='1')
        mdfile.new_paragraph("Shortest Movies:")
        mdfile.new_list(self.shortest_movies, marked_with='1')

        mdfile.create_md_file()
