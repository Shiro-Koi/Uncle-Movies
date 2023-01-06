import openai
import discord
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

openai.api_key = os.getenv("API_KEY")

client = discord.Client()

# This function is used to get the list of movies from the logger (by reading from the movie-log.txt file)


def get_movie_list():
    movie_list = []
    try:
        with open("movie-log.txt", "r") as movie_log_file:
            for line in movie_log_file:
                movie_list.append(line.strip())
    except FileNotFoundError:
        return "movie-log.txt file not found"
    else:
        return "\n".join(movie_list)

# This function is used to search for movies in the logger (by searching the movie-log.txt file)


def search_movies(query):
    search_results = []
    try:
        with open("movie-log.txt", "r") as movie_log_file:
            for line in movie_log_file:
                if query.lower() in line.lower():
                    search_results.append(line.strip())
    except FileNotFoundError:
        return "movie-log.txt file not found"
    else:
        if not search_results:
            return "No results found"
        return "\n".join(search_results)

# This function is used to add a movie to the logger (by appending to the movie-log.txt file)


def add_movie(movie_details):
    if not movie_details:
        return
    # Check if the movie already exists in the logger
    if movie_details in search_movies(movie_details):
        return
    try:
        with open("movie-log.txt", "a") as movie_log_file:
            movie_log_file.write(f"{movie_details}\n")
    except FileNotFoundError:
        return "movie-log.txt file not found"
    
# This function is used to delete a movie from the logger (by overwriting the movie-log.txt file)


def delete_movie(movie_details):
    movie_list = get_movie_list()
    if movie_details not in movie_list:
        return "Movie not found"
    try:
        with open("movie-log.txt", "w") as movie_log_file:
            for movie in movie_list:
                if movie != movie_details:
                    movie_log_file.write(f"{movie}\n")
    except FileNotFoundError:
        return "movie-log.txt file not found"
    

# This function is used to handle errors


def handle_error(error):
    try:
        return f"Error occurred: {error}"
    except Exception as e:
        return "Unable to create error message"


# Debug intents
debug_guild = int(os.getenv("DEBUG_GUILD"))
debug_channel = int(os.getenv("DEBUG_CHANNEL"))


@client.event
async def on_message(message):
    # Check if the message is a command for the bot
    if message.content.startswith("/add"):
        # Use the Davinci-003 model to parse the natural language input and extract the movie details
        try:
            response = openai.Completion.create(
                engine="davinci-003",
                prompt=f"/add {message.content[5:]}",
                max_tokens=1024,
                temperature=0.5,
            )
        except Exception as e:
            # Handle any errors that occurred
            await message.channel.send(handle_error(e))
            return
        # Extract the movie details from the response
        movie_details = response["choices"][0]["text"].strip()
        # Add the movie to the logger
        result = add_movie(movie_details)
        if result:
            await message.channel.send(result)
        else:
            await message.channel.send(f"Movie added: {movie_details}")
            
    elif message.content.startswith("/list"):
        # Get the list of movies from the logger
        movie_list = get_movie_list()
        # Send the list of movies to the channel
        await message.channel.send(f"Movies:\n{movie_list}")
        
    elif message.content.startswith("/search"):
        # Use the Davinci-003 model to parse the natural language search query
        try:
            response = openai.Completion.create(
                engine="davinci-003",
                prompt=f"/search {message.content[8:]}",
                max_tokens=1024,
                temperature=0.5,
            )
        except Exception as e:
            # Handle any errors that occurred
            await message.channel.send(handle_error(e))
            return
        # Extract the search query from the response
        search_query = response["choices"][0]["text"].strip()
        # Search the logger for movies matching the search query
        search_results = search_movies(search_query)
        # Send the search results to the channel
        await message.channel.send(f"Search results:\n{search_results}")
    elif message.content.startswith("/delete"):
        # Use the Davinci-003 model to parse the natural language input and extract the movie details
        try:
            response = openai.Completion.create(
                engine="davinci-003",
                prompt=f"/delete {message.content[8:]}",
                max_tokens=1024,
                temperature=0.5,
            )
        except Exception as e:
            # Handle any errors that occurred
            await message.channel.send(handle_error(e))
            return
        # Extract the movie details from the response
        movie_details = response["choices"][0]["text"].strip()
        # Delete the movie from the logger
        result = delete_movie(movie_details)
        if result:
            await message.channel.send(result)
        else:
            await message.channel.send(f"Movie deleted: {movie_details}")


