# tsoan
Unify County Business Pattern data from the US Census with BLS Injury and Illness Rate data to compute the relative risk that workers face across the country.

[Employment Data Choropleth](https://github.com/oshadatasci/tsoan/blob/master/images/CBP_CHOROPLETH.png)


First run the wrangle.py file to build and test the necessary SQL database tables.

Then run index.py to compute the index for each OSHA area office and export to csv.