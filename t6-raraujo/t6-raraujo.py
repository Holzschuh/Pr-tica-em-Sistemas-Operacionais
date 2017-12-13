#!/usr/bin/env python3

import sys
import json
import requests
from collections import Counter

def removeDuplicates(list):
	newList = []
	for i in list:
		if i not in newList:
			newList.append(i)
	return newList

def makeCountTuple(l):
	l2 = []
	l3 = []
	for i in l:
		l2.append(l.count(i))
	for i in range(len(l)):
		l3.append((l2[i], l[i]))
	return l3

def getLocation(top10):
	url = "https://ipapi.co/"
	top10WithLocation = []
	for ip in top10:
		response = requests.get(url + ip[0] + "/json")
		city = "not found"
		country = "not found"
		try:
			l = (json.loads(response.text))
			country = (l['country_name'])
			city = (l['city'])
			
		except:
			pass
		
		top10WithLocation.append((ip[0], ip[1], city, country))
	return top10WithLocation

def getIpData(l):
	counts = Counter(l)
	counts = list(counts.items())
	counts.sort(key=lambda i: i[1], reverse = True)

	top10 = counts[:10]
	
	top10 = getLocation(top10)

	return top10

def part1(file):
	text = file.readlines()
	packages = len(text)
	print("Total of packages: " + str(packages))

def part2(file):
	top10 = []
	ips = []
	counts = []
	text = file.readlines()
	for line in text:
		if 'SRC=' in line:
			line = line.split('SRC=')[1].split(' ')[0]
			ips.append(line)
	top10 = getIpData(ips)
	for ip in top10:
		print(ip)

	return createChart('Countries from top 10 used source ips:', 'Source', top10, 2)



def part3(file):
	top10 = []
	ips = []
	counts = []
	text = file.readlines()
	for line in text:
		if 'DST=' in line:
			line = line.split('DST=')[1].split(' ')[0]
			ips.append(line)
	top10 = getIpData(ips)
	for ip in top10:
		print(ip)

	return createChart('Countries from top 10 used destiny ips:', 'Destiny', top10, 3)


def part4(file):
	protocol = []
	counts = []
	text = file.readlines()
	for line in text:
		if 'PROTO=' in line:
			line = line.split('PROTO=')[1].split(' ')[0]
			protocol.append(line)
	counts = Counter(protocol)
	counts = list(counts.items())
	counts.sort(key=lambda i: i[1], reverse = True)
	for proto in counts:
		print(proto)

	return createChart("Protocols by usage", "Protocol", counts, 4)

def part5(file):
	top10 = []
	ports = []
	counts = []
	text = file.readlines()
	for line in text:
		if 'SPT=' in line:
			line = line.split('SPT=')[1].split(' ')[0]
			ports.append(line)
	counts = Counter(ports)
	counts = list(counts.items())
	counts.sort(key=lambda i: i[1], reverse = True)

	top10 = counts[:10]


	file2 = open("/etc/services", 'r')
	text = file2.readlines()

	portData = []
	portAux = []
	for line in text:
		for port in top10:
			if port[0] in line:
				if port[0] not in portAux:
					name = line.split('\t')[0]
					portAux.append(port[0])
					portData.append((name, port[0], port[1]))


	for port in top10:
		if port[0] not in portAux:
			portData.append(('default', port[0], port[1]))


	portData.sort(key=lambda i: i[2], reverse = True)


	for port in portData:
		print(port)

	return createChart("Ports by usage", "Port", portData, 5)






