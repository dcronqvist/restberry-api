from flask_restx import Resource, Namespace
from api_v1 import privilege_required
import requests as req
import config as conf

api = Namespace("pihole", description="Information about dani's pihole")

doc = """
### Get current status of the PiHole dani is hosting in his home network.

Returns information regarding how many DNS queries that have been done today, how many of those that were blocked etc.

#### Privileges
- pihole

"""

@api.route("/status")
class PiHoleResource(Resource):

    @api.doc("pihole_status_get", description=doc)
    @api.response(200, "Status retrieved and returned.")
    @api.response(500, "Address to PiHole not correctly setup in config.")
    @privilege_required("pihole")
    def get(self):
        """Get pihole status"""

        address = conf.get_setting("pihole-address", None)
        if not address:
            return { "error": "PiHole address not set up correctly in config." }, 500
        result = req.get(address)
        try:
            j = result.json()
            return { "status": j }, 200
        except:
            return { "error": "PiHole address not set up correctly in config." }, 500