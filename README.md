# Lyric Generator
Root repo for my Lyric Generator web application. 
This project uses Markov Chains to generate new, unique lyrics for a musical artist
based on probabilities from their top 10 songs.

# Microservice Implementation
How to request data:
To request data, simply send a POST request in your app to this app's microservice URL. For example:
req = requests.post(url="http://127.0.0.1:5000/microservice")

This will essentially just call the function on my app, which will generate a list of links in JSON format.

How to receive data:
Since the data is a list of JSON data, you can store it in a variable. For example, using the req variable from above:
data = req.json()

This will ensure you have successfully received and stored the data from this microservice.

Please refer to the following UML Sequence Diagram for further details:
[Future UML Sequence Diagram]
