"""
ArcGIS web service client
"""
import requests
import json

GET_ADDRESS_NAME_ENDPOINT = '/World/GeocodeServer/reverseGeocode?' \
                            'location=%s&langCode=en&outSR=&forStorage=false&f=pjson'


class ArcGISClient(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def get_address_name(self, latitude, longitude):
        """ Get geo address name by geo point coordinates """
        try:
            location = str(latitude)+'%2C'+str(longitude)
            response = requests.get(self.base_url + GET_ADDRESS_NAME_ENDPOINT % location)

            if not response.ok:
                return response.status_code, json.loads(response.content)

            result = json.loads(response.content)
            if result.get('error'):
                return int(result['error']['code']), result['error']['message']

            return result

        except requests.RequestException as e:
            return 'requests_error', e.message

        except StandardError as e:
            return 'api_error', e.message

    # other methods of ArcGIS api below...
    # ...
