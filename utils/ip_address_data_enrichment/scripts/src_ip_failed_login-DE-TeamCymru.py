#!/usr/bin/env python
'''
GPLv3 License

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see https://www.gnu.org/licenses/.

Copyright (C) 2022 Stephen Scally /  www.threatlocus.com


Imports
-------

os:       Module used for input / output files.
Pandas:   Module used for dataframes(df).
Numpy:    Module used for NaN and dataframe functionality.
dns.*:    Module used to create, store, and work with DNS queries to
          TeamCymru DNS endpoint.
rich.*:   Module used to provide status feedback and functionality to
          this script.
logging:  Python logging handler.
'''

import os
import logging
import argparse
import pandas as pd
import numpy as np
import dns.query, dns.message, dns.reversename, dns.resolver
from rich.progress import track
from rich.logging import RichHandler


def cymru_dns_q(_ip_addrs):

  '''
  Parameters
  ----------
  _ip_addrs:
      List of all source IP addresses from the inital dataset.

  Returns
  -------
  lookup_list:
      List with ASN, BGP Prefix, Country Code, RIR, Allocation Date, AS Description, and AS Peers.

  Notes
  -----
  Each IP address is queried for related information using TeamCymru
  IP to ASN mapping service.

  https://www.team-cymru.com/ip-asn-mapping

  The DNS lookup functionality is used to query data for the respective
  v4 or v6 IP address. Additionally, BGP peers of the specific IP address
  are also queried.

  In order to use the DNS lookup functionality we need to perform the
  following:

  1. Loop through each IP address in the source IP address list and build an entry
     of reversed octect v4/v6 query to the respective IPv4 and IPv6 endpoints.

     Example query v4:
     dig +short 31.108.90.216.origin.asn.cymru.com TXT

     Example query v6:
     dig +short 8.6.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.2.0.0.b.0.6.8.4.1.0.0.2.origin6.asn.cymru.com. TXT
    
  2. Check the return code of the query as all IP addresses may not have an entry or a lookup can timeout. 
     We need to create a row entry regardless so that the index mapping of the dataframes is consistant.
     This allows us to merge the dataframes later into one.

  3. With a successful response code we can parse the returned answer into the information we
     want.

     We extract the ASN associated with the returned IP adddress query and perform a lookup
     to the ASN domain endpoint (.asn.cymru.com)

     We extract the list of AS peers as seen through BGP from the respective IP address.

  4. With the inital IP address query data, AS Description and list of peer AS's a dictionary entry
     is created for each IP address queried. The list is returned and stored as a pandas dataframe.

  '''

  v4_reverse_dom = dns.name.from_text("origin.asn.cymru.com.")
  v6_reverse_dom = dns.name.from_text("origin6.asn.cymru.com.")
  peer_dom = dns.name.from_text("peer.asn.cymru.com.")
  asn_dom = ".asn.cymru.com"
  sys_resolvers = dns.resolver.get_default_resolver().nameservers

  lookup_list = []

  # Status / time tracking
  log.info("Starting IP address DNS query")

  for ip in track(_ip_addrs, "Querying IP Data"):
    # IP query to get  AS number, BGP prefix, Country Code, RIR, Alocation Date
    query_ip = dns.reversename.from_address(ip, v4_reverse_dom, v6_reverse_dom)
    query_ip_mesg = dns.message.make_query(query_ip, dns.rdatatype.TXT)
    query_ip_response = dns.query.udp(query_ip_mesg, sys_resolvers[0])

    # Check rcode.
    if query_ip_response.rcode() == 0:

      query_ip_answer = str(query_ip_response.answer[0][0]).replace('"', "").split("|")

      # ASN query to obtain AS description
      query_asn = 'AS' + str(query_ip_answer[0]).strip() + asn_dom
      query_asn_mesg = dns.message.make_query(query_asn, dns.rdatatype.TXT)
      query_asn_response = dns.query.udp(query_asn_mesg, sys_resolvers[0])
      query_asn_answer = str(query_asn_response.answer[0][0]).replace('"', "").split("|")

      # Peer query
      query_peer = dns.reversename.from_address(ip, peer_dom, peer_dom)
      query_peer_mesg = dns.message.make_query(query_peer, dns.rdatatype.TXT)
      query_peer_response = dns.query.udp(query_peer_mesg, sys_resolvers[0])
      query_peer_answer = str(query_peer_response.answer[0][0]).replace('"', "").split("|")

      # Build list of dictionaries for the response
      # 0 - ASN, 1 - BGP Prefix, 2 - Country Code, 3 - RIR, 4 - Allocation Date, 5 - AS Description, 6 - AS Peers
      lookup_list.append({'ASN': query_ip_answer[0].strip(), 'BGP Prefix': query_ip_answer[1].strip(), 'Country Code': query_ip_answer[2].strip(), 
                          'RIR': query_ip_answer[3].strip(), 'Allocation Date': query_ip_answer[4].strip(), 'AS Description': query_asn_answer[4].strip(),
                          'AS Peers': query_peer_answer[0].strip()})
    else:
      # NaN is used as its pandas criteria for working with the dropna functionality
      # See https://pandas.pydata.org/docs/user_guide/missing_data.html#missing-data
      lookup_list.append({'ASN': np.NaN, 'BGP Prefix': np.NaN, 'Country Code': 'None', 
                          'RIR': 'None', 'Allocation Date': np.NaN, 'AS Description': 'None'
                          'AS Peers': np.NaN})

  return lookup_list



