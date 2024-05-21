import os
import asyncio
import logging
import redis
from featureflags.client import CfClient
from featureflags.evaluations.auth_target import Target
from featureflags.config import Config

# Set DJANGO_SETTINGS_MODULE environment variable to None
os.environ['DJANGO_SETTINGS_MODULE'] = ''

# Initialize a Redis client with the specified host and password
r = redis.Redis(
    host='redis-10120.c321.us-east-1-2.ec2.redns.redis-cloud.com',
    port=10120,
    db=0,
    password='vw7NTK5m3dsYKPg6E5eb1oKXKzCFPLU9',
    decode_responses=True
)

# Initialize logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Initialize feature flag keys
keys = ["GitHubActionsFlag", "Flag2"]

# Function to handle feature flag value changes
def onFeatureFlagValueChanged(featureFlagName, previousValue, currentValue):
    if previousValue != currentValue:
        log.info(f"Feature flag value: {featureFlagName} has changed from {previousValue} to {currentValue}")
        flag_value = 1 if currentValue else 0
        r.set(featureFlagName, flag_value)

# Function to continuously check feature flag status
async def checkFFStatus():
    log.info("Harness SDK Getting Started")
    api_key = "2718c06a-a451-4d73-ad10-cfcf168a8e94"
    # api_key2 = "6cf39c1b-4d5d-4fc2-9a84-e37c67a3d1f8"  # API key for featureflagvalue2

    # Create a Feature Flag Client
    client = CfClient(api_key, Config(enable_stream=False, enable_analytics=False, pull_interval=1))
    client.wait_for_initialization()

    # Create a target (different targets can get different results based on)
    target = Target(identifier='Naresh')

    # Loop forever reporting the state of the flag. If there is an error,
    # the default value will be returned
    while True:
        for eachKey in keys:
            result = client.bool_variation(eachKey, target, False)
            onFeatureFlagValueChanged(eachKey, r.get(eachKey), result)

        await asyncio.sleep(1)

# Run the checkFFStatus function
asyncio.run(checkFFStatus())