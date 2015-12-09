# wrangle.py

####################################################################
# Imports
####################################################################
import os
import pandas as pd
import sqlite3 as sqlite
from pandas.io import sql

####################################################################
# Connect to database
####################################################################
DBPATH = os.path.join(os.path.dirname(__file__), "empdata.db")
cnx = sqlite.connect(DBPATH)
cursor = cnx.cursor()


####################################################################
# Globals
####################################################################
EMPDATAPATH = os.path.join(os.path.dirname(__file__), "..","data","employment_data.csv")
RATEDATAPATH = os.path.join(os.path.dirname(__file__), "..","data","rate_data.csv")
RIDDATAPATH = os.path.join(os.path.dirname(__file__), "..","data","fips_to_rids_update2.csv")

area_offices = ["Mobile Area Office","Birmingham Area Office","Anchorage Area Office","Phoenix Area Office",\
				"Little Rock Area Office","Oakland Area Office","San Diego Area Office","Denver Area Office",\
				"Englewood Area Office","Bridgeport Area Office","Hartford Area Office","Wilmington Area Office",\
				"Jacksonville Area Office","Tampa Area Office","Fort Lauderdale Area Office","Savannah Area Office",\
				"Atlanta East Area Office","Atlanta West Area Office","Honolulu Area Office","Boise Area Office",\
				"Peoria Area Office","Fairview Heights Area Office","North Aurora Area Office","Calumet City Area Office",\
				"Chicago North Area Office","Indianapolis Area Office","Des Moines Area Office","Witchita Area Office",\
				"Nashville Area Office","Baton Rouge Area Office","Augusta Area Office","Bangor District Office",\
				"Baltimore Washington Area Office","Braintree Area Office","Springfield Area Office","Andover Area Office",\
				"Lansing Area Office","Eau Claire Area Office","Jackson Area Office","Kansas City Area Office",\
				"St. Louis Area Office","Billings Area Office","Omaha Area Office","Las Vegas Area Office",\
				"Concord Area Office","Marlton Area Office","Hasbrouck Heights Area Office","Parsippany Area Office",\
				"Avenel Area Office","El Paso Area Office","Albany Area Office","Buffalo Area Office","Tarrytown Area Office",\
				"Syracuse Area Office","Manhattan Area Office","Long Island Area Office",\
				"Queens District Office of the Manhattan Area Office","Raleigh Area Office","Bismarck Area Office",\
				"Cincinnati Area Office","Toledo Area Office","Cleveland Area Office","Columbus Area Office",\
				"Oklahoma Area Office","Portland Area Office","Harrisburg Area Office","Pittsburgh Area Office",\
				"Wilkes Barre Area Office","Allentown Area Office","Erie Area Office","Philadelphia Area Office",\
				"Providence Area Office","Columbia Area Office","Dallas Area Office","Lubbock Area Office",\
				"Houston North Area Office","Corpus Christi Area Office","Fort Worth Area Office",\
				"San Antonio Area Office","Austin Area Office","Houston South Area Office","Boston Regional Office",\
				"Norfolk Area Office","Bellevue Area Office","Charleston Area Office","Madison Area Office",\
				"Appleton Area Office","Milwaukee Area Office","Denver Regional Office","Puerto Rico Area Office"]

# Area Offices are more often known by their 'RID' - See lookup table in data folder.
rids = [418600,418300,1032100,936400,627100,936100,936200,830500,830600,111500,112000,317300,419700,420600,418800,\
		418400,418100,418200,936300,1032500,524500,524530,521400,521700,524200,524500,523100,728100,729700,420100,\
		625700,111100,112900,316100,111400,112600,134000,522900,523900,419400,728500,729300,830100,728900,936500,\
		111700,213900,214500,214200,213400,627500,213100,213600,216000,215800,215000,214700,215600,420300,830300,\
		522000,524700,522300,522500,627700,1032700,316700,317500,317700,317900,336000,317000,112300,418500,626300,\
		627510,626600,626000,636900,625500,625400,626700,100000,316300,1032300,316400,523300,521100,523400,800000,\
		215300]

industries = ["Agriculture, forestry, fishing and hunting","Mining","Utilities","Construction","Manufacturing",\
			   "Wholesale trade","Transportation and warehousing","Information","Finance and insurance",\
			   "Real estate and rental and leasing","Professional, scientific, and technical services (scope changed in 2009)",
			   "Management of companies and enterprises","Administrative and support and waste management and remediation services",\
			   "Educational services","Health care and social assistance","Arts, entertainment, and recreation",\
			   "Accommodation and food services","Other services, except public administration"]


####################################################################
# Open employment data csv
# Load into Pandas to wrangle
####################################################################
read_emp = pd.read_csv(EMPDATAPATH, low_memory=False)
view_emp = pd.DataFrame(read_emp, columns=['index','fipstate', 'fipscty', 'naics', 'emp', 'year'])
view_emp = view_emp[['fipstate','fipscty','emp','naics','year']]

def load_emp():
	'''
	Puts all of the employment data into a sql table
	'''
	try: 
		sql.has_table('allemp', con=cnx)
		print "Employment data already loaded."
	except ValueError:
		sql.to_sql(view_emp, name = 'allemp', con=cnx)
		print "Employment data successfully loaded."


