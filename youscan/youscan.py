import requests
from json import JSONDecodeError
from urllib.parse import urlencode

from .exceptions import YouScanException


class Client(object):

    def __init__(self, token: str, mock_server: bool = False) -> None:
        """
        :param token: str (api_key from youscan)
        :param mock_server bool (test with mock server, default=False)
        """
        self.token = token
        self.API_URL = 'https://api.youscan.io/api/external' if not mock_server \
            else 'https://private-anon-d9f08809e4-youscan.apiary-mock.com/api/external'

    def _send_api_request(self, method: str, url: str, data: dict = {}) -> any:
        try:
            session = requests.session()
            r = session.__getattribute__(method)(url=url, json=data)
            if r.status_code > 204:
                print(r.text)
                raise YouScanException(r.status_code, r.reason)
            return r.json()
        except (requests.ConnectionError, JSONDecodeError):
            raise YouScanException(500, "Server connection error.")

    def get_topics(self):
        """
        endpoint doc - https://youscan.docs.apiary.io/#reference/topics/list-topics/list-topics?console=1
        :return: json data or raise YouScanException
        """
        url = f"{self.API_URL}/topics/?apiKey={self.token}"
        return self._send_api_request('get', url)

    def get_tags(self, topic_id: int) -> any:
        """
        endpoint doc - https://youscan.docs.apiary.io/#reference/topics/list-tags/list-tags?console=1
        :param topic_id: int
        :return: any or raise YouScanException
        """
        url = f"{self.API_URL}/topics/{topic_id}/tags/?apiKey={self.token}"
        return self._send_api_request('get', url)

    def crete_tag(self, topic_id: int, name: str, note: str, color: str) -> any:
        """
        endpoint doc - https://youscan.docs.apiary.io/#reference/topics/create-tag/create-tag?console=1
        :param topic_id: int
        :param name: str (like: "unique_name")
        :param note: str (like: "some notes")
        :param color: str (like: "red")
        :return: any or raise YouScanException
        """
        url = f"{self.API_URL}/topics/{topic_id}/tags/?apiKey={self.token}"
        data = {
            'name': name,
            'note': note,
            'color': color,
        }
        return self._send_api_request('post', url=url, data=data)

    def _create_param(self, param: str) -> str:
        """
        :param param: str
        :return: str
        """
        if '_' in param:
            spl = param.split('_')
            return spl[0] + spl[1].capitalize()
        elif param == 'from_date':
            return 'from'
        elif param == 'to_date':
            return 'to'
        return param

    def list_mentions(self, topic_id: int, from_date: str = None, to_date: str = None, sentiment: str = None,
                      exclude_sentiment: str = None, sources: str = None, exclude_sources: str = None,
                      tags: str = None, exclude_tags: str = None, auto_categories: str = None,
                      exclude_auto_categories: str = None, starred: bool = None, tagged: bool = None,
                      processed: bool = None, deleted: bool = None, spam: bool = None, size: int = None,
                      skip: int = None, order_by: str = None) -> any:
        """
        endpoint doc: https://youscan.docs.apiary.io/#reference/mention-stream/fetching-mentions/list-mentions?console=1
        :param topic_id: int
        :param from_date: str
        :param to_date: str
        :param sentiment: str
        :param exclude_sentiment: str
        :param sources: str
        :param exclude_sources: str
        :param tags: str
        :param exclude_tags: str
        :param auto_categories: str
        :param exclude_auto_categories: str
        :param starred: bool
        :param tagged: bool
        :param processed: bool
        :param deleted: bool
        :param spam: bool
        :param size: int
        :param skip: int
        :param order_by: str
        :return: any
        """
        url = f"{self.API_URL}/topics/{topic_id}/mentions/?apiKey={self.token}"
        params = {}
        local_params = locals()
        local_params.pop('self', None)
        for param, value in local_params.items():
            if value is not None:
                params[self._create_param(param)] = value
        url += '&' + urlencode(params)
        return self._send_api_request('get', url)

    def _get_statistic(self, obj: str, topic_id: int, from_date: str, to_date: str,
                       data: dict = {}, extra_url_params: dict = {}) -> any:
        url = f"{self.API_URL}/topics/{topic_id}/statistics/{obj}?apiKey={self.token}"
        params = {
            'from': from_date,
            'to': to_date,
        }
        if extra_url_params:
            params.update(**extra_url_params)
        url += '&' + urlencode(params)
        print(url)
        return self._send_api_request('get', url=url, data=data)

    def get_sentiments_statistic(self, topic_id: int, from_date: str, to_date: str) -> any:
        """
        endpoint doc - https://youscan.docs.apiary.io/#reference/statistics/sentiment/get?console=1
        :param topic_id: int
        :param from_date: str
        :param to_date: str
        :return: any or raise YouScanException
        """
        return self._get_statistic('sentiments', topic_id, from_date, to_date)

    def get_tags_statistic(self, topic_id: int, from_date: str, to_date: str):
        """
        endpoint doc - https://youscan.docs.apiary.io/#reference/statistics/tags/get?console=1
        :param topic_id: int
        :param from_date: str
        :param to_date: str
        :return: any or raise YouScanException
        """
        return self._get_statistic('tags', topic_id, from_date, to_date)

    def get_words_statistic(self, topic_id: int, from_date: str, to_date: str) -> any:
        """
        endpoint doc - https://youscan.docs.apiary.io/#reference/statistics/wordcloud/get?console=1
        :param topic_id: int
        :param from_date: str
        :param to_date: str
        :return: any or raise YouScanException
        """
        return self._get_statistic('words', topic_id, from_date, to_date)

    def get_regions_sentiments_statistic(self, topic_id: int, from_date: str, to_date: str,
                                         size: int = None, country: str = None) -> any:
        """
        endpoint doc - https://youscan.docs.apiary.io/#reference/statistics/sentiment-by-regions/get?console=1
        :param topic_id: int
        :param from_date: str
        :param to_date: str
        :param size: int
        :param country: str
        :return: any or raise YouScanException
        """
        extra_url_params = {}
        if size:
            extra_url_params['size'] = size
        if country:
            extra_url_params['country'] = country
        return self._get_statistic('regions-sentiments', topic_id, from_date, to_date,
                                   extra_url_params=extra_url_params)

    def get_sources_sentiments_statistic(self, topic_id: int, from_date: str, to_date: str,
                                         size: int = None) -> any:
        """
        endpoint doc - https://youscan.docs.apiary.io/#reference/statistics/sentiment-by-sources/get?console=1
        :param topic_id: int
        :param from_date: str
        :param to_date: str
        :param size: int
        :return: any or raise YouScanException
        """
        extra_url_params = {}
        if size:
            extra_url_params['size'] = size
        return self._get_statistic('sources-sentiments', topic_id, from_date, to_date,
                                   extra_url_params=extra_url_params)

    def get_sources_by_regions_sentiments_statistic(self, topic_id: int, from_date: str, to_date: str,
                                                    sources_size: int = None, regions_size: int = None) -> any:
        """
        endpoint doc - https://youscan.docs.apiary.io/#reference/statistics/sentiment-by-sources-by-regions/get?console=1
        :param topic_id: int
        :param from_date: str
        :param to_date: str
        :param sources_size: int
        :param regions_size: int
        :return: any or raise YouScanException
        """
        extra_url_params = {}
        if sources_size:
            extra_url_params['sourcesSize'] = sources_size
        if regions_size:
            extra_url_params['regionsSize'] = regions_size
        return self._get_statistic('regions-sources-sentiments', topic_id, from_date, to_date,
                                   extra_url_params=extra_url_params)

    def get_histogram_statistic(self, topic_id: int, from_date: str, to_date: str) -> any:
        """
        endpoint doc - https://youscan.docs.apiary.io/#reference/statistics/histogram/get?console=1
        :param topic_id: int
        :param from_date: str
        :param to_date: str
        :return: any or raise YouScanException
        """
        return self._get_statistic('histogram', topic_id, from_date, to_date)

    def get_trends_statistic(self, topic_id: int, from_date: str, to_date: str) -> any:
        """
        endpoint doc - https://youscan.docs.apiary.io/#reference/statistics/trends/get?console=1
        :param topic_id: int
        :param from_date: str
        :param to_date: str
        :return: any or raise YouScanException
        """
        return self._get_statistic('trends', topic_id, from_date, to_date)

    def get_genders_statistic(self, topic_id: int, from_date: str, to_date: str) -> any:
        """
        endpoint doc - https://youscan.docs.apiary.io/#reference/statistics/genders/get?console=1
        :param topic_id: int
        :param from_date: str
        :param to_date: str
        :return: any or raise YouScanException
        """
        return self._get_statistic('genders', topic_id, from_date, to_date)

    def get_ages_statistic(self, topic_id: int, from_date: str, to_date: str) -> any:
        """
        endpoint doc - https://youscan.docs.apiary.io/#reference/statistics/ages/get?console=1
        :param topic_id: int
        :param from_date: str
        :param to_date: str
        :return: any or raise YouScanException
        """
        return self._get_statistic('ages', topic_id, from_date, to_date)

    def get_links_statistic(self, topic_id: int, from_date: str, to_date: str, sort: str = None) -> any:
        """
        endpoint doc - https://youscan.docs.apiary.io/#reference/statistics/links/get?console=1
        :param topic_id: int
        :param from_date: str
        :param to_date: str
        :param sort: str
        :return: any or raise YouScanException
        """
        extra_url_params = {}
        if sort:
            extra_url_params['sort'] = sort
        return self._get_statistic('links', topic_id, from_date, to_date, extra_url_params=extra_url_params)

    def get_authors_statistic(self, topic_id: int, from_date: str, to_date: str, sort: str = None) -> any:
        """
        endpoint doc - https://youscan.docs.apiary.io/#reference/statistics/authors/get?console=1
        :param topic_id: int
        :param from_date: str
        :param to_date: str
        :param sort: str
        :return: any or raise YouScanException
        """
        extra_url_params = {}
        if sort:
            extra_url_params['sort'] = sort
        return self._get_statistic('authors', topic_id, from_date, to_date, extra_url_params=extra_url_params)

    def get_publication_places_statistic(self, topic_id: int, from_date: str, to_date: str, sort: str = None) -> any:
        """
        endpoint doc - https://youscan.docs.apiary.io/#reference/statistics/publication-places/get?console=1
        :param topic_id: int
        :param from_date: str
        :param to_date: str
        :param sort: str
        :return: any or raise YouScanException
        """
        extra_url_params = {}
        if sort:
            extra_url_params['sort'] = sort
        return self._get_statistic('publication-places', topic_id, from_date, to_date,
                                   extra_url_params=extra_url_params)
