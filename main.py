# Import the necessary libraries
import sqlite3
import objecttier

################################################################## 
# Define the lookup_name function to search for a movie by name
################################################################## 
def lookup_name(dbConn):
    print()
    # Prompt the user to enter a movie name
    movie = input("Enter movie name (wildcards _ and % supported): ")
    
    # Call the get_movies function to get a list of movies matching the search criteria
    movies = objecttier.get_movies(dbConn, movie)
    
    # Handle errors and display the search results
    if movies is None:  # error
        print("**Internal error: lookup_name")
    elif len(movies) > 100:
        print()
        print("# of movies found:", len(movies))
        print()
        print("There are too many movies to display, please narrow your search and try again...")
    else: 
        print()
        print("# of movies found:", len(movies))
        for s in movies:
            print(s.Movie_ID, ":", s.Title, "("+s.Release_Year+")")
          
################################################################## 
# Define the details function to display details about a movie
##################################################################       
def details(dbConn):
    print()

    # Prompt the user to enter a movie ID
    movie = input("Enter movie id: ")
    
    # Call the get_movie_details function to get the details of the specified movie
    m_detail = objecttier.get_movie_details(dbConn, movie)

    # Handle errors and display the movie details
    if m_detail is None:  # error
        print()
        print("No such movie...")
    else: 
        print()
        print(m_detail.Movie_ID, ":", m_detail.Title)
        print("  Release date:",m_detail.Release_Date)
        print("  Runtime:", m_detail.Runtime,"("+"mins"+")")
        print("  Orig language:", m_detail.Original_Language)
        print("  Budget: ${:,}".format(m_detail.Budget),"(USD)")
        print("  Revenue: ${:,}".format(m_detail.Revenue),"(USD)")
        print("  Num reviews:",m_detail.Num_Reviews)
        print("  Avg rating:",f"{m_detail.Avg_Rating:.2f}","(0..10)")
        print('  Genres:', end= ' ')
        for line in m_detail.Genres:
              print(line, end=", ")
              
        print()
        print('  Production companies:', end = " ")
        for line in m_detail.Production_Companies:
              print(line, end=", ")
              
        print()
        print("  Tagline:",m_detail.Tagline)
      
################################################################## 
# Define the top_N function to display the top N movies
# based on their average rating      
################################################################## 
def top_N(dbConn):
    print()
    
    # Get user input for N and min number of reviews
    n = input("N? ")
    n = int(n)
    if(n<=0):
        print("Please enter a positive value for N...")
        return
  
    min = input("min number of reviews? ")
    min = int(min)
    if(min<=0):
        print("Please enter a positive value for min number of reviews...")
        return

    # Get top N movies based on user input
    result = objecttier.get_top_N_movies(dbConn,n,min)

    if result is None:
        return 
    else:
        print()
        # Print the top N movies
        for s in result:
            print(s.Movie_ID,":",s.Title,"("+s.Release_Year+"),","avg rating =", f"{s.Avg_Rating:.2f}", "({}".format(s.Num_Reviews),"reviews)")

################################################################## 
# Add a review for a movie.
# param dbConn: Database connection object
################################################################## 
def review(dbConn):
    print()
    # Get user input for rating and movie ID
    num = input("Enter rating (0..10): ")
    num = int(num)
    if(num < 0 or num > 10):
        print("Invalid rating...")
        return

    id = input("Enter movie id: ")
  
    # Add the review to the database
    result = objecttier.add_review(dbConn,id,num)
  
    if result == 0:
        print()
        print("No such movie...")
    else:
        print()
        print("Review successfully inserted")
      
################################################################## 
# Set a tagline for a movie.
# param: dbConn Database connection object
##################################################################       
def tagline(dbConn):
    print()
    # Get user input for tagline and movie ID
    prompt = input("tagline? ")
    id = input("movie id? ")

    # Set the tagline for the movie
    result = objecttier.set_tagline(dbConn,id,prompt)

    if result == 0:
        print()
        print("No such movie...")
    else:
        print()
        print("Tagline successfully set")

################################################################## 
# main
################################################################## 
print('** Welcome to the MovieLens app **')
print()
# Connect to the database and print general stats
dbConn = sqlite3.connect('MovieLens.db')
print("General stats:")
print("  # of movies: {:,}".format(objecttier.num_movies(dbConn)))
print("  # of reviews: {:,}".format(objecttier.num_reviews(dbConn)))
print()

# Loop through user commands until 'x' is entered
cmd = input("Please enter a command (1-5, x to exit): ")
while cmd != "x":
    if cmd == "1":
        lookup_name(dbConn)
    elif cmd == "2":
        details(dbConn)
    elif cmd == "3":
        top_N(dbConn)
    elif cmd == "4":
        review(dbConn)
    elif cmd == "5":
        tagline(dbConn)
    else:
        print("**Error, unknown command, try again...")

    print()
    cmd = input("Please enter a command (1-5, x to exit): ")

# Close the database connection
dbConn.close()
#
# done
#