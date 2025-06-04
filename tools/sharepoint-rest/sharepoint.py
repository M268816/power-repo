import json
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext

with open("./config.json") as login:
    CONFIG = json.load(login)

SITE_URL = "https://mdigital.sharepoint.com/sites/RaysTest"
CLIENT_ID = "60e8bab6-20b4-45d0-8dc5-4ffd09319d77"
CLIENT_SECRET = "971fcf5e-c4c2-4742-aab3-049447749349"
TENANT_ID = "db76fb59-a377-4120-bc54-59dead7d39c9"
USERNAME = CONFIG["username"]
PASSWORD = CONFIG["password"]

ctx = AuthenticationContext(SITE_URL)

try:
    if ctx.acquire_token_for_user(USERNAME, PASSWORD):
    # if ctx.acquire_token_for_app(CLIENT_ID, CLIENT_SECRET):
        print("Authenticated.")
    else:
        print("ERROR: Did not authenticate.")
        exit()
except Exception as e:
    print(f"Authentication Exception: {e}")
    exit()

client = ClientContext(SITE_URL, ctx)

try:
    lists = client.web.lists
    print(f"Lists: {lists}")

    client.load(lists)
    client.execute_query()

    for sp_list in lists:
        print(f"List Title: {sp_list.properties['Title']}")
except Exception as e:
    print(f"Error loading lists: {e}")
    
print("--- FINISHED ---")
exit()