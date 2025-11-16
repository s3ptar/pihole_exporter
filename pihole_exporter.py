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
"""#####################################################################
# Informations
#####################################################################"""

"""#####################################################################
# Declarations
#####################################################################"""



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


"""#####################################################################
# Constant
#####################################################################"""

"""#####################################################################
# Local Funtions
#####################################################################"""





"""#####################################################################
#! @fn          int main(){
#  @ brief       start up function
#  @ param       none
#  @ exception   none
#  @ return      none
#####################################################################"""

if __name__ == "__main__":

    ### ---------- config logging ---------- ###

    logging.basicConfig(
        #filename='myapp.log',
        format='%(asctime)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler("myapp.log"), # Log messages to a file
            logging.StreamHandler(sys.stdout) # Log messages to the console (stdout)
        ]
    )
    logger.info('Started')

    ### ---------- read config ---------- ###

    try:
        with open("config.json") as json_data:
            d = json_data.read()
            # js = json.loads('{"mqtt_server_url" : "homedeb.local","mqtt_server_port" : 1883,"mqtt_server_topic" : "stfc"}')
            js = json.loads(d)
    
        logger.debug(f"host is {js['pihole']['host']}")
    except Exception as e:
        logger.error(f"Error reading config file: {e}")
        sys.exit(1)

    ### ---------- read pihole sid ---------- ###
    url = f"http://{ js['pihole']['host'] }/api/auth"
    payload = {
        "password": f"{js['pihole']['webpasword'] }"
    }

    response = requests.post(url, json=payload, verify=False)
    logger.debug(response.json())
    pi_hole_respose_sid = response.json()['session']['sid']
    logger.debug(f" sid is : { pi_hole_respose_sid }")

    logger.info('Finished')

