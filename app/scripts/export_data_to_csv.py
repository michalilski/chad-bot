import csv
import random
from datetime import date, datetime, time, timedelta

from app.settings import PROJECT_PATH

random.seed(42)

MOVIES_LIMIT = 100
TARGET_YEARS = {"2017", "2018", "2019"}

START_SCHEDULE_DAY = date(2023, 7, 1)
END_SCHEDULE_DAY = date(2023, 8, 1)
STARTING_HOUR = 8
FINAL_HOUR = 22
HOUR_GAP = 2


def select_movies(path):
    movies = {}
    with open(path / "title.basics.tsv") as fd:
        reader = csv.reader(fd, delimiter="\t", quotechar='"')
        _ = next(reader)
        for line in reader:
            if line[1] == "movie" and line[5] in TARGET_YEARS and line[8] != "\\N":
                if "," in line[8]:
                    line[8] = " ".join(line[8].split(","))
                movies[line[0]] = {"title": line[2], "year": line[5], "genre": line[8]}
            if len(movies) == MOVIES_LIMIT:
                return movies
    return movies


def match_director(path, movies):
    selected_ids = set(movies.keys())
    name_ids = {}
    with open(path / "title.crew.tsv") as fd:
        reader = csv.reader(fd, delimiter="\t", quotechar='"')
        _ = next(reader)
        for line in reader:
            if line[0] in selected_ids:
                if "," in line[1]:
                    line[1] = line[1].split(",")[0]
                name_ids[line[0]] = line[1]

    name_ids_keys = set(name_ids.values())
    names = {}
    with open(path / "name.basics.tsv") as fd:
        reader = csv.reader(fd, delimiter="\t", quotechar='"')
        _ = next(reader)
        for line in reader:
            if line[0] in name_ids_keys:
                names[line[0]] = line[1]

    for idx, movie in movies.items():
        movie["director"] = names[name_ids[idx]]
    return movies


def generate_schedule(movie_ids):
    schedule = []
    samples_per_day = int((FINAL_HOUR + HOUR_GAP - STARTING_HOUR) / 2)
    for n in range(int((END_SCHEDULE_DAY - START_SCHEDULE_DAY).days)):
        current_date = START_SCHEDULE_DAY + timedelta(n)
        sampled_movies = random.sample(movie_ids, samples_per_day)
        for movie, hour in zip(sampled_movies, range(STARTING_HOUR, FINAL_HOUR + HOUR_GAP, HOUR_GAP)):
            schedule.append((movie, datetime.combine(date=current_date, time=time(hour=hour))))
    return schedule


def export_movies_to_csv(path, movies):
    with open(path / "movies.csv", "w+") as file:
        columns = ["imdb_id", "title", "director", "year", "genre"]
        writer = csv.writer(file)
        writer.writerow(columns)
        for idx, movie in movies.items():
            writer.writerow((idx, movie["movie_title"], movie["director"], movie["year"], movie["movie_genre"]))


def export_schedule_to_csv(path, schedule):
    with open(path / "movie_shows.csv", "w+") as file:
        columns = ["movie_id", "show_time"]
        writer = csv.writer(file)
        writer.writerow(columns)
        for show in schedule:
            writer.writerow(show)


def export():
    # files downloaded from https://datasets.imdbws.com/
    source_data_path = PROJECT_PATH / "data" / "raw_imdb"
    target_data_path = PROJECT_PATH / "data" / "csv"

    selected_movies = select_movies(source_data_path)
    selected_movies = match_director(source_data_path, selected_movies)
    schedule = generate_schedule(list(selected_movies.keys()))

    export_movies_to_csv(target_data_path, selected_movies)
    export_schedule_to_csv(target_data_path, schedule)


if __name__ == "__main__":
    export()
