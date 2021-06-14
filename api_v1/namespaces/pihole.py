from flask_restx import Resource, Namespace
from api_v1 import privilege_required
import requests as req
import config as conf

api = Namespace("pihole", description="Information about dani's pihole")

class PiHole(object):
    def __init__(self):
        pass


ph = PiHole()

@api.route("/status")
class PiHoleResource(Resource):
    '''Get PiHole status'''

    @api.doc("pihole_status_get", description="## Get the current status of the PiHole dani is hosting in his home network.")
    @api.response(200, "Status retrieved and returned")
    @api.response(500, "Address to PiHole not correctly setup in config.")
    @privilege_required("pihole")
    def get(self):
        address = conf.get_setting("pihole-address", None)
        if not address:
            return { "error": "PiHole address not set up correctly in config" }, 500
        result = req.get(address)
        try:
            j = result.json()
            return { "status": j }, 200
        except:
            return { "error": "PiHole address not set up correctly in config" }, 500