# Import modules
# Using SUDS from https://fedorahosted.org/suds/
from suds.client import Client
from pyspeak import Channel
# read the config file

# Now we have the right variables
# Read the settings from the settings file
    settings_file = open(settings_file)
    # e.g. "/dev/ttyUSB0"
    settings_line = settings_file.readline().rstrip('\n').split(',')
    port = settings_line[0]
    baud = eval(settings_line[1])
    par = settings_line[2]
    byte = eval(settings_line[3])
    ceol = settings_line[4]
    if ceol == 'r':
        eol = b'\r'
    elif ceol == 'nr':
        eol = b'\n\r'
    else:
        eol = b'\n'
    logger.info(port)
    # path for data files
    # e.g. "/home/logger/datacpc3010/"
    datapath = settings_file.readline().rstrip('\n')
    logger.info(datapath)
    filetimeformat = settings_file.readline().rstrip('\n').split(',')
    logger.info(filetimeformat)
    # Short or long file name format
    if (filetimeformat[0] == 'short'):
        fnamefmt = "%Y%m%d.tsv"
    else:
        fnamefmt = "%Y-%m-%d.tsv"
    # Read the compressing flag
    flags = settings_file.readline().rstrip().split(',')
    # Close the settings file
    settings_file.close()

user = 'Gustavo'
pwd = 'Olivares'
url = 'http://neon.unidata.com.au/NeonWebService.asmx?WSDL'
node1 = '6381'
node2 = '6385'
target = 'http://api.thingspeak.com'
channel1 = 172186
readkey1 = 'IG053Q3OX1WKLEDB'
writekey1 = 'B3O1AJ2MIVA0Y53Y'
channel2 = 172188
readkey2 = 'GY6X15Y9R0WZYEHC'
writekey2 = '5ZTWOPTZSAOR1TUV'

# Initialise the SOAP client
client = Client(url)

# Fetch data
hoani = client.service.GetChannelList(user, pwd, '6381', 0)
prospect = client.service.GetChannelList(user, pwd, '6385', 0)

# Initialise the dictionary to update the thingspeak channels
# fields = ['Wind Speed','Wind Direction','Temperature','Relative Humidity','Gust Speed']
options1 = {}
options2 = {}

# Go for Hoani Waititi
options1["field1"] = eval(hoani.diffgram[0].DocumentElement[
                          0].Neon_x0020_Channels[0].Last_Value[0])
options1["field2"] = eval(hoani.diffgram[0].DocumentElement[
                          0].Neon_x0020_Channels[4].Last_Value[0])
options1["field3"] = eval(hoani.diffgram[0].DocumentElement[
                          0].Neon_x0020_Channels[3].Last_Value[0])
options1["field4"] = eval(hoani.diffgram[0].DocumentElement[
                          0].Neon_x0020_Channels[5].Last_Value[0])
options1["field5"] = eval(hoani.diffgram[0].DocumentElement[
                          0].Neon_x0020_Channels[8].Last_Value[0])

hoani_TS = Channel(channel1, '', target, readkey1, writekey1)
hoani_TS.update_channel(options1)

# Go for Prospect
options2["field1"] = eval(prospect.diffgram[0].DocumentElement[
                          0].Neon_x0020_Channels[4].Last_Value[0])
options2["field2"] = eval(prospect.diffgram[0].DocumentElement[
                          0].Neon_x0020_Channels[1].Last_Value[0])
options2["field3"] = eval(prospect.diffgram[0].DocumentElement[
                          0].Neon_x0020_Channels[0].Last_Value[0])
options2["field4"] = eval(prospect.diffgram[0].DocumentElement[
                          0].Neon_x0020_Channels[8].Last_Value[0])
options2["field5"] = eval(prospect.diffgram[0].DocumentElement[
                          0].Neon_x0020_Channels[6].Last_Value[0])

prospect_TS = Channel(channel2, '', target, readkey2, writekey2)
prospect_TS.update_channel(options2)
