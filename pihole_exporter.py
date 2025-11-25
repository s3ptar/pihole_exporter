"""#####################################################################
#! @ file:                   pihole_exporter.py
#  @ projekt:                pihole_exporter 
#  @ created on:             2025 11 16
#  @ author:                 R. Gräber
#  @ version:                0
#  @ history:                -
#  @ brief
#####################################################################"""

"""#####################################################################
# Includes
#####################################################################"""
import logging
import sys
import json
import requests
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
"""#####################################################################
# Informations
#####################################################################"""
# https://influxdb-python.readthedocs.io/en/latest/examples.html
# https://docs.influxdata.com/influxdb/cloud/api-guide/client-libraries/python/
"""#####################################################################
# Declarations
#####################################################################"""

requests_urls = [
    "/stats/summary", 
    "/info/version", 
    "/stats/upstreams", 
    "/stats/top_domains?blocked=true&count=20",
    "/stats/top_clients?blocked=true&count=20",
    "/stats/recent_blocked?count=20"
]

"""#####################################################################
# Constant
#####################################################################"""


"""#####################################################################
# Global Variable
#####################################################################"""


"""#####################################################################
# local Variable
#####################################################################"""
logger = logging.getLogger(__name__)
pi_hole_session_id = ""
"""#####################################################################
# Constant
#####################################################################"""

"""#####################################################################
# Local Funtions
#####################################################################"""

"""#####################################################################
#! @fn           write_summary_data(url, bucket, org, measurement, data, key="", tag="")
#  @ brief       write summary to influxdb
#  @ param       none
#  @ exception   none
#  @ return      none
#####################################################################"""
def write_summary_data(url, bucket, org, measurement, data, key="", tag=""):

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )
    
    # auf daten prüfen und ggf weiter absteigen
    
    # -------------- queries ----------------------------------------------
    point = influxdb_client.Point(measurement)
    point.tag("location", "home")
    point.tag("summary", "queries")
    point.field("total", int(summary_data['queries']['total']))
    point.field("percent_blocked", int(summary_data['queries']['percent_blocked']))
    point.field("unique_domains", int(summary_data['queries']['unique_domains']))
    point.field("forwarded", int(summary_data['queries']['forwarded']))
    point.field("frequency", int(summary_data['queries']['frequency']))
    point.field("cached", int(summary_data['queries']['cached']))
    point.field("frequency", int(summary_data['queries']['frequency']))
    point.time(datetime.now())

    write_api = client.write_api(write_options=SYNCHRONOUS)  
    write_api.write(bucket, org, record=point)

    # -------------- queries - types ----------------------------------------------
    point = influxdb_client.Point(measurement)
    point.tag("location", "home")
    point.tag("summary", "queries")
    point.tag("queries", "types")
    for type in summary_data['queries']['types']:
        point.field(type, int(summary_data['queries']['types'][type]))
    point.time(datetime.now())
    write_api = client.write_api(write_options=SYNCHRONOUS)  
    write_api.write(bucket, org, record=point)

    # -------------- queries - status ----------------------------------------------
    point = influxdb_client.Point(measurement)
    point.tag("location", "home")
    point.tag("summary", "queries")
    point.tag("queries", "status")
    for state in summary_data['queries']['status']:
        point.field(state, int(summary_data['queries']['status'][state]))
    point.time(datetime.now())
    write_api = client.write_api(write_options=SYNCHRONOUS)  
    write_api.write(bucket, org, record=point)

    # -------------- queries - replies ----------------------------------------------
    point = influxdb_client.Point(measurement)
    point.tag("location", "home")
    point.tag("summary", "queries")
    point.tag("queries", "replies")
    for reply in summary_data['queries']['replies']:
        point.field(reply, int(summary_data['queries']['status'][reply]))
    point.time(datetime.now())
    write_api = client.write_api(write_options=SYNCHRONOUS)  
    write_api.write(bucket, org, record=point)

    # -------------- clients ----------------------------------------------
    point = influxdb_client.Point(measurement)
    point.tag("location", "home")
    point.tag("summary", "clients")
    for client in summary_data['clients']:
        point.field(client, int(summary_data['clients'][client]))
    point.time(datetime.now())
    write_api = client.write_api(write_options=SYNCHRONOUS)  
    write_api.write(bucket, org, record=point)

    # -------------- gravity ----------------------------------------------
    point = influxdb_client.Point(measurement)
    point.tag("location", "home")
    point.tag("summary", "gravity")
    for grav in summary_data['gravity']:
        point.field(client, int(summary_data['gravity'][grav]))
    point.time(datetime.now())
    write_api = client.write_api(write_options=SYNCHRONOUS)  
    write_api.write(bucket, org, record=point)
    
    # 
    #for fields in data:
    #    point.tag(key, fields) if key != "" else None
    #    # prüfen ob noch mehr daten in den feldern sind
    #    if isinstance(data[fields], dict):
    #        # ja => rekursiver aufruf
    #        write_summary_data(url, bucket, org, measurement, data[fields], key=fields)
    #    else:
    #        point.field(fields, int(data[fields]))
    #        
        #    for field in summary_data[tags]:
        #            point = influxdb_client.Point("pihole_metrics")
        #            point.tag("type", req.strip('/').replace('/', '_'))
        #            point.tag("category", tags)
        #            point.field(field, summary_data[tags][field])
        #            point.time(datetime.now())
        #            p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 25.3)
    #point.time(datetime.now())
    
    
    logger.debug(f"Written point: {point.to_line_protocol()}")

    



