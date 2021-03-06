#!/usr/bin/env python
import urllib.request
import urllib
import sys
import csv
import os 
import re
from datetime import datetime, timedelta
import time
import glob
from os import path
import codecs

class StockTableInfo:
	__item_list = []
	__item_num = 0
	def __init__(self, stockTabURL, stockDayURL):
		self.item_list = []
		self.item_num = 0
		self.stockTabURL = stockTabURL
		self.stockDayURL = stockDayURL
	def append(self, serial_number, name):
		item = []
		item.append(serial_number)
		item.append(name)
		self.__item_list.append(item)
		self.__item_num+=1
	def remove(self):
		item = []
		if (self.__item_num > 0):
			item = self.__item_list[0]
			self.__item_list.remove(0)
			self.__item_num-=1
		return item
	def getItem(self, idx):
		item = []
		if (idx < self.__item_num):
			item = self.__item_list[idx]
		return item
	def getSize(self):
		return self.__item_num
	def printMsg(self):
		item = []
		for idx in range(0, self.__item_num):
			item = self.__item_list[idx]
			print("serial number:", item[0], " ;name:", item[1])

	
def stock_download_data(year,month,stock,Stock_DAY_URL):

	if(os.path.exists('data') == False):
		os.system('mkdir data')

	urlList = Stock_DAY_URL %(year,month,year,month,stock)
	localList = "./data/%04d%02d_%s.csv" %(year,month,stock)
	with urllib.request.urlopen(urlList) as response, \
			open(localList, 'w') as infile:
		try:
			# specify decoding to remove OS dependency
			infile.write(response.read().decode('big5hkscs')) # for '恒', '碁'
		except UnicodeDecodeError:
			return False
	if(path.getsize(localList) == 0):	
		os.remove(localList)	

def stock_combin_all_day(Stock):
	output_name = './stock_data/'+Stock+'.csv'
	init = 0
	if(os.path.exists('stock_data') == False):
		os.system('mkdir stock_data')
	
	outfile = open(output_name,'w')
	for file in glob.glob('./data/*'+Stock+'.csv'):
		if init == 0:
			outfile.write("Day,Trading Volume,Turnover,Opening price,Highest Price,Floor price,Closing price,Spread,Auction items\n")
			init = 1
		f = open(file,'r')
		for line in f.readlines()[2:]:
			outfile.write(line)
		f.close()
		os.remove(file)
	init = 0
	outfile.close()
	if(path.getsize(output_name) == 0):	
		os.remove(output_name)	

def stock_download_all_day(cStockTabInfo,StartYear,StartMonth,Stock):
	for y in range(StartYear,datetime.today().year+1):
		if StartYear == datetime.today().year:
			for m in range(StartMonth,datetime.today().month+1):
				#print('Y%04d-%02d' %(y,m))
				#print(g_Stock_DAY_URL %(y,m,y,m,Stock))
				stock_download_data(y,m,Stock,cStockTabInfo.stockDayURL)
		elif y == datetime.today().year:
			for m in range(1,datetime.today().month+1):
				#print('R%04d-%02d' %(y,m))
				#print(g_Stock_DAY_URL %(y,m,y,m,Stock))
				stock_download_data(y,m,Stock,cStockTabInfo.stockDayURL)
		elif y == StartYear:
			for m in range(StartMonth,12+1):
				#print('V%04d-%02d' %(y,m))
				#print(g_Stock_DAY_URL %(y,m,y,m,Stock))
				stock_download_data(y,m,Stock,cStockTabInfo.stockDayURL)
		else:
			for m in range(1,12+1):
				#print('N%04d-%02d' %(y,m))
				stock_download_data(y,m,Stock,cStockTabInfo.stockDayURL)
		m = 0
	stock_combin_all_day(Stock)

def stock_download(cStockTabInfo,StartYear,StartMonth):
        if(os.path.exists('stock_data') == False):
                os.system('mkdir stock_data')

        print("Downloading stock data..........")

        for i in range(0, cStockTabInfo.getSize()):
                item = cStockTabInfo.getItem(i)
                #print(item[0])
                done = int(100 *i / int(cStockTabInfo.getSize()))
                sys.stdout.write("\r[%s%s] %d%s %s  " % ('=' * done, ' ' * (100-done),done,'%',item[0]))
                sys.stdout.flush()
                stock_download_all_day(cStockTabInfo,StartYear,StartMonth,item[0])

def parseinfo_stocktable(cStockTabInfo):
	
	browser_urlinfo = codecs.decode(urllib.request.urlopen(cStockTabInfo.stockTabURL).read(), 'big5', errors='ignore')

	if (len(browser_urlinfo) == 0):
       		return

	urlinfo_split = re.split("<td", browser_urlinfo)
	item_flag = 0
	serial_num = ""
	name = ""
	for i in range(0, len(urlinfo_split)):
		data = ""
		if (urlinfo_split[i].find("td") >= 0):
			data = urlinfo_split[i].split('>')[1].replace("&nbsp;", "").split('<')[0]
		if (len(data) > 0):
                        if (item_flag == 0):
                                serial_num = data
                                item_flag = 1
                        elif (item_flag == 1):
                                name = data
                                cStockTabInfo.append(serial_num, name)
                                item_flag = 0

def parse_stock_table_htm2csv(StockURL,StockTable):
	next_line = 0
	localList = "./stock_data/StockTable.htm"

	if(os.path.exists('stock_data') == False):
		os.system('mkdir stock_data')

	with urllib.request.urlopen(StockURL) as response, \
			open(localList, 'w') as infile:
		try:
			# specify decoding to remove OS dependency
			infile.write(response.read().decode('big5hkscs')) # for '恒', '碁'
		except UnicodeDecodeError:
			return False


	infile = open('./stock_data/'+StockTable+'.htm','r')
	outfile = open('./stock_data/'+StockTable+'.csv','w')

	outfile.write("Number,Name\n")
	for line in infile.readlines():
		if line.find('&nbsp') != -1:
			if( line.split('&nbsp')[0].split('>')[1].split('<')[0] != ''):
				outfile.write(line.split('&nbsp')[0].split('>')[1].split('<')[0])
				if next_line == 0:
					outfile.write(",")
					next_line = 1
				else:
					outfile.write("\n")
					next_line = 0		
	infile.close()
	outfile.close()

