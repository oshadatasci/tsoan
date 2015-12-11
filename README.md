# tsoan
Unify County Business Pattern data from the US Census with BLS Injury and Illness Rate data to compute the relative risk that workers face across the country.

![Employment Data Choropleth](https://github.com/oshadatasci/tsoan/blob/master/images/CBP_CHOROPLETH.png)

## First Get the Data from BLS    
1. Access the Multi-screen data tool here: http://data.bls.gov/cgi-bin/dsrv?ii.    
2. Choose the area    
	- Choose all of the Private Industry selections.    
	- Choose states using Shift or CTRL + arrow keys.    
	- Please note that some states do not participate in the Survey of Occupational Injuries and Illnesses (SOII) and state participation may vary year to year so some state data are not available. Using the national averages is a suggested alternative to using state level data.    
	- Click Next Form.
3. Choose the supersector    
	- Choose each one using the Shift or CTRL + arrow keys    
	- Click Next Form.    
4. Choose the individual industries    
	- Each supersector that you selected will have its own section    
	- At the end of each section is the 2-digit NAICS. For example, GP1CON or GP2CON will give you the general construction industry.    
	- Anything with letters instead of numbers (like GP1CON above) is a 2-digt NAICS or combined 2-digit NAICS (like Natural Resources and Mining, which is combination of NAICS 11 Agriculture, forestry, fishing and hunting and NAICS 21 Mining, quarrying, and oil and gas extraction)    
	- Select all of the industries you like and click Next Form.    
5. Choose case type    
	- Choose using CTRL + arrow keys:    
		1 = Total recordable cases    
		2 = Cases involving days away from work, job transfer, or restriction    
		3 = Cases involving days away from work    
		4 = Cases involving days of job transfer or restriction    
		8 = Other recordable cases    	
	- Click Next Form.    
6. Choose data type    
	- Choose using CTRL + arrow keys    
		3 = Rate of injury and illness cases per 100 full-time workers (size class 0)    
        6 = Number of injury and illness cases (thousands) (size class 0)    
	- Click Next Form.    
7. Verify selections    
	- This example will return 16,026 data series    
	- Click Retrieve Data    
8. Review data: The data are displayed in an HTML page. There is also an option to export each data series into an Excel file    

## Next get the County Business Pattern Data     
From: http://www.census.gov/econ/cbp/ 

## Load
Run loaddata.py to start loading and preprocess the BLS and CBP data.

## Wrangle
Run the wrangle/wrangle.py file to build and test the necessary SQL database tables.

## Index
Then run index.py to compute the index for each OSHA area office and export to csv.