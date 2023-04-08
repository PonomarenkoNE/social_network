import os
import asyncio
import aiohttp
import random

from loremipsum import get_sentence
from faker import Faker
from dotenv import load_dotenv

# Load configuration from a file
load_dotenv('bot.env')

number_of_users = int(os.getenv('NUMBER_OF_USERS', 4))
max_posts_per_user = int(os.getenv('MAX_POSTS_PER_USER', 2))
max_likes_per_user = int(os.getenv('MAX_LIKES_PER_USER', 5))
base_url = os.getenv('BASE_URL', 'http://localhost:8000')

# Use faker for generating fake usernames, passwords and emails
fake: Faker = Faker()


singup_url = f'{base_url}/auth/users/'  # User signup endpoint

login_url = f'{base_url}/auth/jwt/create/'  # User login endpoint

list_posts = f'{base_url}/api/posts/'

post_url = f'{base_url}/api/posts/create'  # Post creation endpoint

like_url = f'{base_url}/api/like/'  # Post liking endpoint


async def signup_user(session):
    # Generate a random username and password
    username = fake.user_name()
    password = fake.password(length=8)
    email = fake.email()

    # Create the signup request payload
    data = {
        'username': username,
        'password': password,
        'email': email
    }

    # Make the signup request
    async with session.post(singup_url, data=data) as response:
        print(f"Response on user {username} with password {password}: {await response.text()}")
        if response.status != 201:
            return

    async with session.post(login_url, data=data) as response:
        if response.status != 200:
            print(f"Wrong login or password for user {username}")
            return
        token = (await response.json()).get('access')

    return token


async def create_posts(session, token):
    # Generate a random number of posts for the user
    num_posts = random.randint(1, int(max_posts_per_user))

    # Create the post request payload
    data = {
        'content': get_sentence(),
        'title': get_sentence()
    }
    headers = {
        'Authorization': f'Bearer {token}'
    }

    # Make the post requests
    for i in range(num_posts):
        async with session.post(post_url, data=data, headers=headers) as response:
            print(f"Response creating post: {await response.text()}")


async def like_posts(session, token):
    # Get all posts for the user
    headers = {
        'Authorization': f'Bearer {token}'
    }
    async with session.get(list_posts, headers=headers) as response:
        print(f"List of all posts: {await response.text()}")
        posts = await response.json()

    # Randomly like posts
    num_likes = random.randint(1, min(max_likes_per_user, len(posts)))
    post_ids = [post['id'] for post in posts]
    for i in range(num_likes):
        post_id = random.choice(post_ids)
        data = {
            'to_post': post_id
        }
        async with session.post(like_url, data=data, headers=headers) as response:
            if response.status == 201:
                print(f"Liked post with id:{post_id}")
            else:
                print(f"Like for post with id {post_id} skipped")


async def run():
    async with aiohttp.ClientSession() as session:
        # Signup users
        tokens = await asyncio.gather(*[signup_user(session) for i in range(number_of_users)])

        # Create posts and like posts for each user
        for token in tokens:
            if token is None:
                print("Skipped one token")
                continue
            await create_posts(session, token)
            await like_posts(session, token)


if __name__ == '__main__':
    asyncio.run(run())
