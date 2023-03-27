# File: objecttier.py
#
# objecttier
#
# Builds Movie-related objects from data retrieved through
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:

  def __init__(self, id, title, ryear):
    self._Movie_ID = id
    self._Title = title
    self._Release_Year = ryear

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year


##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating:

  def __init__(self, id, title, ryear, nrev, avgr):
    self._Movie_ID = id
    self._Title = title
    self._Release_Year = ryear
    self._Num_Reviews = nrev
    self._Avg_Rating = avgr

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year

  @property
  def Num_Reviews(self):
    return self._Num_Reviews

  @property
  def Avg_Rating(self):
    return self._Avg_Rating


##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:

  def __init__(self, id, title, rdate, rtime, lang, bud, rev, nrev, avg, tag,
               gen, prod):
    self._Movie_ID = id
    self._Title = title
    self._Release_Date = rdate
    self._Runtime = rtime
    self._Original_Language = lang
    self._Budget = bud
    self._Revenue = rev
    self._Num_Reviews = nrev
    self._Avg_Rating = avg
    self._Tagline = tag
    self._Genres = gen
    self._Production_Companies = prod

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Date(self):
    return self._Release_Date

  @property
  def Runtime(self):
    return self._Runtime

  @property
  def Original_Language(self):
    return self._Original_Language

  @property
  def Budget(self):
    return self._Budget

  @property
  def Revenue(self):
    return self._Revenue

  @property
  def Num_Reviews(self):
    return self._Num_Reviews

  @property
  def Avg_Rating(self):
    return self._Avg_Rating

  @property
  def Tagline(self):
    return self._Tagline

  @property
  def Genres(self):
    return self._Genres

  @property
  def Production_Companies(self):
    return self._Production_Companies


##################################################################
#
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
  query = "Select count(Movie_ID) from Movies"

  # Execute the query and get the count of movies
  result = datatier.select_one_row(dbConn, query)

  # Check if result is None
  if (result is None):
    # Return -1 if an error occurred
    return -1

  # Return the count of movies
  return result[0]


##################################################################
#
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
  query = "Select count(Rating) from Ratings"

  # Execute the query and get the count of reviews
  result = datatier.select_one_row(dbConn, query)

  # Check if result is None
  if (result is None):
    # Return -1 if an error occurred
    return -1

  # Return the count of reviews
  return result[0]


##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by name;
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
  # Construct the query to get movies that match the given pattern
  query = "Select Movie_ID, Title,  strftime('%Y',Release_Date) from Movies where Title like ? order by Movie_ID asc"

  # Execute the query and get the results
  result = datatier.select_n_rows(dbConn, query, [pattern])

  # Create a list of Movie objects from the results
  c = []
  for r in result:
    movieObject = Movie(r[0], r[1], r[2])
    c.append(movieObject)

  # Return the list of Movie objects
  return c

##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):

  # SQL query to retrieve details about the given movie
  query1 = "SELECT Movies.Movie_ID, Movies.Title, date(Movies.Release_Date), Movies.Runtime, Movies.Original_Language, Movies.Budget, Movies.Revenue, COUNT(Ratings.Movie_ID) AS Review_Count, AVG(Ratings.Rating) AS Avg_Rating,  Movie_Taglines.Tagline FROM Movies LEFT JOIN Movie_Taglines ON Movies.Movie_ID = Movie_Taglines.Movie_ID LEFT JOIN Ratings ON Movies.Movie_ID = Ratings.Movie_ID WHERE Movies.Movie_ID = ? GROUP BY Movies.Movie_ID, Movies.Release_Date, Movies.Runtime, Movies.Original_Language, Movies.Revenue, Movie_Taglines.Tagline"

  # SQL query to retrieve genres for the given movie
  query2 = "SELECT Genres.Genre_Name FROM Genres JOIN Movie_Genres ON Genres.Genre_ID = Movie_Genres.Genre_ID WHERE Movie_Genres.Movie_ID = ?;"

  # SQL query to retrieve production companies for the given movie
  query3 = "SELECT DISTINCT Companies.Company_Name FROM Companies JOIN Movie_Production_Companies ON Companies.Company_ID = Movie_Production_Companies.Company_ID WHERE Movie_Production_Companies.Movie_ID = ?;"

  # Retrieve the details of the given movie
  result1 = datatier.select_one_row(dbConn, query1, [movie_id])

  # Retrieve the genres of the given movie
  result2 = datatier.select_n_rows(dbConn, query2, [movie_id])

  # Retrieve the production companies of the given movie
  result3 = datatier.select_n_rows(dbConn, query3, [movie_id])

  # Return None if no movie was found with the given id
  if(result1 == ()):
    return None

  # Retrieve genres and production companies for the movie
  a = []
  b = []
  for r in result2:
    a.append(r[0])
  a.sort()
  for r in result3:
    b.append(r[0])
  b.sort()

  # Create a MovieDetails object and return it
  detailObject = MovieDetails(result1[0], result1[1], result1[2], result1[3], result1[4], result1[5], result1[6], result1[7], 0 if(result1[8] is None) else result1[8], '' if(result1[9] is None) else result1[9], a, b)
  return detailObject


