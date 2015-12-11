insheet using "/Users/mikescomputer/Documents/OSHA/ii.data.1.AllData.txt", tab

gen industry_code=substr(series_id,7,6)
sort industry_code

save "/Users/mikescomputer/Documents/OSHA/rawiidata", replace

clear
insheet using "/Users/mikescomputer/Documents/OSHA/ii.industry.txt", tab
sort industry_code
drop v7
merge 1:m industry_code using rawiidata
gen area=substr(series_id,15,3)

*IIU00000000001100

gen data_type_code=substr(series_id,13,1)
gen case_type_code=substr(series_id,14,1)

sort data_type_code
drop _merge
save "/Users/mikescomputer/Documents/OSHA/ii_data_ind", replace


clear
insheet using "/Users/mikescomputer/Documents/OSHA/ii.data_type.txt", tab
drop if v1=="data_type_code"
rename v1 data_type_code
rename v2 data_type_text
sort data_type_code

merge 1:m data_type_code using "/Users/mikescomputer/Documents/OSHA/ii_data_ind"
drop _merge

save "/Users/mikescomputer/Documents/OSHA/ii_data_ind_case", replace

clear
insheet using "/Users/mikescomputer/Documents/OSHA/ii.case_type.txt", tab
drop v3
drop if v1=="case_type_code"
rename v1 case_type_code
rename v2 case_type_text
sort case_type_code

merge 1:m case_type_code using "/Users/mikescomputer/Documents/OSHA/ii_data_ind_case"
drop _merge
save "/Users/mikescomputer/Documents/OSHA/iidata", replace


keep if industry_code=="GP2AFH" | industry_code=="GP2MIN" | industry_code=="SP2UTL" |  industry_code=="GP1CON" |  industry_code=="GP1MFG" |  industry_code=="SP2WHT" |  industry_code=="SP2TRW" |  industry_code=="SP1INF" | industry_code=="SP2FIN" | industry_code=="SP2RRL" | industry_code=="541000" | industry_code=="551000" | industry_code=="SP2ADW" | industry_code=="SP2EDS" | industry_code=="SP2HSA" | industry_code=="SP2AER" | industry_code=="SP2AFS" | industry_code=="SP2OTS" | industry_code=="SP1PAD" 
drop if strpos(case_type_text , "RSE")!=0
drop period
rename area area_code
save "/Users/mikescomputer/Documents/OSHA/iidata_small", replace

clear
insheet using "/Users/mikescomputer/Documents/OSHA/ii.area.txt", tab
drop v6
sort area_code
gen new_area = string(area_code,"%03.0f")
drop area_code
rename new_area area_code
merge 1:m area_code using "/Users/mikescomputer/Documents/OSHA/iidata_small"
drop if _merge==1
drop _merge

save "/Users/mikescomputer/Documents/OSHA/ii_data_select_ind_all_numbs"
outsheet using "/Users/mikescomputer/Documents/OSHA/ii_data_select_ind_all_numbs.csv", delimiter(",")


/*
11 GP2AFH
21 GP2MIN
22 SP2UTL
23 GP1CON
31-33 GP1MFG  (Manufacturing)
42 - 45 SP2WHT
48 - 49 SP2TRW
51 SP1INF
52 SP2FIN
53 SP2RRL
54 541000
55 551000
56 SP2ADW
61 SP2EDS
62 SP2HSA
71 SP2AER
72 SP2AFS
81 SP2OTS
92 SP1PAD
*/