def createChart(title, name, data, graphicNumber):
	chartCode = '''// Draw the pie chart when Charts is loaded.
      google.charts.setOnLoadCallback(draw''' + name + '''Chart);

      

      // Callback that draws the pie chart
      function draw''' + name + '''Chart() {

        // Create the data table
        var data = new google.visualization.DataTable();
        data.addColumn('string', '');
        data.addColumn('number', '');
        data.addColumn({type: 'string', role: 'tooltip'})

        data.addRows([ '''


	if   graphicNumber == 2:
		chartCode += makeCountryCode(data)
	elif graphicNumber == 3:
		chartCode += makeCountryCode(data)
	elif graphicNumber == 4:
		chartCode += makeProtoCode(data)
	elif graphicNumber == 5:
		chartCode += makePortCode(data)

	chartCode += ''']);
        // Set options for chart
        var options = {title:\'''' + title + '''\',
                       width:400,
                       height:400};

        // Instantiate and draw the chart
        var chart = new google.visualization.PieChart(document.getElementById(\'''' + name + '''\'));
        chart.draw(data, options);
      }
	'''

	return chartCode

def makePortCode(data):
	chartCode = ""
	p = 0
	for element in data:
		chartCode += "['" + element[0] + "'," + str(element[2]) + ", 'Using " + element[0] + " port (" + element[1] + "): " + str(element[2]) + "\\n"           
		chartCode += "']"
		if(p != len(data)-1):
			chartCode += ','
		p += 1

	return chartCode

def makeProtoCode(data):
	chartCode = ""
	p = 0
	for element in data:
		chartCode += "['" + element[0] + "'," + str(element[1]) + ", 'Using " + element[0] + ": " + str(element[1]) + "\\n"           
		chartCode += "']"
		if(p != len(data)-1):
			chartCode += ','
		p += 1

	return chartCode


def makeCountryCode(data):
	chartCode = ""
	countries = []
	for element in data:
		countries.append(element[3])

	counts = Counter(countries)
	countries = list(counts.items())

	p = 0
	for country in countries:
		chartCode += "['" + country[0] + "'," + str(country[1]) + ", '" + str(country[1]) + " ips from " + country[0] + ":\\n"           

		for element in data:
			if country[0] == element[3]:
				chartCode += element[0] + '\\n'
		chartCode += "']"



		if(p != len(countries)-1):
			chartCode += ','
		p += 1

	return chartCode


def createChartTable(chartCode):
	if not chartCode:
		return ""

	id = chartCode.split("getElementById('")[1].split("'")[0]

	return '''\t\t\t<td><div id="''' + id + '''" style="border: 1px solid #ccc"></div></td>\n'''




chart2 = ""
chart3 = ""
chart4 = ""
chart5 = ""
chart2Table = ""
chart3Table = ""
chart4Table = ""
chart5Table = ""


file = open(sys.argv[1], 'r')
	
part1(file)


print("\n\nTop 10 source ip used:\n")
file.seek(0)
chart2 = part2(file)


print("\n\nTop 10 destiny ip used:\n")
file.seek(0)
chart3 = part3(file)


print("\n\nPackages by protocol: \n")
file.seek(0)
chart4 = part4(file)


print("\n\nTop 10 STP used ports: \n")
file.seek(0)
chart5 = part5(file)
print("\n")




htmlHeader = '''<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">

      // Load Charts and the corechart package.
      google.charts.load('current', {'packages':['corechart']});'''




htmlIntermission = '''</script>
  </head>
  <body>
    <!--Table and divs that hold the pie charts-->
    <table class="columns">
      <tr>\n'''


chart2Table =  createChartTable(chart2)
chart3Table =  createChartTable(chart3)
chart4Table =  createChartTable(chart4)
chart5Table =  createChartTable(chart5)

charts = chart2 + chart3 + chart4 + chart5
chartsTables = chart2Table + chart3Table + chart4Table + chart5Table

htmlEnding = '''</tr>
    </table>
  </body>
</html>'''

try:
	fileHtml = open("charts.html", 'x')
except:
	fileHtml = open("charts.html", 'w')

fileHtml.write(htmlHeader + charts + htmlIntermission + chartsTables + '\n' + htmlEnding)

fileHtml.close()

# pegar as listas 

	