def main():

  # Collect user input
  parser = argparse.ArgumentParser(
            description="Data Enrichment (DE) of IP address datasets using TeamCymru.",
            epilog="See http://threatlocus.com/blog/ip-address-data-enrichment-team-cymru/")

  parser.add_argument('--input-file', '-if',
                      nargs='?',
                      default=os.path.abspath("../datasets/download/src_ip_address_failed_login_attempts.txt"),
                      help='Specifies an alternative input filename. (csv format)')
  parser.add_argument('--output-file', '-of',
                      nargs='?',
                      default=os.path.abspath("../datasets/generated/src_ip_failed_login_attempts_team_cymru_ip_to_asn_mapped.csv"),
                      help='Specifies an alternatvie output filename. (csv format)')
  parser.add_argument('--quiet', '-q', action='store_true', default=False,
                      help='Only outputs the query progress to TeamCymru. Overrides --debug')

  parser.add_argument('--debug', '-d', action='store_true',
                      help='Enable debug logging output.')

  args = parser.parse_args()

  # Logging Handler
  global log
  FORMAT = "%(asctime)s - %(message)s"
  LOGLEVEL=logging.INFO

  if args.debug and not args.quiet:
      LOGLEVEL=logging.DEBUG

  if args.quiet:
      LOGLEVEL=logging.WARNING

  logging.basicConfig(level=LOGLEVEL,format=FORMAT, datefmt=None, handlers=[RichHandler(show_time=False)])
  log = logging.getLogger("rich")
  log.debug("Global logger configured.")
  log.debug(log)

  # Verify provided arguments
  log.debug('Provided commandline arguments: %s', args)

  # This is our source of questionable IP addresses
  log.info("Reading source dataset, creating dataframe.")
  log.debug("Input file is: %s", os.path.abspath(args.input_file))
  df_ip_address = pd.read_csv(args.input_file,
                              delim_whitespace=1,
                              names=['ip_count','src_ip'])

  # Extract ip_address column into list
  log.info("Create src_ip list from dataframe.")
  ip_addr_lst = df_ip_address["src_ip"].tolist()

  # Dataframe of queried data
  log.info("Call TeamCymru lookup function.")
  df_ip_address_data = pd.DataFrame(cymru_dns_q(ip_addr_lst))

  # Status / time tracking
  log.info("Finished IP address DNS query")

  # Concatnate datasets
  log.info("Concatnate both datasets")
  all_data = pd.concat([df_ip_address,df_ip_address_data], axis=1)

  ## Generate Enriched Dataset
  log.info("Writing dataset to new file.")
  log.debug("Output file is: %s", os.path.abspath(args.output_file))
  all_data.to_csv(args.output_file,
                  index=False)


if __name__ == "__main__":
    main()