####################################################################
# Open injury and illness rate csv
# Load into Pandas to wrangle - just get DAWF for 100 FTW
####################################################################
read_rates = pd.read_csv(RATEDATAPATH, low_memory=False)
view_rates = pd.DataFrame(read_rates, columns=['index','area_name','case_type_code','data_type_code','naics','year','value'])
view_rates = view_rates[['area_name','case_type_code','data_type_code','naics','year','value']]

# national averages only
US_all = view_rates[view_rates.area_name == 'Private industry, All U.S.']

# just select case type 3 - Days Away from Work
DAWF = US_all[US_all.case_type_code == '3']

# just select data type 3 - Rate of injury/illness per 100 FTW
DAWF_rate = DAWF[DAWF.data_type_code == '3']
DAWF_rate = DAWF_rate.drop('area_name', 1)
DAWF_rate = DAWF_rate.drop('case_type_code', 1)
DAWF_rate = DAWF_rate.drop('data_type_code', 1)

def load_rates():
	'''
	Puts all the DAWF rates into a sql table
	'''
	try: 
		sql.has_table('DAWF', con=cnx)
		print "Injury rate data already loaded."
	except ValueError:
		sql.to_sql(DAWF_rate, name = 'DAWF', con=cnx)
		print "Injury rate data successfully loaded."

####################################################################
# Open area office data csv
# Load into Pandas to wrangle
####################################################################
fips_to_rids = pd.read_csv(RIDDATAPATH)
aos = pd.DataFrame(fips_to_rids, columns=['fipstate', 'fipscty', 'county', 'state', 'area_office', 'rid','region'])

def load_aos():
	'''
	Puts all the Area Offices into a sql table
	'''
	try: 
		sql.has_table('AOS', con=cnx)
		print "Area office data already loaded."
	except ValueError:
		sql.to_sql(aos, name = 'AOS', con=cnx)
		print "Area office data successfully loaded."

####################################################################
# Lookup FIP by Area Office - either by RID or Area Office Name
####################################################################
def ao_to_fip(ao):
	'''
	If you know the name of the area office, generate the FIP state and county codes
	as well as the name of the counties that are under that area office's jurisdiction.
	'''
	cursor.execute("SELECT fipstate,fipscty,county FROM AOS WHERE area_office = ?", (ao,))
	fip = cursor.fetchall()
	return fip

def rid_to_fip(rid):
	'''
	If you know the RID number for the area office, generate the FIP state and county codes
	as well as the name of the counties that are under that area office's jurisdiction.
	'''
	cursor.execute("SELECT fipstate,fipscty,county FROM AOS WHERE rid = ?", (rid,))
	fip = cursor.fetchall()
	return fip


####################################################################
# Precompute number of workers by area office
####################################################################
def create_ao_workers():
	'''
	Precomputes number of workers that each area office covers.
	Stores values in a sql table
	'''
	sql_commit = (
    			"CREATE TABLE IF NOT EXISTS workers ("
   				"    id INTEGER PRIMARY KEY AUTOINCREMENT,"
    			"    area_office TEXT NOT NULL,"
    			"	 worker_count INT"
    			")"
			)
	cursor.execute(sql_commit)
	print "Worker data by area office successfully created."

def worker_count(state_code,city_code, industry, year=2013):
	'''
	Return the number of workers for a given state code, city code, year, and industry.
	'''
	cursor.execute("SELECT emp FROM allemp WHERE fipstate = ? AND fipscty = ? AND naics=? AND year=?", (state_code,city_code,industry,year))
	emp = int(cursor.fetchone()[0])
	return emp	

def ao_worker_count(ao):
	'''
	Return the number of workers in a given area office (which includes multiple FIPs).
	'''
	fips = rid_to_fip(ao)
	total = 0
	for f in fips:
		state = f[0]
		city = f[1] 
		for i in industries:
			try: 
				total += worker_count(state,city,i)
			except TypeError:
				pass
	return total

def all_aos_worker_count():
	sql_commit = "INSERT INTO workers (area_office, worker_count) VALUES (?,?)"
	for ao in rids:
		count = ao_worker_count(ao)
		cursor.execute(sql_commit, (ao,count,))
		cnx.commit()
		print "Successfully committed the count for %s" % ao


if __name__ ==  "__main__":
	# Build the SQL tables to run the queries
	load_emp() 
	load_rates()
	load_aos()
	create_ao_workers()
	all_aos_worker_count()

	# Test by printing out the employment for a given industry in a given county
	cursor.execute("SELECT emp FROM allemp WHERE fipstate = ? AND fipscty = ? AND naics=? AND year=?", (1,1,"Construction",2013))
	emp = int(cursor.fetchone()[0])
	print "In 2013, Autauga County had %d workers in the Construction industry." % emp

	# Test by printing out the injury rate for a given industry
	cursor.execute("SELECT value FROM DAWF WHERE naics = ? AND year = ?", ("Construction", 2013,))
	rate = float(cursor.fetchone()[0])
	print "That year, the BLS DAWF injury rate for Construction was %d." % rate

	# Test by printing out all the FIPs for a given area office
	cursor.execute("SELECT county FROM AOS WHERE rid = ?", (418600,)) 
	fip = cursor.fetchall()
	print "The Mobile Area Office is responsible for the following counties:"
	for f in fip:
		print f