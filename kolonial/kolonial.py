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

        self.auth = '{"username": "%s", "password": "%s" }' % (username, password)
        
        self._session()

    def _session(self):
        res = self.session.get(self.base_url)

        if res.status_code == 401:
            self._login()
        else:
            pass

    def _login(self):
        self._post('user/login/', payload=self.auth)

        self.cj.save(ignore_discard=True, ignore_expires=True)

    def _internal_call(self, method, endpoint, payload=None):
        url = self.base_url + endpoint

        try:
            response = self.session.request(method, url, data=payload)
            response.raise_for_status()

            if response.status_code == 404:
                return None

            results = response.json()

            return results
            
        except requests.exceptions.HTTPError:
            try:
                msg = response.json()['detail']
            except (ValueError, KeyError):
                msg = "Error"

            logger.error('Error: %s - %s',
                         response.status_code, msg)
            return None

    def _get(self, endpoint):
        return self._internal_call('GET', endpoint)

    def _post(self, endpoint, payload=None):
        return self._internal_call('POST', endpoint, payload)

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
            results = self._get('productcategories/%s/' % (product_category_id))
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
            results = self._get('products/%s/' % (product_id))
        else:
            results = 'Usage: product(product_id)'

        return results

    def search(self, query=None):
        """
        Search for a product. Can be used for both text queries and numeric barcodes

        Parameters:
            - query - the search query
        
        """
        results = self._get('search/?q=%s' % (query))

        return results

    def search_recipe(self, query=None):
        """
        Search for a recipe.

        Parameters:
            - query - the search query
        
        """
        if query:
            results = self._get('search/recipes/?q=%s' % (query))
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
        results = self._get('recipe-tags/%s/' % (recipe_tag_id))

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
            results = self._get('recipes/%s/' % (recipe_id))
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
            results = self._post('recipes/%s/like-toggle/' % (recipe_id))
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
