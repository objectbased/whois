#! /bin/python/env
# Author: github.com/rush-dev

import requests
import argparse

parser = argparse.ArgumentParser(
    description='This utility performs a GET request to arin.net to perform queries on IP addresses and returns the output to the terminal.'
)

# Required arguments
required = parser.add_argument_group('required arguments')
required.add_argument(
    "-i",
    "--ip",
    help="parses a single IP address.",
    action="store",
    type=str,
    required=True)

args = parser.parse_args()

# Main code

# First GET request with IP

ip_request = requests.get(f'http://whois.arin.net/rest/ip/{args.ip}.json')
ip_response = ip_request.json()

# IP network categories

start_address = ip_response['net']['startAddress']['$']
end_address = ip_response['net']['endAddress']['$']
handle = ip_response['net']['handle']['$']
name = ip_response['net']['name']['$']
org_name = ip_response['net']['orgRef']['@name']
org_handle = ip_response['net']['orgRef']['@handle']
last_updated = ip_response['net']['updateDate']['$']
rest_link = ip_response['net']['ref']['$']

# Second GET request with organization name

org_request = requests.get(f'https://whois.arin.net/rest/org/{org_handle}.json')
org_response = org_request.json()

# Organization categories

city = org_response['org']['city']['$']
postal = org_response['org']['postalCode']['$']
country = org_response['org']['iso3166-1']['code2']['$']
org_last_updated = org_response['org']['updateDate']['$']
org_rest_link = org_response['org']['ref']['$']

# Try statements to catch commonly blank fields and differences in indexing on ARIN's side

try:
    cidr = ip_response['net']['netBlocks']['netBlock']['cidrLength']['$']

except TypeError:
    cidr = ip_response['net']['netBlocks']['netBlock'][0]['cidrLength']['$']

try:
    net_type = ip_response['net']['netBlocks']['netBlock']['description']['$']

except TypeError:
    net_type = ip_response['net']['netBlocks']['netBlock'][0]['description']['$']

try:
    parent_name = ip_response['net']['parentNetRef']['@name']
    parent_handle = ip_response['net']['parentNetRef']['@handle']

except KeyError:
    parent_name = ''
    parent_handle = ''

try:
    origin_as = ip_response['net']['originASes']['originAS'][0]['$']

except KeyError:
    origin_as = ''

try:
    reg_date = ip_response['net']['registrationDate']['$']

except KeyError:
    reg_date = ''

try:
    org_reg_date = org_response['org']['registrationDate']['$']

except KeyError:
    org_reg_date = ''

try:
    state = org_response['org']['iso3166-2']['$']

except KeyError:
    state = ''

try:
    street = org_response['org']['streetAddress']['line']['$']

except TypeError:
    street = org_response['org']['streetAddress']['line'][0]['$']

# Output to terminal
print(f'You searched for: {args.ip}\n')
print('Network')
print(f'NetRange:         {start_address} - {end_address}')
print(f'CIDR:             {start_address}/{cidr}')
print(f'Name:             {name}')
print(f'Handle:           {handle}')
print(f'Parent:           {parent_name} ({parent_handle})')
print(f'NetType:          {net_type}')
print(f'OriginAS:         {origin_as}')
print(f'Organization:     {org_name} ({org_handle})')
print(f'RegistrationDate: {reg_date}')
print(f'LastUpdated:      {last_updated}')
print(f'RESTful Link:     {rest_link}\n')
print('Organization')
print(f'Name:             {org_name}')
print(f'Handle:           {org_handle}')
print(f'Street:           {street}')
print(f'City:             {city}')
print(f'State/Province:   {state}')
print(f'PostalCode:       {postal}')
print(f'Country:          {country}')
print(f'RegistrationDate: {org_reg_date}')
print(f'LastUpdated:      {org_last_updated}')
print(f'RESTful Link:     {org_rest_link}')
