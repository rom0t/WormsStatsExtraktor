import requests

def get_joke():
    # Make a GET request to the API
    response = requests.get("https://witzapi.de/api/joke")

    # Check if the GET request was successful
    if response.status_code == 200:
        # Get the JSON data from the response
        data = response.json()

        # Extract the joke from the JSON data
        #joke = data["joke"]["text"]
        return data[0]["text"]
    else:
        return "Sorry, I could not find a joke at the moment. Please try again later."

joke = get_joke()
print(joke)