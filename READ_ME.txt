Please see the 2019 SDFSS Capstone Report for more detailed information. 

The SDFSS.py file contains the sdfss function that performs the switching calculations.  It will take in
the current temperature, year, month, day, hour, and what system is being used ("B" for Bosch and "G" for 
Goodman). It willreturn an array with the elec value, the price of electricity, the COP, the price of natural gas, 
and the Furnass Efficientcy.  The elec value is a floating numbers that signals which system to use. 
If it is greater than 1, then use electricity, but if it less than 1 use Natural Gas.  

The analysis.py file performs an analysis using data taken from Environment and the Climate Change Canada - 
Meteorological Service of Canada (see report for reference).  The user of the file can choose what senarios to 
perform by munipulating what is in the dataFiles array, the sTypes array, and the modes array.  It will perform 
the sdfss function on every point of data given the perrameters, and save the information as a csv file in the 
selected folder. This data can be viewed and analysed using excel.  

The api.py file is a simple Rest-ful api that demonstrates how the function can be used on a sever. The only 
parameter is the outdoor temperature, which should be communicated in KELVIN to avoid negative values. It will 
perform the calculation using the current time and the selected system.  It will give the response in JSON. 

