# index.py

####################################################################
# Imports
####################################################################
import os
import wrangle
import pandas as pd
import csv
import sqlite3 as sqlite

from wrangle import wrangle

####################################################################
# Connect to database
####################################################################
cnx = sqlite.connect(wrangle.DBPATH)
cursor = cnx.cursor()


####################################################################
# Basic Index Computation
####################################################################
def sum_sq_dev(emp, rate, norm=0.5):
	'''
	Compute the sum square deviance of an industry based on the number of workers
	employed in that industry, the BLS injury and illness rate for that industry,
	and the norm rate (defaults to 0.5).
	'''
	if emp > 0:
		x = ((rate-norm)/norm)**2
		return x
	else:
		return 0.0


####################################################################
# Index computation by FIP - requires FIP State Code and FIP County Code
####################################################################
def compute_index(state_code,city_code, year, industry):
	'''
	Compute the index for a given state code, city code, year, and industry.
	'''
	try:
		cursor.execute("SELECT emp FROM allemp WHERE fipstate = ? AND fipscty = ? AND naics=? AND year=?", (state_code,city_code,industry,year))
		emp = int(cursor.fetchone()[0])
		cursor.execute("SELECT value FROM DAWF WHERE naics = ? AND year = ?", (industry, year,))
		rate = float(cursor.fetchone()[0])
		index = sum_sq_dev(emp, rate, 1)*emp
		return index	
	except TypeError:
		return 0.0

def multi_naics_index(state_code,city_code):
	'''
	Compute the 2013 index given a state code and city code.
	'''
	composite = 0
	for i in wrangle.industries:
		temp = compute_index(state_code,city_code,2013,i)
		composite += temp
	return composite

def index_change(state_code,city_code,year1,year2,industry):
	'''
	Compute the change in index given a state code, city code, industry, and a date range.
	'''
	first_year = compute_index(state_code,city_code,year1,industry)
	second_year = compute_index(state_code,city_code,year2,industry)
	change = first_year - second_year
	if change == 0:
		print "No change in index between %s and %s in the %s industry:" % (year1,year2,industry),
	elif change >0:
		print "The index went down between %s and %s in the %s industry:" % (year1,year2,industry),
	else:
		print "The index went up between %s and %s in the %s industry:" % (year1,year2,industry),
	return change


####################################################################
# Index computation by an area office's RID
####################################################################
def multi_naics_ao(ao):
	'''
	Compute the 2013 index given an area office RID number.
	'''
	fips = wrangle.rid_to_fip(ao)
	total = 0
	for f in fips:
		state = f[0]
		city = f[1] 
		total += multi_naics_index(state,city)	
	return total


####################################################################
# Compute all the indices for all the area offices
####################################################################
def index_aos():
	'''
	Compute the multi_naics_index for all area offices and export table.
	'''
	with open('results2.csv', 'wb') as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=',')
		csvwriter.writerow(["area_office","osha_index","total_workers"])
		for rid in wrangle.rids:
			print "Printing data for %d" % rid
			osha_index = multi_naics_ao(rid)
			cursor.execute("SELECT worker_count FROM workers WHERE area_office=?", (rid,))
			worker_count = cursor.fetchone()[0]
			csvwriter.writerow([rid,osha_index,worker_count])



if __name__ ==  "__main__":
	# # Test to get osha_index by area office
	# print multi_naics_ao(625700) # Baton Rouge Area Office

	# Compute the osha_index for all area offices and export to a table called "results.csv".
	index_aos()
