# kinopoisk

data for db was parsed using unofficial kinopoisk API - https://kinopoiskapiunofficial.tech/

parsing is done manually in 3 stages - necessary utils and script are located in scripts&utils folder:

1) parse_movie.py - works in terminal, to get data from API for 20 movies (details of request seek at API documentation) - data from API is saved to disk as list of dicts

2) images_parse.py - works in terminal, list of movies is read from disk, then iterated, for each movie there is url for image, it is saved to disk

3) add_records_scrip.py - works in django shell to communicate with db directly, just copy the script to shell and execute -  it will load list of movies from disk, iterate over it and create model instance for each movie along with cover

4) there are two extra scripts - one to remove duplicates from db if there are any (key to duplicate is kinopoiskId) to be run in shell and one to parse description if there are None for initial parsing

the rest is quite straightforward django project:
views:
  - add_movie
  - show movies with filtering - each movie in list has link to more detailed view (see below)
  - show individual movie
  - search movies title and description and view results as list

