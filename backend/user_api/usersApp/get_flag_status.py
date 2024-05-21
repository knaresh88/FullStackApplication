import redis

r = redis.Redis(host='redis-10120.c321.us-east-1-2.ec2.redns.redis-cloud.com', 
                port=10120, db=0, 
                password='vw7NTK5m3dsYKPg6E5eb1oKXKzCFPLU9',
                decode_responses=True)

githubaction_flag_status = int(r.get("GitHubActionsFlag") or 0)
featureflagvalue2_flag_status = int(r.get("Flag2") or 0)

print(githubaction_flag_status, featureflagvalue2_flag_status)

# Check if both feature flags are set to 1 in Redis
def check_flag_status():
    githubaction_value = int(r.get('GitHubActionsFlag') or 0)
    featureflagvalue2_value = int(r.get('Flag2') or 0)
    # return githubaction_value == 1 and featureflagvalue2_value == 1
    return githubaction_value == 1 and featureflagvalue2_value == 1

if __name__ == "__main__":
    # Check the status of the feature flags
    if check_flag_status():
        # If both flags are set to 1, print 'success' to trigger GitHub Actions workflow
        print("success")