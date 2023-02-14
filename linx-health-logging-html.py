import paramiko
import datetime

# Set the IP address and credentials for the remote server
ip_address = "139.144.4.252"
username = "root"
password = "P@ssw0rd123"

# Connect to the remote server using Paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip_address, username=username, password=password)

# Create a log file for appending logs
now = datetime.datetime.now()
log_file_name = "log_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
log_file = open(log_file_name, "a")

# Log the SSH connection time
log_file.write("SSH connection successful at " + str(now) + "\n")

# Define a function to execute commands and log output
def execute_command(command, message):
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode().strip()
    log_file.write(message + "\n" + output + "\n")
    return output

# Execute commands and log output
uptime = execute_command("uptime", "System uptime:")
os_version = execute_command("uname -a", "Operating system version:")
cpu_utilization = execute_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'", "CPU utilization:")
load_average = execute_command("cat /proc/loadavg", "Load average:")
mem_utilization = execute_command("free | awk 'FNR == 2 {print $3/($3+$4)*100}'", "Memory utilization:")
disk_utilization = execute_command("df -h", "Disk utilization:")
network_utilization = execute_command("iftop -t -s 1", "Network utilization:")
active_users = execute_command("who", "Active users:")

# Get the status of specific services
service_status = ""
services = ["sshd", "ntpd", "httpd"]
for service in services:
    output = execute_command(f"systemctl is-active {service}", f"{service} status:")
    service_status += f"{service} - {output}\n"

# Generate an HTML report of the health check results
html_file_name = "output_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".html"
html_file = open(html_file_name, "w")
html_file.write("<html><body>")
html_file.write("<h1>Server Health Check</h1>")
html_file.write("<h2>Status of Specific Services:</h2>")
html_file.write("<pre>" + service_status + "</pre>")
html_file.write("<h2>System Uptime:</h2>")
html_file.write("<pre>" + uptime + "</pre>")
html_file.write("<h2>Operating System Version:</h2>")
html_file.write("<pre>" + os_version + "</pre>")
html_file.write("<h2>CPU Utilization:</h2>")
html_file.write("<pre>" + cpu_utilization + "</pre>")
html_file.write("<h2>Load Average:</h2>")
html_file.write("<pre>" + load_average + "</pre>")
html_file.write("<h2>Memory Utilization:</h2>")
html_file.write("<pre>" + mem_utilization + "</pre>")
html_file.write("<h2>Disk Utilization:</h2>")
html_file.write("<pre>" + disk_utilization + "</pre>")
html_file.write("<h2>Network Utilization:</h2>")
html_file.write("<pre>" + network_utilization + "</pre>")
