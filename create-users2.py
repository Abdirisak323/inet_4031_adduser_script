#!/usr/bin/python3
# INET4031
# 03/18/2026
# 03/18/2026

# Import OS module to execute Linux system commands
# Import re module for pattern matching (used to detect comment lines)
# Import sys module to read input from standard input (stdin)
import os
import re
import sys
# This script supports a "dry-run" mode.
# In dry-run mode, the script will print the commands instead of executing them.
# This allows the user to test what will happen without making any changes to the system.

def main():
# dry_run controls whether commands are executed or just displayed
# True = print commands only (no changes made)
# False = execute commands on the system
    dry_run = False

    for line in sys.stdin:

        match = re.match("^#", line)
        fields = line.strip().split(':')

        if match or len(fields) != 5:
            if dry_run:
                print("Skipping invalid line:", line.strip())
            continue

        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])
        groups = fields[4].split(',')

        print("==> Creating account for %s..." % username)
# If dry_run is enabled, print the command instead of creating the user
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)

        if dry_run:
            print("DRY RUN:", cmd)
        else:
            os.system(cmd)

# If dry_run is enabled, print the password command instead of executing it
        print("==> Setting the password for %s..." % username)
# If dry_run is enabled, print the command instead of creating the user
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)

        if dry_run:
            print("DRY RUN:", cmd)
        else:
            os.system(cmd)
# If dry_run is enabled, print the group assignment command instead of executing it
        for group in groups:

            if group == '-':
                if dry_run:
                    print("Skipping group assignment for", username)
                continue

            print("==> Assigning %s to the %s group..." % (username, group))
# If dry_run is enabled, print the command instead of creating the user
            cmd = "/usr/sbin/adduser %s %s" % (username, group)

            if dry_run:
                print("DRY RUN:", cmd)
            else:
                os.system(cmd)

if __name__ == '__main__':
    main()