# Run the bot
client.run(os.getenv("DISCORD_BOT_TOKEN"))



        


# import openai
# import discord
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# openai.api_key = os.getenv("API_KEY")

# client = discord.Client()

# # This function is used to get the list of movies from the logger (by reading from the movie-log.txt file)


# def get_movie_list():
#     movie_list = []
#     try:
#         with open("movie-log.txt", "r") as movie_log_file:
#             for line in movie_log_file:
#                 movie_list.append(line.strip())
#     except FileNotFoundError:
#         return "movie-log.txt file not found"
#     else:
#         return "\n".join(movie_list)

# # This function is used to search for movies in the logger (by searching the movie-log.txt file)


# def search_movies(query):
#     search_results = []
#     try:
#         with open("movie-log.txt", "r") as movie_log_file:
#             for line in movie_log_file:
#                 if query.lower() in line.lower():
#                     search_results.append(line.strip())
#     except FileNotFoundError:
#         return "movie-log.txt file not found"
#     else:
#         if not search_results:
#             return "No results found"
#         return "\n".join(search_results)

# # This function is used to add a movie to the logger (by appending to the movie-log.txt file)


# def add_movie(movie_details):
#     if not movie_details:
#         return
#     # Check if the movie already exists in the logger
#     if movie_details in search_movies(movie_details):
#         return
#     try:
#         with open("movie-log.txt", "a") as movie_log_file:
#             movie_log_file.write(f"{movie_details}\n")
#     except FileNotFoundError:
#         return "movie-log.txt file not found"

# # This function is used to handle errors


# def handle_error(error):
#     try:
#         return f"Error occurred: {error}"
#     except Exception as e:
#         return "Unable to create error message"


# # Debug intents
# debug_guild = os.getenv("DEBUG_GUILD")
# debug_channel = os.getenv("DEBUG_CHANNEL")


# @client.event
# async def on_message(message):
#     # Check if the message is a command for the bot
#     if message.content.startswith("/add"):
#         # Use the Davinci-003 model to parse the natural language input and extract the movie details
#         try:
#             response = openai.Completion.create(
#                 engine="davinci-003",
#                 prompt=f"/add {message.content[5:]}",
#                 max_tokens=1024,
#                 temperature=0.5,
#             )
#         except Exception as e:
#             # Handle any errors that occurred
#             await message.channel.send(handle_error(e))
#             return
#         # Extract the movie details from the response
#         movie_details = response["choices"][0]["text"].strip()
#         # Add the movie to the logger
#         result = add_movie(movie_details)
#         if result:
#             await message.channel.send(result)
#         else:
#             await message.channel.send(f"Movie added: {movie_details}")
#     elif message.content.startswith("/list"):
#         # Get the list of movies from the logger
#         movie_list = get_movie_list()
#         # Send the list of movies to the channel
#         await message.channel.send(f"Movies:\n{movie_list}")
#     elif message.content.startswith("/search"):
#         # Use the Davinci-003 model to parse the natural language search query
#         try:
#             response = openai.Completion.create(
#                 engine="davinci-003",
#                 prompt=f"/search {message.content[8:]}",
#                 max_tokens=1024,
#                 temperature=0.5,
#             )
#         except Exception as e:
#             # Handle any errors that occurred
#             await message.channel.send(handle_error(e))
#             return
#         # Extract the search query from the response
#         search_query = response["choices"][0]["text"].strip()
#         # Search for movies in the logger
#         search_results = search_movies(search_query)
#         # Send the search results to the channel
#         await message.channel.send(f"Search results:\n{search_results}")
#     elif message.guild.id == debug_guild and message.channel.id == debug_channel:
#         # Use the Davinci-003 model to generate a response to the message
#         try:
#             response = openai.Completion.create(
#                 engine="davinci-003",
#                 prompt=message.content,
#                 max_tokens=1024,
#                 temperature=0.5,
#             )
#         except Exception as e:
#             # Handle any errors that occurred
#             await message.channel.send(handle_error(e))
#             return
#         # Extract the response from the model
#         bot_response = response["choices"][0]["text"].strip()
#         # Send the response to the channel
#         await message.channel.send(bot_response)

# # Run the bot
# client.run(os.getenv("DISCORD_BOT_TOKEN"))
