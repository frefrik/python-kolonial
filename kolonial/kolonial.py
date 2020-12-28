import os
import requests
import logging
import json
from http.cookiejar import MozillaCookieJar

logger = logging.getLogger(__name__)


class Kolonial(object):
    """
    Class for accessing Kolonial.no API.

    """
    cookiesFile = 'kolonial_cj.txt'
    cj = MozillaCookieJar(cookiesFile)

    if os.path.exists(cookiesFile):
        cj.load(ignore_discard=True, ignore_expires=True)

    def __init__(self, username, password, useragent, token):
        self.base_url = 'https://kolonial.no/api/v1/'

        self.session = requests.Session()
        self.session.cookies = Kolonial.cj

        self.session.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': useragent,
            'X-Client-Token': token
        }

        self.auth = {
            'username': username,
            'password': password
        }

        self._session()

    def _session(self):
        res = self.session.get(self.base_url)

        if res.status_code == 401:
            self._login()
        else:
            pass

    def _login(self):
        self._post('user/login/', payload=json.dumps(self.auth))

        self.cj.save(ignore_discard=True, ignore_expires=True)

    def _internal_call(self, method, endpoint, payload=None):
        url = self.base_url + endpoint

        response = self.session.request(method, url, data=payload)

        try:
            response.raise_for_status()

            if response.status_code == 404:
                return None

            results = response.json()

            return results

        except requests.exceptions.HTTPError:
            try:
                msg = response.json()['errors'][0]
            except (ValueError, KeyError):
                msg = "Error"

            logger.error(f'Error {response.status_code} - {msg}')

            return None

    def _get(self, endpoint):
        return self._internal_call('GET', endpoint)

    def _post(self, endpoint, payload=None):
        return self._internal_call('POST', endpoint, payload)

    def _delete(self, endpoint):
        return self._internal_call('DELETE', endpoint)

    def product_categories(self):
        """
        Gets list of all product categories.

        """
        results = self._get('productcategories/')

        return results

    def product_category(self, product_category_id=None):
        """
        Gets all products in a given product category.

        Parameters:
            - product_category_id - the id of the product category

        """
        if product_category_id:
            results = self._get(f'productcategories/{product_category_id}/')
        else:
            results = 'Usage: product_category(product_category_id)'

        return results

    def product(self, product_id=None):
        """
        Gets extended information about specified product.

        Parameters:
            - product_id - the id of the product

        """
        if product_id:
            results = self._get(f'products/{product_id}/')
        else:
            results = 'Usage: product(product_id)'

        return results

    def search(self, query=None):
        """
        Search for a product. Can be used for both text queries and numeric barcodes

        Parameters:
            - query - the search query

        """
        results = self._get(f'search/?q={query}')

        return results

    def search_recipe(self, query=None):
        """
        Search for a recipe.

        Parameters:
            - query - the search query

        """
        if query:
            results = self._get(f'search/recipes/?q={query}')
        else:
            results = 'Usage: search_recipe(query)'

        return results

    def recipe_tags(self):
        """
        Gets list of recipe tags.

        """
        results = self._get('recipe-tags/')

        return results

    def recipe_tag(self, recipe_tag_id):
        """
        Gets all recipes in specified recipe tag.

        Parameters:
            - recipe_tag_id - the id of the recipe tag

        """
        results = self._get(f'recipe-tags/{recipe_tag_id}/')

        return results

    def recipe_plans(self):
        """
        Gets list of your suggested recipe plans.

        """
        results = self._get('recipes/plans/current/')

        return results

    def recipe(self, recipe_id=None):
        """
        Gets extended information about specified recipe, including product details.

        Parameters:
            - recipe_id - the id of the recipe

        """
        if recipe_id:
            results = self._get(f'recipes/{recipe_id}/')
        else:
            results = 'Usage: recipe(recipe_id)'

        return results

    def recipes_likes(self):
        """
        Gets list of your liked recipes.

        """
        results = self._get('recipes/likes/')

        return results

    def recipes_purchased(self):
        """
        Gets list of your liked recipes.

        """
        results = self._get('recipes/purchased/')

        return results

    def recipe_like(self, recipe_id=None):
        """
        Toggles like button on a specified recipe.

        Parameters:
            - recipe_id - the id of the recipe

        """
        if recipe_id:
            results = self._post(f'recipes/{recipe_id}/like-toggle/')
        else:
            results = 'Usage: recipe_like(recipe_id)'

        return results

    def cart(self):
        """
        View the contents of your cart.

        """
        results = self._get('cart/')

        return results

    def modify_cart(self, items=None):
        """
        Add or remove products to/from your cart.
        The quantity field adjusts the quantity currently in the cart.

        Parameters:
            - items - json-array of items to add. For example:
                {
                    "items": [{
                        "product_id": 9329,
                        "quantity": 2,
                    }, {
                        "product_id": 15163,
                        "quantity": 1
                    }]
                }

        """
        if items:
            results = self._post('cart/items/', payload=items)
        else:
            results = 'Usage: add_to_cart(items)'

        return results

    def clear_cart(self):
        """
        Clear the contents of your cart.

        """
        results = self._post('cart/clear/')

        return results

    def product_lists(self):
        """
        List all product lists.

        """
        results = self._get('product-lists/')

        return results

    def product_list(self, id=None):
        """
        Show product list items/details.

        Parameters:
            - id - product-list id

        """
        if id:
            results = self._get(f'product-lists/{id}/')
        else:
            results = 'Usage: product_list(id)'

        return results

    def product_list_suggestions(self, id=None, limit=10, offset=0):
        """
        Get list of product suggestions from product list.

        Parameters:
            - id - product-list id
            - offset - (default: 0)
            - limit  - (default: 10)

        """

        if id:
            results = self._get(f'product-lists/{id}/suggestions/?limit={limit}&offset={offset}')
        else:
            results = 'Usage: product_list_suggestions(id, limit, offset)'

        return results

    def new_product_list(self, title=None, description=None):
        """
        Create new product list.

        Parameters:
            - title - product-list title
            - description - product-list description

        """

        payload = {
            'title': title,
            'description': description
        }

        if title and description:
            results = self._post('product-lists/', payload=json.dumps(payload))
        else:
            results = 'Usage: new_product_list(title, description)'

        return results

    def modify_product_list(self, id=None, title=None, description=None):
        """
        Change title and/or description of product list.

        Parameters:
            - id - product-list id
            - title - product-list title
            - description - product list description (optional)

        """
        payload = {}

        if title:
            payload['title'] = title
        if description:
            payload['description'] = description

        if id and title:
            results = self._post(f'product-lists/{id}/', payload=json.dumps(payload))
        else:
            results = 'Usage: modify_product_list(id, title, description)'

        return results

    def delete_product_list(self, id=None):
        """
        Delete an existing product list.

        Parameters:
            - id - product-list id

        """
        if id:
            results = self._delete(f'product-lists/{id}/')
        else:
            results = 'Usage: delete_product_list(id)'

        return results

    def add_to_product_list(self, id=None, product_id=None, quantity=1):
        """
        Add new product to list.

        Parameters:
            - id - product-list id
            - product_id - product id
            - quantity - quantity (default: 1)

        """
        payload = {
            'items': [
                {}
            ]
        }

        if id and product_id:
            payload['items'][0]['product_id'] = product_id
            payload['items'][0]['quantity'] = quantity

            results = self._post(f'product-lists/{id}/products/', payload=json.dumps(payload))
        else:
            results = 'Usage: add_to_product_list(id, product_id, quantity)'

        return results

    def remove_from_product_list(self, id=None, product_id=None):
        """
        Remove product from list.

        Parameters:
            - id - product-list id
            - product_id - product id

        """
        payload = {
            'items': [
                {}
            ]
        }

        if id and product_id:
            payload['items'][0]['product_id'] = product_id
            payload['items'][0]['delete'] = True

            results = self._post(f'product-lists/{id}/products/', payload=json.dumps(payload))
        else:
            results = 'Usage: remove_from_product_list(id, product_id)'

        return results
