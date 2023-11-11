import requests
import json
import sys
import os

def validate_license_key(key):
  validation = requests.post(
    "https://api.keygen.sh/v1/accounts/{}/licenses/actions/validate-key".format(os.environ['KEYGEN_ACCOUNT_ID']),
    headers={
      "Content-Type": "application/vnd.api+json",
      "Accept": "application/vnd.api+json"
    },
    data=json.dumps({
      "meta": {
        "key": key
      }
    })
  ).json()

  if "errors" in validation:
    errs = validation["errors"]

    print(
      "license validation failed: {}".format(
        '\n'.join(map(lambda e: "{} - {}".format(e["title"], e["detail"]).lower(), errs))
      )
    )

    return

  valid = validation["meta"]["valid"]
  code = validation["meta"]["code"]
  detail = validation["meta"]["detail"]
  id = None

  if validation["data"]:
    id = validation["data"]["id"]

  if valid:
    print(
      "license is valid: detail={} code={} id={}".format(detail, code, id)
    )
  else:
    print(
      "license is invalid: detail={} code={} id={}".format(detail, code, id)
    )

# Run from the command line:
#   python main.py some_license_key
key = sys.argv[1]

validate_license_key(key)
