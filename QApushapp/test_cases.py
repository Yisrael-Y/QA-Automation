def generate_test_cases(first_email, additional_emails, first_phone_id, additional_phone_ids, absolute_private_key_path, absolute_logfile_path, port):
    # List of test cases with types included
    test_cases = [
        # Test case: Sending an email notification
        {"type": "email", "case": f"-e {first_email} -d \"Test Email Notification\" -t 60 -k \"{absolute_private_key_path}\" -z {port} -i private"},
        # Test case: Sending an email notification to multiple recipients
        {"type": "email", "case": f"-e {first_email} {additional_emails} -d \"Test Email Notification\" -t 60 -k \"{absolute_private_key_path}\" -z {port} -i private"},
        
        # Test case: Sending a push notification to a single phone ID
        {"type": "phone", "case": f"-p {first_phone_id} -d \"Test Push Notification\" -t 60 -k \"{absolute_private_key_path}\" -z 1234 -i private"},
        # Test case: Sending a push notification to multiple phone IDs
        {"type": "phone", "case": f"-p {first_phone_id} {additional_phone_ids} -d \"Test Push Notification\" -t 60 -k \"{absolute_private_key_path}\" -z {port} -i private"},
        # Test case: Sending a location-based notification
        {"type": "phone", "case": f"-p {first_phone_id} -d \"Test Location-based Notification\" -t 60 -k \"{absolute_private_key_path}\" -w.lat 11 -w.lon 16 -z {port} -i private"},
        # Test case: Sending a notification with logging
        {"type": "phone", "case": f"-p {first_phone_id} -d \"Test Logging\" -t 60 -k \"{absolute_private_key_path}\" --LOG -f \"{absolute_logfile_path}\" -z {port} -i private"},
        # Test case: Sending approval notifications to multiple phone IDs
        {"type": "phone", "case": f"-p {first_phone_id} {additional_phone_ids} -d \"Test Approvals\" -t 60 -k \"{absolute_private_key_path}\" -o.digits 5 -o.algorithm SHA-256 -m 2 -z {port} -i private"},
        
        # Test case: Sending mixed email and push notifications
        {"type": "both", "case": f"-p {first_phone_id} -e {first_email} -d \"Test Mixed Notifications\" -t 60 -k \"{absolute_private_key_path}\" -z {port} -i private"},
        # Test case: Sending a TOTP (Time-based One-Time Password) notification
        {"type": "both", "case": f"-p {first_phone_id} -e {first_email} -d \"Test TOTP\" -t 60 -k \"{absolute_private_key_path}\" --TOTP -o.digits 6 -o.algorithm SHA-512 -o.secret TOTPSecret123 -z {port} -i private"},
        # Test case: Sending a notification with a config file
        {"type": "both", "case": f"-p {first_phone_id} -e {first_email} -d \"Test Config File\" -t 60 -b -k \"{absolute_private_key_path}\""},
        # Test case: Sending a notification with a config file and specific use
        # {"type": "both", "case": f"-p {first_phone_id} -e {first_email} -d \"Test Config File Use\" -t 60 -c {absolute_path} -k \"{absolute_private_key_path}\" -z {port} -i private"}, 
        # Test case: Testing background execution
        {"type": "both", "case": f"-b -k \"{absolute_private_key_path}\""},
        # ... (add more test cases here)
    ]
    return test_cases