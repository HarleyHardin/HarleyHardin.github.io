# read and analyze login attempts from a security log file
# report total login attempts, successful logins, and failed logins
# reports Failed attempts by IP address
# consider a IP address as suspicious if it has 3 or more failed login attempts
# identify the username with the most failed login attempts
# prints a security report

# colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def load_security_log(file_path):
    log_entries = []
    with open(file_path) as f:
        for line in f:
            log_entries.append(line.strip())
    return log_entries

file_path = input("Path to Log_File.txt: ")
log_entries = load_security_log(file_path)
total_attempts = len(log_entries)
successful_logins = sum(1 for entry in log_entries if "SUCCESS" in entry)
failed_logins = sum(1 for entry in log_entries if "FAILED" in entry)

failed_attempts_by_ip = {}
for entry in log_entries:
    if "FAILED" in entry:
        ip = entry.split(",")[-2]
        if ip not in failed_attempts_by_ip:
            failed_attempts_by_ip[ip] = 0
        failed_attempts_by_ip[ip] += 1

suspicious_ips = [ip for ip, count in failed_attempts_by_ip.items() if count >= 3]

failed_attempts_by_username = {}
for entry in log_entries:
    if "FAILED" in entry:
        username = entry.split(",")[0]
        if username not in failed_attempts_by_username:
            failed_attempts_by_username[username] = 0
        failed_attempts_by_username[username] += 1

most_failed_user = max(failed_attempts_by_username, key=failed_attempts_by_username.get) if failed_attempts_by_username else None

print("\nSecurity Report")
print(f"Total login attempts: {total_attempts}")
print(f"Successful logins: {GREEN}{successful_logins}{RESET}")
print(f"Failed logins: {RED}{failed_logins}{RESET}")
print("\nFailed attempts by IP:")
for ip, count in failed_attempts_by_ip.items():
    print(f"{ip}: {RED}{count}{RESET}")
print("\nSuspicious IPs (3 or more failed attempts):")
if len(suspicious_ips) == 0:
    print("No suspicious IPs detected")
else:
    for ip in suspicious_ips:
        print(f"{YELLOW}{ip}{RESET}")

print(f"\nUsername with the most failed login attempts: {YELLOW}{most_failed_user}{RESET}")
