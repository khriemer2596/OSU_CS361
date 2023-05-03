# Lyric Generator
Root repo for my Lyric Generator web application. 
This project uses Markov Chains to generate new, unique lyrics for a musical artist
based on probabilities from their top 10 songs.

Please refer to requirements.txt for requirements/dependencies if you want to run the app locally.

# Microservice Implementation/Communication Contract
How to request data:
To request data, simply send a POST request in your app to this app's microservice URL. For example, if you are running this app locally on port 5000, you can make the call from your app by doing the following:
```
req = requests.post(url="http://localhost:5000/microservice")
```

This will essentially just call the microservice function on my app, which will generate a list of links in JSON format.

How to receive data:
Currently, this app assumes you are running you're app locally on port 3000. If this is not the case, please update line 48 in the app.py with the correct destination URL of your app. 

Since the data is a list of JSON data, you can store it in a variable. For example, using the req variable from above, you can add this to your app:
```
data = req.json()
```

This will ensure you have successfully received and stored the data sent from this microservice.

Long term, this app will be hosted on Heroku and the microservice will be available to handle calls from there.

Please refer to the following UML Sequence Diagram for further details:
![alt text](images/UML%20Sequence%20Diagram%20Image.png)
