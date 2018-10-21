#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
import csv

from math import sin, cos, sqrt, atan2, radians

from lib.arcgis_client import ArcGISClient

CSV_DELIMITER = ','
ARCGIS_BASE_URL = 'http://geocode.arcgis.com/arcgis/rest/services'  # <-- should be in .conf file


class AddressController(object):
    """ Address API controller object"""
    def __init__(self, logger):
        self.logger = logger

    def get_address(self, input_file):
        """
        Parse input csv file, validate it.
        Then, get address names by coordinates from ArcGIS service and calculate all possible distances
        between geo points, excluding duplication.
        :param input_file: csv file
        :return: dictionary object: {'points': [...], 'links': [...]}
        """
        try:
            parsed_input_file = csv.reader(input_file, delimiter=CSV_DELIMITER)
        except csv.Error as e:
            self.logger.debug('Unable to parse input file: %s' % e)
            raise ValueError('invalid_csv_file_format')

        self.logger.debug('Getting address names and distances')

        output_dict = {'points': [], 'links': []}
        temporary_list = []
        row_counter = 0
        for row in parsed_input_file:
            row_counter += 1
            if row_counter == 1:
                continue  # skip header

            row = self._validate_row(row, row_counter)

            # Get human readable address form ArcGis:
            arcgis_client = ArcGISClient(base_url=ARCGIS_BASE_URL)
            result = arcgis_client.get_address_name(row[1], row[2])
            if isinstance(result, tuple):
                if result[0] in ('requests_error', 'api_error'):
                    self.logger.error('Unexpected error occurred while trying to '
                                      'get address from ArcGIS service:\n %s' % result[1])
                    raise RuntimeError('unable_to_get_address')

                self.logger.error('Unable to get address name from ArcGis for coordinates: %s, %s!\n'
                                  'Error: %s' % (row[1], row[2], result[1]))
                raise ValueError('unable_to_get_address')

            # Append geo point info to result dict:
            output_dict['points'].append({'name': row[0], 'address': result['address']['LongLabel']})

            # Calculate distances between current geo point and others:
            temporary_list.append({'name': row[0], 'lat': row[1], 'lon': row[2]})
            for other_point in temporary_list:
                if row[0] != other_point['name']:

                    distance = self._calculate_distance(row[1], row[2], other_point['lat'], other_point['lon'])
                    output_dict['links'].append({'name': row[0]+other_point['name'], 'distance': distance})

        return output_dict

    @staticmethod
    def _calculate_distance(lat1, lon1, lat2, lon2):
        """ Calculate distance(meters) between two geo points """
        earth_r = 6373.0  # approximate radius of earth in km

        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        d_lon = lon2 - lon1
        d_lat = lat2 - lat1

        a = sin(d_lat / 2)**2 + cos(lat1) * cos(lat2) * sin(d_lon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = earth_r * c  # km
        distance = distance * 1000
        return round(distance, ndigits=2)

    def _validate_row(self, row, row_counter):
        """ Validate row from input csv file """
        if len(row) != 3:
            self.logger.error('Invalid format of row %s in input file!' % row_counter)
            raise ValueError('invalid_csv_file_format')

        try:
            row[0] = str(row[0])
            row[1] = float(row[1])
            row[2] = float(row[2])
        except ValueError:
            self.logger.error('Invalid values in row %s of input file!!' % row_counter)
            raise ValueError('invalid_csv_file_format')

        return row
