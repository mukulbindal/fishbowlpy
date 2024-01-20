# fishbowlpy

fishbowlpy is a Python library that allows you to interact with fishbowlapp. This library provides a simple interface to login, access bowls, posts, and comments in your fishbowlapp feed.

## First of all what is Fishbowlapp?

Fishbowlapp is an anonymous network where you can post insights of your company without revealing your identity. It's a good platform for those who are looking into job change or want suggestions from random people. It is a Glassdoor initiative but now there are lots of things going on in this platform. You can ask for referrals, give referrals, discuss about ongoing policy changes and that too without revealing your identity. Visit https://www.fishbowlapp.com for more info.

## Features

It is just the beginning. I have created the basic needs, and **looking for the contributors** to make this library developed quickly.

## Prerequisites

Before you start using fishbowlpy, please make sure you have Python 3.6 or higher installed on your machine.

## Installation

You can install fishbowlpy from the Python Package Index (PyPI). Make sure you have pip installed on your system, and then run the following command:

```
pip install fishbowlpy
```

## Usage

Here is an example of the minimum code required to use fishbowlpy. You can find the [full documentation here.](https://mukulbindal.github.io/fishbowlpy/)

```
from fishbowlpy.fishbowlclient import FishBowlClient

# Initialize the fishbowl client
client = FishBowlClient()

# Access posts in the subscribed bowl
posts = client.get_posts(bowl_name='tech-india')

print(posts)
```

## Documentation

Documentation is available here [https://mukulbindal.github.io/fishbowlpy/](https://mukulbindal.github.io/fishbowlpy/).

## Contributions

We encourage you to contribute to this package by following these steps:

Start by exploring the issues tab and selecting any issue that you would like to work on. This will help you find areas where your skills can be put to good use.

If you have a new feature in mind that you believe would enhance the package, we invite you to create a new issue to propose your idea. This allows the community to provide feedback and discuss the potential implementation before you begin working on it.

Before creating a pull request, it's important to ensure that you follow our contribution guidelines. These guidelines outline the required coding style, documentation standards, and any other specific conventions we follow. Adhering to these guidelines helps maintain consistency throughout the codebase.

By following these steps, you can actively participate in improving the package and help make it even better. Your contributions are highly appreciated and valued by the community.

## Contributors

We eagerly anticipate your valuable contribution to our project. As a token of our appreciation, we have reserved a special section where we will acknowledge your involvement. Rest assured, we will diligently update the contributors list under this designated section to recognize your valuable input.

## License

This project is licensed under the [MIT License](https://github.com/mukulbindal/fishbowlpy/blob/main/LICENSE).

## Contact Information

Feel free to reach out to me with any questions or suggestions. I look forward to hearing from you at mukulbindal170299@gmail.com
