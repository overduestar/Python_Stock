import os
import time
from parse import *
from datetime import datetime, timedelta

def parse():

	#=============== Pattern =================
	g_StockTabURL =  "http://www.emega.com.tw/js/StockTable.htm" #"http://www.emega.com.tw/js/StockTable.xls" # For Stock context
	g_StockDayURL = "http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/Report%04d%02d/%04d%02d_F3_1_8_%s.php&type=csv" # For Stock Day Info.
	c_StockTab = StockTableInfo(g_StockTabURL, g_StockDayURL)
	#=========================================

	print('=====Start====')
	print(datetime.today())

	StartYear = input('Please enter Start Year : ')
	StartMonth = input('Please enter Start Month : ')
	StockNumber = input('Please enter Stock Number or enter \'all\' : ')	
	
	if(StockNumber == 'all'):
		parseinfo_stocktable(c_StockTab)
		stock_download(c_StockTab,int(StartYear),int(StartMonth))
	else:
		stock_download_all_day(c_StockTab,int(StartYear),int(StartMonth),StockNumber)
		
	os.system('rm -rf data')

	print('======End=====')


if __name__ == '__main__':

	#=== parse all stock info==#
	tStart = time.time()
	parse() 
	tEnd = time.time()
	print("Time taken: %f seconds" %(tEnd - tStart))




