import argparse

def parse_args():
    """Parse command-line arguments for required tag key and value.
    
    This function sets up an ArgumentParser to handle user inputs for customizing
    the tagging behavior, such as specifying the key and value for the required tag.
    It defines default values if no arguments are provided and returns the parsed args.
    """
    parser = argparse.ArgumentParser(description='AWS S3 Tagging Enforcer - Applies required tags to buckets.')
    parser.add_argument('--required_key', type=str, default='CostCenter', help='Required tag key (default: CostCenter).')
    parser.add_argument('--required_value', type=str, default='FinOps', help='Required tag value (default: FinOps).')
    return parser.parse_args()

def enforce_tags(buckets, required):
    """Enforce tags on buckets, logging before/after states and count of changes.
    
    This function iterates through a list of mock buckets, checks for the presence of
    a required tag key, adds it if missing, logs the changes, and returns the count
    of buckets that were updated. It prints the state of buckets before and after tagging
    to demonstrate the enforcement process.
    """
    tagged_count = 0
    print("Before:")
    for b in buckets:
        print(f"{b['Name']}: {b['Tags']}")

    for bucket in buckets:
        # If required key missing, add it and increment count
        if required['Key'] not in bucket['Tags']:
            bucket['Tags'][required['Key']] = required['Value']
            tagged_count += 1
            print(f"Tagged {bucket['Name']} with {required['Key']}: {required['Value']}")

    print("\nAfter:")
    for b in buckets:
        print(f"{b['Name']}: {b['Tags']}")
    return tagged_count

if __name__ == "__main__":
    args = parse_args()
    tag_required = {'Key': args.required_key, 'Value': args.required_value}  # Define required tags, renamed to avoid shadowing
    s3_buckets = [  # Define mock buckets, renamed to avoid shadowing
        {'Name': 'data-bucket', 'Tags': {}},
        {'Name': 'logs-bucket', 'Tags': {'CostCenter': 'Ops'}},
        {'Name': 'backup-bucket', 'Tags': {'CostCenter': 'FinOps'}}
    ]
    count = enforce_tags(s3_buckets, tag_required)
    # If no tags added, print compliance message
    if count == 0:
        print("All buckets already compliant.")
