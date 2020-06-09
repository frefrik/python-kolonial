import os
import requests
import logging
import json
from http.cookiejar import MozillaCookieJar

logger = logging.getLogger(__name__)

class Kolonial(object):
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
        results = self._get('productcategories/')
        
        return results

    def product_category(self, product_category_id=None):

        if product_category_id:
            results = self._get('productcategories/%s/' % (product_category_id))
        else:
            results = 'Usage: product_category(product_category_id)'

        return results

    def product(self, product_id=None):
        if product_id:
            results = self._get('products/%s/' % (product_id))
        else:
            results = 'Usage: product(product_id)'

        return results

    def search(self, query=None):
        results = self._get('search/?q=%s' % (query))

        return results

    def search_recipe(self, query=None):
        if query:
            results = self._get('search/recipes/?q=%s' % (query))
        else:
            results = 'Usage: search_recipe(query)'
        
        return results

    def recipe_tags(self):
        results = self._get('recipe-tags/')

        return results

    def recipe_tag(self, recipe_tag_id):
        results = self._get('recipe-tags/%s/' % (recipe_tag_id))

        return results

    def recipe_plans(self):
        results = self._get('recipes/plans/current/')

        return results

    def recipe(self, recipe_id=None):
        if recipe_id:
            results = self._get('recipes/%s/' % (recipe_id))
        else:
            results = 'Usage: recipe(recipe_id)'

        return results

    def recipes_likes(self):
        results = self._get('recipes/likes/')

        return results

    def recipes_purchased(self):
        results = self._get('recipes/purchased/')

        return results

    def recipe_like(self, recipe_id=None):
        if recipe_id:
            results = self._post('recipes/%s/like-toggle/' % (recipe_id))
        else:
            results = 'Usage: recipe_like(recipe_id)'
        
        return results

    def cart(self):
        results = self._get('cart/')

        return results

    def add_to_cart(self, items=None):
        if items:
            results = self._post('cart/items/', payload=items)
        else:
            results = 'Usage: add_to_cart(items)'
        
        return results

    def clear_cart(self):
        results = self._post('cart/clear/')

        return results
