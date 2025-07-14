import os
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import json

PUBLIC_KEY = os.environ["DISC_PUBLIC_KEY"]

def lambda_handler(event, context):

    signature = event.get("headers").get("x-signature-ed25519")
    timestamp = event.get("headers").get("x-signature-timestamp")
    strBody = event.get("body")

    if signature is None or timestamp is None:
        return {
            "statusCode": 401,
            "body": json.dumps("Missing signature or timestamp header"),
        }

    try:
        verifyKey = VerifyKey(bytes.fromhex(PUBLIC_KEY))
        verifyKey.verify(
            (timestamp + strBody).encode(),
            bytes.fromhex(signature)
        )
    except BadSignatureError:
        return {
            "statusCode": 401,
            "body": json.dumps("Bad Public Key"),
        }

    data = json.loads(strBody)

    # Discord ping response 
    # https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-interaction-callback-type
    if data.get("type") == 1:
        return {
            "statusCode": 200,
            "body": json.dumps({"type": 1}),
        }

    # handle /foo command
    if data.get("data").get("name") == "foo":
        return json.dumps({
            "type": 4,
            "data": {"content": "bar"}
        })

    # default to 200 response because we received something
    return {
        "statusCode": 200,
        "body": json.dumps("Received other request..."),
    }