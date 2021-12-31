#####################################################################################
# Change the variable acu_ipv4 to the correct IP addresss
#
# Add the line below to the crontab
# */20 * * * * /usr/bin/env python /root/gps/GPSscraper.py >/dev/null 2>&1
#
# MariConnect ehf
#####################################################################################
import os, argparse
import json
from datetime import date
from datetime import datetime

#Arguments url username password
parser = argparse.ArgumentParser()
parser.add_argument("url")
parser.add_argument("username")
parser.add_argument("password")
args = parser.parse_args()

#declaring variables
path = "/tmp/"
filename_r = args.username+"_index.html"
filename_w = args.username+"_position.txt"
zabbix_pos = args.username+"_zabbix_pos.txt"
password_list = ["D6v6\"%\"3DUCS\"", "slept-gb2e%25\""]

#Downloading ACU HTML page
#Times out after 60 seconds to prevent hangups
if "213." in "url":
        #Telenor ACU
        os.system("curl --max-time 60 http://" +args.url+ "\"/?pageId=login\" -H \"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0\" -H \"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\" -H \"Accept-Language: en-US,en;q=0.5\" --compressed -H \"Content-Type: application/x-www-form-urlencoded\" -H \"Origin: http://"+args.url+"\" -H \"Connection: keep-alive\" -H \"Referer: http://"+args.url+"\" -H \"Cookie: tt_adm=deleted\" -H \"Upgrade-Insecure-Requests: 1\" --data \"user_login=admin&pass_login="+password_list[0]+" -o "+path+filename_r)
elif "81.85." in "url":
        #Speedcast ACU
        os.system("curl --max-time 60 http://" +args.url+ "\"/?pageId=login\" -H \"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0\" -H \"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\" -H \"Accept-Language: en-US,en;q=0.5\" --compressed -H \"Content-Type: application/x-www-form-urlencoded\" -H \"Origin: http://"+args.url+"\" -H \"Connection: keep-alive\" -H \"Referer: http://"+args.url+"\" -H \"Cookie: tt_adm=deleted\" -H \"Upgrade-Insecure-Requests: 1\" --data \"user_login=admin&pass_login="+password_list[1]+" -o "+path+filename_r)
else:
        #Other telenor ACU with IP address that doesn't start in 213.
        os.system("curl --max-time 60 http://" +args.url+ "\"/?pageId=login\" -H \"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0\" -H \"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\" -H \"Accept-Language: en-US,en;q=0.5\" --compressed -H \"Content-Type: application/x-www-form-urlencoded\" -H \"Origin: http://"+args.url+"\" -H \"Connection: keep-alive\" -H \"Referer: http://"+args.url+"\" -H \"Cookie: tt_adm=deleted\" -H \"Upgrade-Insecure-Requests: 1\" --data \"user_login=admin&pass_login="+password_list[0]+" -o "+path+filename_r)

#Testing that HTML page can be opened
#If it can be opened, connection made and downloaded successfully
#If it fails terminate this program
try:
        fh = open(path+filename_r,'r')
except:
        print("Couldn't connect to ACU")
        quit()

#Declaring positional variables
latitude2 = ""
longitude2 = ""
knots = "0"
heading = ""

#Zabbix - declaring variables
signal_lvl = "no_data"
reference = "no_data"
rx_freq = "no_data"
tx_freq = "no_data"
tx_allowed = "no_data"
software_ver = "no_data"

#Formatting the date
raw_today = date.today()
modified_year = str(raw_today)[2:4]
modified_month = str(raw_today)[5:7]
modified_day = str(raw_today)[8:10]
todays_day = modified_day+modified_month+modified_year

a = datetime.now()
time_now = "%02d%02d%02d" % (a.hour,a.minute,a.second)
span = list()
lati = list()
longi = list()
lines = fh.readlines()
sat_pos = ""


#Formatting heading, latitude and longitude to correct format
for line in lines:
    if "Vessel heading" in line:
        span    = line.split(" ")
        heading = span[12]
        heading = heading.rstrip()
        heading = heading[13:]
        heading = heading.rstrip("&deg;</span>")
    elif "Satellite position" in line:
        span    = line.split(" ")
        sat_pos = span[12]
        sat_pos = sat_pos[24:]
        sat_pos = sat_pos.rstrip("&deg;")
        try:
            sat_pos = sat_pos + " " + span[13][0]
        except:
            pass
    elif "GNSS position" in line:
            span       = line.split(" ")
        latitude   = span[12]
        latitude   = latitude[19:]
        latitude   = latitude.rstrip("&deg;")
        latitude2  =  span[13]
        latitude2  = latitude2[0:1]
        longitude  = span[14]
        longitude  = longitude[0:5]
        longitude2 = span[15]
        longitude2 = longitude2[0:1]
