# fishbowlpy

A python library to interact with fishbowlapp. This library provides a simple interface to login, access bowls, posts and comments in our fishbowlapp feed.

## Prerequisites

Before you continue, make sure you have python 3.6 or higher installed in your machine.

## Installation

This package is available on pypi.org
Make sure you have pip installed in your system

```
pip install fishbowlpy
```

## Usage

Below is the bare minimum code to use this package. Full documentation can be accessed here.

```
from fishbowlpy.fishbowlclient import FishBowlClient

# Initialize the fishbowl client
client = FishBowlClient()

# Access posts in the subscribed bowl
posts = client.get_posts('tech-india')

print(posts)
```

## Contributions

You can contribute to this package. Check out the issues tab and pick up any issue you want to work with. If you have any new feature in mind, feel free to create one issue before creating a pull request. Please make sure to follow our contribution guidelines before creating a pull request.

## Contributors

Below are the contributors for this library.
Mukul Bindal

## License

MIT License

## Contact Information

In case you have any questions, suggestion, feel free to contact me at mukulbindal170299@gmail.com
