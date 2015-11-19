from collections import Counter
from datetime import datetime, timedelta
import itertools
import urllib
import urlparse

from django.conf import settings
import requests

from core.models import Product
from incident_response.models import IratStatus


class ZendeskClient(object):
    """
    Zendesk REST API client
    """

    def __init__(self):
        conf = settings.ZENDESK_API
        self.base_url = conf['url']
        self.auth = ('{username}/token'.format(**conf), conf['token'])

    def _request(self, endpoint, data=None, **kwargs):
        url = '?'.join(filter(None, [
            urlparse.urljoin(self.base_url, endpoint),
            len(kwargs) and urllib.urlencode(kwargs) or None]))
        headers = {'content-type': 'application/json'}

        if data is None:
            return requests.get(url, auth=self.auth, headers=headers)

        return requests.post(url, data=data, auth=self.auth, headers=headers)

    def search(self, **kwargs):
        return self._request('search.json', **kwargs)


class ZendeskSearch(object):
    """
    Lazily populated list of search results for specified query.

    The search results are fetched on demand. Results are fetched once only and
    cached.

    NB: Behaviour is undefined if tickets matching the search query are created
    or deleted between page fetches.
    """

    class Result(object):
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    def __init__(self, query):
        self.query = query

    def _result_pages(self):
        zd = ZendeskClient()

        for page in itertools.count(1):
            json = zd.search(query=self.query, page=page).json()
            self.count = json.get('count', 0)
            yield json.get('results', [])

            if 'next_page' not in json:
                raise StopIteration

    def __len__(self):
        if not hasattr(self, 'count'):
            self._results = next(self._result_pages())

        return self.count

    def __getitem__(self, i):
        if i < 0 or i >= len(self):
            raise IndexError

        while i >= len(self._results):
            self._results.extend(next(self._result_pages()))

        return self.Result(**self._results[i])

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]


class IncidentsInLast2Weeks(ZendeskSearch):

    def __init__(self):
        self.query = (
            'ticket_type:incident created>{two_weeks_ago:%Y-%m-%d}'.format(
                two_weeks_ago=datetime.utcnow() - timedelta(days=14)))


def check_incidents():
    incidents = IncidentsInLast2Weeks()
    prefix = 'product:'

    def product_tags(incident):
        return filter(lambda tag: tag.startswith(prefix), incident.tags)

    counts = sum(map(Counter, map(product_tags, incidents)), Counter())

    for tag, count in counts.iteritems():

        try:
            product = Product.objects.get(slug=tag[len(prefix):])

        except Product.DoesNotExist:
            continue

        try:
            status = IratStatus.objects.get(product=product)
            status.incidents_in_last_two_weeks = count
            status.save()

        except IratStatus.DoesNotExist:
            status = IratStatus.objects.create(
                product=product,
                incidents_in_last_two_weeks=count)
