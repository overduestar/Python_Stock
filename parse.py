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


StockURL = "http://www.emega.com.tw/js/StockTable.xls" # For Stock context
Stock_DAY_URL = "http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/Report%04d%02d/%04d%02d_F3_1_8_%s.php&type=csv" # For Stock Day Info.

StockTable = 'StockTable'

def stock_download_data(year,month,stock,Stock_DAY_URL):

	if(os.path.exists('data') == False):
		os.system('mkdir data')

	urlList = Stock_DAY_URL %(year,month,year,month,stock)
	localList = "./data/%04d%02d_%s.csv" %(year,month,stock)
	urllib.request.urlretrieve(urlList, localList)
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

def stock_download_all_day(StartYear,StartMonth,Stock):
	for y in range(StartYear,datetime.today().year+1):
		if StartYear == datetime.today().year:
			for m in range(StartMonth,datetime.today().month+1):
				#print('Y%04d-%02d' %(y,m))
				#print(Stock_DAY_URL %(y,m,y,m,Stock))
				stock_download_data(y,m,Stock,Stock_DAY_URL)
		elif y == datetime.today().year:
			for m in range(1,datetime.today().month+1):
				#print('R%04d-%02d' %(y,m))
				#print(Stock_DAY_URL %(y,m,y,m,Stock))
				stock_download_data(y,m,Stock,Stock_DAY_URL)
		elif y == StartYear:
			for m in range(StartMonth,12+1):
				#print('V%04d-%02d' %(y,m))
				#print(Stock_DAY_URL %(y,m,y,m,Stock))
				stock_download_data(y,m,Stock,Stock_DAY_URL)
		else:
			for m in range(1,12+1):
				#print('N%04d-%02d' %(y,m))
				stock_download_data(y,m,Stock,Stock_DAY_URL)
		m = 0
	stock_combin_all_day(Stock)

def stock_download(StartYear,StartMonth,StockTable):
	f = open('./stock_data/'+StockTable+'.csv','r')
	for row in csv.DictReader(f):
		print(row['Number'])
		stock_download_all_day(StartYear,StartMonth,row['Number'])

def parse_stock_table_htm2csv(StockURL,StockTable):
	next_line = 0
	localList = "./stock_data/StockTable.htm"

	if(os.path.exists('stock_data') == False):
		os.system('mkdir stock_data')

	urllib.request.urlretrieve(StockURL, localList)

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


print('=====Start====')
print(datetime.today())
print(datetime.today().year)
print(datetime.today().month)
print(datetime.today().day)
print('%02d' %(datetime.today().day))
parse_stock_table_htm2csv(StockURL,StockTable)
#stock_download_all_day(2015,2,'4545')
#stock_download_all_day(2015,9,'3322')
#stock_combin_all_day('4545')
#stock_combin_all_day('3322')
stock_download(2016,3,StockTable)
os.system('del -rf data')
#download_stock_all_data(StockTable,Stock_DAY_URL)
print('======End=====')


