import tweepy

# Your API keys and tokens
api_key = '9k5tcllDnxPQJNb41cwQt8ATj'
api_secret_key = 'AvpOBex7EpTn617eM9EK0qxSGyzoX0xhTv3riRJpE2Ad7qPJZg'
access_token = '1879457784363622401-0A4bV5EYDMtQcBsfKYTmuyB4bR5RlZ'
access_token_secret = 'aGEzODEfdFZZbLOjgez8eGSlp2ATCGFfMOvN8mSoXgeXh'















api_key = '9k5tcllDnxPQJNb41cwQt8ATj'
api_secret_key = 'AvpOBex7EpTn617eM9EK0qxSGyzoX0xhTv3riRJpE2Ad7qPJZg'
access_token = '1879457784363622401-0A4bV5EYDMtQcBsfKYTmuyB4bR5RlZ'
access_token_secret = 'aGEzODEfdFZZbLOjgez8eGSlp2ATCGFfMOvN8mSoXgeXh'
client_id = 'MHptVFVtQW5Ua1JyU0V5SVI2R1o6MTpjaQ'
client_secret = '8HrEa52Q7KPqwsGq3awB_09_0dFSmmfC3eVknVkbi7sYFv_avW'




# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(consumer_key=api_key,
                                 consumer_secret=api_secret_key,
                                 access_token=access_token,
                                 access_token_secret=access_token_secret)

# Create API object
api = tweepy.API(auth)

# Tweet content and image
tweet_text = "🚀 Here's my latest update! #Django #Python #Development"
image_path = 'path_to_your_image.jpg'  # Replace with the path to your image file

# Post the tweet with an image
api.update_with_media(image_path, status=tweet_text)

print("Tweet posted successfully!")
# C:\Users\Deepak\api\ecommerce_website\twiter.py