##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
  # SQL query to select movies based on average rating and minimum number of reviews
  query = "SELECT Movies.Movie_ID, Movies.Title, strftime('%Y',Movies.Release_Date), AVG(Ratings.Rating) AS Avg_Rating, count(Ratings.Movie_ID) FROM Movies JOIN Ratings ON Movies.Movie_ID = Ratings.Movie_ID group by Ratings.Movie_ID having count(Ratings.Movie_ID) >= ? order by Avg_Rating desc limit ?"
  # Selecting n rows from the database that match the query criteria
  result = datatier.select_n_rows(dbConn, query, [min_num_reviews, N])
  # Creating a list of MovieRating objects and returning the list
  c = []
  for r in result:
    numObject = MovieRating(r[0],r[1], r[2], r[4], r[3])
    c.append(numObject)
  return c  

##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
  # SQL query to check if the movie exists in the database
  query1 = "Select Movie_ID from Movies where Movie_ID = ?"
  # Executing the query to check if the movie exists
  result1 = datatier.select_one_row(dbConn, query1, [movie_id])
  # If the movie does not exist, return 0
  if len(result1) == 0:
    return 0
  # SQL query to insert the review into the database
  query2 = "Insert into Ratings (Movie_ID, Rating) Values(?,?)"
  # Executing the query to insert the review into the database
  result2 = datatier.perform_action(dbConn, query2, [movie_id, rating])
  # If the review is not inserted, return 0
  if result2 <= 0:
    return 0
  # If the review is successfully inserted, return 1
  return 1



##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):

  # Check if the movie exists in the database
  query1 = "Select Movie_ID from Movies where Movie_ID = ?"
  result1 = datatier.select_one_row(dbConn, query1, [movie_id])
  
  # If the movie doesn't exist, return 0 to indicate an error
  if (len(result1) == 0):
      return 0

  # Check if the movie already has a tagline in the Movie_Taglines table
  query2 = "SELECT Movie_Taglines.Tagline FROM Movies LEFT JOIN Movie_Taglines ON Movies.Movie_ID = Movie_Taglines.Movie_ID WHERE Movie_Taglines.Movie_ID = ?"
  result2 = datatier.select_one_row(dbConn, query2, [movie_id]) 

  # If the movie doesn't have a tagline, insert a new tagline into the Movie_Taglines table
  if(len(result2) == 0):
    query2 = "Insert into Movie_Taglines (Movie_ID, Tagline) Values(?,?)"
    result2 = datatier.perform_action(dbConn, query2, [movie_id, tagline])
  
  # If the movie already has a tagline, update the existing tagline with the new tagline value
  else:
    query3 = "Update Movie_Taglines Set Tagline = ? where Movie_ID = ?"
    result3 = datatier.perform_action(dbConn, query3, [tagline, movie_id])
    
    # If an error occurs during the update, return 0 to indicate an error
    if result3 == -1:
      return 0

  # If the function executes successfully, return 1 to indicate success
  return 1
