# python-kolonial
Python wrapper for the [Kolonial.no API](https://github.com/kolonialno/api-docs)

# Installation


### Example usage

```python
from kolonial import Kolonial

USERNAME = 'your@email'
PASSWORD = 'yourPassword'
USER_AGENT = 'yourUserAgent'
TOKEN = 'yourToken'

# Authenticate using Kolonial account credentials and useragent/token
api = Kolonial(USERNAME, PASSWORD, USER_AGENT, TOKEN)

# Search products
search = api.search('melkesjokolade')

# Get product info
product_info = api.product('269')

# View cart
cart = api.cart()
```