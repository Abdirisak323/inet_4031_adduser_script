#!/usr/bin/python3

# INET4031
# Abdirisak Abdullahi
# 03/18/2026
# 03/18/2026

# Import OS module to execute Linux system commands
# Import re module for pattern matching (used to detect comment lines)
# Import sys module to read input from standard input (stdin)
import os
import re
import sys


def main():
    for line in sys.stdin:

        # Check if the line starts with '#' which indicates a comment line and should be skipped
        match = re.match("^#",line)

        # Split the input line into fields using ':' as the delimiter
        fields = line.strip().split(':')

        # Skip the line if it is a comment or does not contain exactly 5 fields
        if match or len(fields) != 5:
            continue

        # Extract username, password, and user information (gecos) from the input fields
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3],fields[2])

        # Split the groups field by ',' to allow multiple group assignments
        groups = fields[4].split(',')

        # Display message indicating a new user account is being created
        print("==> Creating account for %s..." % (username))
        # Build the Linux command to create a user with no password and set user details
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos,username)


        print(cmd)
        os.system(cmd)

        # Display message indicating the password is being set for the user
        print("==> Setting the password for %s..." % (username))
        # Build the command to set the user's password using echo and passwd
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password,password,username)

        print(cmd)
        os.system(cmd)

        for group in groups:
            # Assign the user to each group if the group is not '-'
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username,group))
                cmd = "/usr/sbin/adduser %s %s" % (username,group)
                print(cmd)
                os.system(cmd)

if __name__ == '__main__':
    main()