#Zabbix - gathering data
    elif "Signal level" in line:
        span    = line.split(" ")
        signal_lvl = span[12]
        signal_lvl = signal_lvl.rstrip()
        signal_lvl = signal_lvl[18:]
        signal_lvl = signal_lvl.rstrip("&deg;</span>")
        print(signal_lvl)
    elif "Reference" in line:
        span    = line.split(" ")
        reference = span[12]
        reference = reference.rstrip()
        reference = reference.rstrip("&deg;</span>")
        print(reference)
    elif "RX IF" in line:
        span    = line.split(" ")
        rx_freq = span[13]
        rx_freq = rx_freq.rstrip()
        rx_freq = rx_freq[21:]
        rx_freq = rx_freq.rstrip("&deg;</span>")
        print(rx_freq)
    elif "TX IF" in line:
        span    = line.split(" ")
        tx_freq = span[13]
        tx_freq = tx_freq.rstrip()
        tx_freq = tx_freq[21:]
        tx_freq = tx_freq.rstrip("&deg;</span>")
        print(tx_freq)
    elif "TX allowed" in line:
        span    = line.split(" ")
        tx_allowed = span[12]
        tx_allowed = tx_allowed.rstrip()
        tx_allowed = tx_allowed[16:]
        tx_allowed = tx_allowed.replace("</span>", "")
        tx_allowed = tx_allowed.rstrip("&deg;")
        print(tx_allowed)
    elif "Software version" in line:
        span    = line.split(" ")
        software_ver = span[12]
        software_ver = software_ver.rstrip()
        software_ver = software_ver[25:]
                software_ver += "-" + span[13] + "-" + span[14]
        software_ver = software_ver.rstrip("&deg;</span>\n")
        print(software_ver)


fh.close()
print("sat pos: "+sat_pos)
print("heading: "+heading)
#Displaying the values
print "latitude",latitude
print "longitude",longitude

lati = latitude.split(".")
longi = longitude.split(".")

nr_latitude = float(lati[1])

nr_latitude = nr_latitude*0.6
if nr_latitude < 10:
    lati[1] = "0"+str(nr_latitude)
else:
    lati[1] = str(nr_latitude)
latitude = lati[0]+lati[1]
print latitude

if "&" in longi[1]:
    longi[1] = longi[1].rstrip("&")
nr_longitude = float(longi[1])
nr_longitude = nr_longitude*0.6
if nr_longitude < 10:
    longi[1] = "0"+str(nr_longitude)
else:
    longi[1] = str(nr_longitude)
longitude = longi[0]+longi[1]
print longitude

#Write the current position to a file ([vessel]_position.txt)
fh = open(path+filename_w,"w")
fh.write("$GPRMC,"+time_now+",A,"+latitude+","+latitude2+","+longitude+","+longitude2+","+knots+","+heading+","+todays_day+",,")
fh.close()

#Runnes the gps.php script to send position from the [vessel]_position.txt file to GPStracker
os.system("php /root/gpstracker/gps.php "+args.username+" "+args.password+" "+path+filename_w)

#Write satellite position to a file
file = open("/root/gpstracker/satpos.txt", "a")
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#Writing position to file
file.write(now)
file.write("\n")
file.write(args.username)
file.write("\n")
file.write("Satellite position: " + sat_pos)
file.write("\n")
file.write("Heading: " + heading)
file.write("\n\n")
#Close file
file.close()

#Zabbix - creating dictionary
#zabbix_dict = { '{#V_NAME}':args.username,'{#SIGNAL_LVL}':signal_lvl,'{#REFERENCE}':reference,'{#RX_FREQ}':rx_freq,'{#TX_FREQ}':tx_freq,'{#TX_ALLOWED}':tx_allowed,'{#SOFTWARE_VER}':software_ver }
zabbix_list = [signal_lvl,reference,rx_freq,tx_freq,tx_allowed,software_ver]

#Zabbix - converting dictionary into JSON and editing formatting to have plain text
#zabbix_json = json.dumps(zabbix_dict)
#zabbix_json = zabbix_json.replace(" ", "")
#zabbix_json = zabbix_json.replace("\n", "")
#zabbix_json = zabbix_json.replace("{", "")
#zabbix_json = zabbix_json.replace("}", "")
#zabbix_json = zabbix_json.replace("[", "")
#zabbix_json = zabbix_json.replace("]", "")
#zabbix_json = zabbix_json.replace(":", "")
#zabbix_json = zabbix_json.replace("\"", "")
#zabbix_json = zabbix_json.replace(",", "")



#Zabbix - write formated "JSON" to file
file = open("/root/gpstracker/zabbix/" + args.username, "w")
file.write(' '.join(zabbix_list))
file.close()


#Remove HTML page
#Allows try-catch to run properly on line 41
os.system("rm "+path+filename_r)                                                                  