"""#####################################################################
#! @fn          int main(){
#  @ brief       start up function
#  @ param       none
#  @ exception   none
#  @ return      none
#####################################################################"""

if __name__ == "__main__":

    ### ---------- read config ---------- ###

    try:
        with open("config.json") as json_data:
            d = json_data.read()
            # js = json.loads('{"mqtt_server_url" : "homedeb.local","mqtt_server_port" : 1883,"mqtt_server_topic" : "stfc"}')
            js = json.loads(d)
    
    except Exception as e:
        print(f"Error reading config file: {e}")
        sys.exit(1)

    ### ---------- config logging ---------- ###
    log_lvl = js['logging']['level'].upper()
    log_path = js['logging']['log_path']
    logging.basicConfig(
        #filename='myapp.log',
        format='%(asctime)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]',
        level=log_lvl,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(log_path), # Log messages to a file
            logging.StreamHandler(sys.stdout) # Log messages to the console (stdout)
        ]
    )
    logger.info('Started')

    ### ---------- read pihole sid ---------- ###
    url = f"http://{ js['pihole']['host'] }/api/auth"
    payload = {
        "password": f"{ js['pihole']['webpasword'] }"
    }

    response = requests.post(url, json=payload, verify=False)
    logger.debug(response.json())
    try:
        pi_hole_session_id = response.json()['session']['sid']
        logger.debug(f" sid is : { pi_hole_session_id }")
    except Exception as e:
        logger.error(f"Error reading pihole sid: {e}")
        sys.exit(1)
 

    # ------ DB connection prepare ------   

    bucket = js['influxdb']['bucket']
    org = js['influxdb']['org']
    token = js['influxdb']['token']
    # Store the URL of your InfluxDB instance
    url=js['influxdb']['url']
    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )
    write_api = client.write_api(write_options=SYNCHRONOUS)  

    # ------ Daten abfragen ------
    summary_payload = {"sid": pi_hole_session_id}   # SID muss im Body stehen

    for req in js['pihole']['request_config']:
        
        # prüfen ob summaray abgerufen werden soll
        if js['pihole']['request_config'][req] == 1 and "summary" in req:
            logger.debug(f"process { req } data")
            summary_url = f"http://{ js['pihole']['host'] }/api/stats/summary"
            summary_response = requests.get(summary_url, json=summary_payload, verify=False)
            summary_data = summary_response.json()

            write_summary_data(url, bucket, org, "summary", summary_data, key="type")


    #for req in api_requests:
    #for req in js['pihole']['requests']:
    #    summary_url = f"http://{ js['pihole']['host'] }/api{ req }"
    
    #    summary_response = requests.get(summary_url, json=summary_payload, verify=False)
    #    summary_data = summary_response.json()
        
    #    create_influx_fields(bucket, org, summary_data, "summary")
        
    #    logger.debug(f"Request:{ req }")

        #logger.debug(f"Summary-Daten:{ summary_url }")
        #logger.debug(f"Summary-Daten:{ summary_data }")

        # ------ Daten in InfluxDB schreiben ------
          
        

        #if req == '/stats/summary':
        #    # ------ InfluxDB Verbindung ------
        #    influx_client = InfluxDBClient(
        #        url=js['influxdb']['url'],
        #        token=js['influxdb']['token'],
        #        org=js['influxdb']['org']
        #    )
        #    write_api = influx_client.write_api()

        #    point = (
        #        Point("pihole_summary")
        #        .field("dns_queries_today", int(summary_data.get("dns_queries_today", 0)))
        #        .field("ads_blocked_today", int(summary_data.get("ads_blocked_today", 0)))
        #        .field("ads_percentage_today", float(summary_data.get("ads_percentage_today", 0)))
        #        .field("domains_being_blocked", int(summary_data.get("domains_being_blocked", 0)))
        #        .time(datetime.now())
        #    )
        #    write_api.write(bucket=js['influxdb']['bucket'], org=js['influxdb']['org'], record=point)


    logger.info('Finished')

