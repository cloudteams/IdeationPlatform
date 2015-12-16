import json
import requests

__author__ = 'dipap'


GEOCODE_API = 'https://maps.googleapis.com/maps/api/geocode/'


address_info_cache = {}


def get_address_info(address):
    """
    Returns GoogleMaps-style info about an address
    Caches the results without ever expiring them
    """
    api_key = 'AIzaSyB5sKctUXR02OXbxJ5WQOXn_ehJLYWpzTI'

    if address in address_info_cache:
        return address_info_cache[address]
    else:
        result = json.loads(requests.get(GEOCODE_API + 'json?address=%s&sensor=true&key=%s' %
                                         (address, api_key)).content)
        address_info_cache[address] = result
        return result


def address_to_city__helper(address, info=None):
    if not info:
        info = get_address_info(address)

    if not info['results']:
        return '', info

    city_name = ''
    for component in info['results'][0]['address_components']:
        if 'administrative_area_level_3' in component['types']:
            city_name = component['long_name']
        elif 'administrative_area_level_5' in component['types']:
            city_name = component['long_name']

        if city_name:
            break

    return city_name, info


def address_to_city(*args):
    """
    Given an address, detect the city where this address is located
    """
    address = zip(*args)[0][0]
    if not address:
        return ''

    return address_to_city__helper(address)[0]


def address_to_country__helper(address, info=None):
    if not info:
        info = get_address_info(address)

    if not info['results']:
        return '', info

    country_name = ''
    for component in info['results'][0]['address_components']:
        if 'country' in component['types']:
            country_name = component['long_name']

        if country_name:
            break

    return country_name, info


def address_to_country(*args):
    """
    Given an address, detect the country where this address is located
    """
    address = zip(*args)[0][0]
    if not address:
        return ''

    return address_to_country__helper(address)[0]


def address_to_city_country(*args):
    address = zip(*args)[0][0]
    if not address:
        return ''

    city, info = address_to_city__helper(address)
    if not city:
        city = ''

    country, _ = address_to_country__helper(address, info)
    if not country:
        country = ''

    if city and country:
        return city + ', ' + country
    else:
        return city + country
