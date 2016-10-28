#This script plots observations for up to 10 emesh stations for a given date range
#Use by typing "python emesh_plot.py [stations] [date range]" at the command line.
#Station numbers are 2-digit station codes seperated by commas
#Date range is YYYYMMDD,YYYYMMDD
#
#Example:
#python emesh_plot.py"
#Please enter station numbers as 'SN,SN,...'
#01, 02, 03
#Please enter desired date range as 'YYYYMMDD,YYYYMMDD or just YYYYMMDD if only one day
#20161023
#--END EXAMPLE--
#
#Written by Christopher Phillips
#
#Future plans
#Allow for date ranges to transition years

#Importing necessary modules
import datetime
import matplotlib.pyplot as pp
import numpy
import sys

#Set appropriate file path here (directory where all station directories are located)
#Station directories MUST be "station_SN"
filep = "/home/christopher/Documents/work/emesh/data/"

#Asking user for input
stations = input("Please enter station numbers as 'SN,SN,...'\n")
date_range = input("Please enter desired date range as 'YYYYMMDD,YYYYMMDD' or just YYYYMMDD if only one day\n")

#Extracting user station numbers and dates from user input
stations = (stations).replace(" ","").split(",")
date_range = (date_range).replace(" ","").split(",")


#Computing dates within date range
#Start by computing day of year
day1 = datetime.datetime.strptime(date_range[0], "%Y%m%d").timetuple().tm_yday
day2 = datetime.datetime.strptime(date_range[-1], "%Y%m%d").timetuple().tm_yday

#Accounting for transitions between years
if (day2 < day1):
	eoy_day = datetime.datetime.strptime(date_range[0][0:4]+"1231", "%Y%m%d").timetuple().tm_yday
	day2 += eoy_day
#Find days in that range
days = numpy.arange(day1, day2+1)
if (day2 < day1):
	days[days > eoy_day] -= eoy_day

#Transform back to dates
year1 = (date_range[0])[0:4]
year2 = (date_range[-1])[0:4]
dates = []
year_flag = True
for d in range(len(days)):
	#Accounting for transitions between years	
	if (year_flag):
		dates.append(datetime.datetime.strptime(year1+","+str(days[d]), "%Y,%j").strftime("%Y%m%d"))
	else: 
		dates.append(datetime.datetime.strptime(year2+","+str(days[d]), "%Y,%j").strftime("%Y%m%d"))

	if ((d != len(days)-1) and (days[d] > days[d+1])):
		year_flag = False

#Extracting data from files
data = [] #Array to hold data for each station
for s in range(len(stations)):
	#Creating empty lists
	time = []
	sht_temp = []
	sht_rh = []
	bmp_pres = []
	wind_spd = []
	wind_dir = []
	rain = []
	for d in range(len(dates)):
		fn = open(filep+"station_"+stations[s]+"/"+dates[d][2:]+stations[s]+".TXT")
		for line in fn:
			if ((line[0] == "#") or (line == "\n")):
				continue
			else:
				dummy = line.split() #Seperating emesh data
				#Extracting time
				time.append(float(dummy[3])+float(dummy[4])/60.0+float(dummy[5])/3600.0+24*d)
				
				#Extracting data
				wind_dummy = float(dummy[12])
				sht_temp.append(float(dummy[8]))	#'C
				sht_rh.append(float(dummy[9]))	#%
				bmp_pres.append(float(dummy[6]))	#hPa
				wind_spd.append(float(dummy[11])) 	#m/s
				wind_dir.append(10**(-6)*wind_dummy**3-0.0026*wind_dummy**2+1.6681*wind_dummy) #deg
				rain.append(float(dummy[10])*0.2) #mm
		
	#Plotting
	colors = ['black','red','green','blue','brown','violet','goldenrod','navy','hotpink','gray']
	xaxis = [0,24*len(dates)]	
	if (len(dates) < 4): #Hours between tick labels
		dt = 6
	else:
		dt = 12

	#Temperature
	pp.subplot(2,3,1)
	pp.plot(time, sht_temp, colors[s])
	pp.title("Temperature ('C)")
	#pp.ylim(0,35)
	pp.xlim(xaxis)
	pp.xticks(numpy.arange(0,24*len(dates)+dt,dt))
	pp.grid(True)

	#Pressure
	pp.subplot(2,3,2)
	pp.plot(time, bmp_pres, colors[s])
	pp.title("Pressure (hPa)")
	#pp.ylim(980, 1020)
	pp.xlim(xaxis)
	pp.xticks(numpy.arange(0,24*len(dates)+dt,dt))
	pp.grid(True)

	#Wind speed
	pp.subplot(2,3,3)
	pp.plot(time, wind_spd, colors[s])
	pp.title("Wind Speed (m/s)")
	pp.xlim(xaxis)
	pp.xticks(numpy.arange(0,24*len(dates)+dt,dt))
	pp.grid(True)

	#Relative Humidity
	pp.subplot(2,3,4)
	pp.plot(time, sht_rh, colors[s])
	pp.title("RH (%)")
	pp.ylim(0,100)
	pp.xlim(xaxis)
	pp.xticks(numpy.arange(0,24*len(dates)+dt,dt))
	pp.grid(True)

	#Rainfall
	pp.subplot(2,3,5)
	pp.plot(time, rain, colors[s])
	pp.title("Rainfall (mm)")
	pp.xlim(xaxis)
	pp.xticks(numpy.arange(0,24*len(dates)+dt,dt))
	pp.grid(True)

	#Wind Direction
	pp.subplot(2,3,6)
	pp.plot(time[0:-1:8], wind_dir[0:-1:8], colors[s], ls="dotted")
	pp.title("Wind Direction (')")
	pp.ylim(0,360)
	pp.xlim(xaxis)
	pp.xticks(numpy.arange(0,24*len(dates)+dt,dt))
	pp.grid(True)
	
pp.suptitle(dates[0])
pp.show()
	#Storing each station in the data array for plotting.
	#data.append({'time':time, 'sht_temp':sht_temp, 'sht_rh':sht_rh, 'bmp_pres':bmp_pres,
	#	'wind_spd':wind_spd, 'wind_dir':wind_dir, 'rain':rain})


