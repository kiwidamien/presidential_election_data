# Presidential data set

It is difficult to find a collection of election results for all years. For more modern elections (post 2008) there are reasonably gppd sources; before that it is a case of having to scrape individual PDFs that the FEC has produced.

Someone has already put together an election data source and colated the results in Excel, and put the data here:
https://drive.google.com/folderview?id=0Bz_uFI8VY7xLekx0cWdVcGhJblk&usp=sharing

The Excel workbook is not particularly tidy, and it is difficult to store and transform this data. This repo contains the code to turn this worksheet into a more convinient (but still not long or "tidy") format in two files: `output/candidates.csv` and `output/election.csv`. 

## Processing files

There are four files that are important in the processing. 

The first is the [original data file](https://drive.google.com/folderview?id=0Bz_uFI8VY7xLekx0cWdVcGhJblk&usp=sharing). 

The second is `us_state_abbrev.py`. This file contains a single dictionary that maps state name to the two letter state abbreviation.

The third is `01_process_from_excel.py`. This converts the data from excel, does some cleaning, and strips off the multiindex from it. The data is mostly processed at this point, and has the form shown below:
```
year,state,votes,candidate,party,short_state
2016,Alabama,729547,"Clinton, Hillary",Democratic,AL
2016,Alaska,116454,"Clinton, Hillary",Democratic,AK
2016,Arizona,1161167,"Clinton, Hillary",Democratic,AZ
2016,Arkansas,380494,"Clinton, Hillary",Democratic,AR
2016,California,8753788,"Clinton, Hillary",Democratic,CA
2016,Colorado,1338870,"Clinton, Hillary",Democratic,CO
2016,Connecticut,897572,"Clinton, Hillary",Democratic,CT
```

The difficulty with this case is there is lots of information that is repeated (for example, in the lines quoted above, we should not repeat the information that "Hillary Clinton" is the 2016 candidate for the Democratic Party). The last file, `02_to_long_form.py`, separates the table above into two CSVs that are in close to normal form: elections.csv (which contains information about how the vote went for each party in each state) and `candidates.csv` (which contains information about who the candidate is for each party in a given election year). 

## Output formats

### Format of output/candidates.csv
```
year,party,candidate
1952,Democratic,"Stevenson, Adlai"
1952,Republican,"Eisenhower, Dwight"
1956,Democratic,"Stevenson, Adlai"
1956,Republican,"Eisenhower, Dwight"
1960,Democratic,"Kennedy, Jack (JFK)"
1960,Republican,"Nixon, Richard"
etc
```

### Format of putput/elections.csv
```
State,Democrat,Republican,Other,Year
AK,0,0,0,1952
AL,275075,149231,0,1952
AR,226300,177155,0,1952
AZ,108528,152042,0,1952
CA,2257646,3035587,0,1952
CO,245504,379782,0,1952
CT,481649,611012,0,1952
DC,0,0,0,1952
DE,83315,90059,0,1952
```

### Non-tidy election data

Note that the election data is still not [tidy data](http://vita.had.co.nz/papers/tidy-data.pdf). In particular:
* The columns `Democrat` and `Republican` are variables (i.e. we are storing variables as both rows and columns)
* The "observational units" are the number of votes for a single party in a given state in a given year

A tidy data set would take the form
```
State,Year,Party,Votes
AL,1952,Democrat,275075
AL,1952,Republican,149231
AR,1952,Democrat,226300
AR,1952,Republican,177155
...
```

Because the US is largely a two-party system, I have not broken the data down to this level. Instead, I have considered the "operational unit" to be the results of an election in a given state, in a given year.

