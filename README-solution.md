
### PREREQUISITES


This demo requires the following python modules to be installed:

- dataset==1.0.6
- unittest2==1.1.0
- web.py==0.39

The following commands should install the correct versions of these files:

- pip install dataset
- pip install unittest
- pip install web.py

Data has already been imported into the sqlite database. If you would like to
reimport the csv data please ensure that sqlite3 has been installed on your
machine so that the database can be recreated from the schema.



### RUNNING THE DEMO


To run the demo navigate to the top level directory, then the following commands
are available:

*python example.py -demo*

this starts a web.py server on localhost port 8080 that will serve the demo
webpage. to view the webpage navigate to http:://localhost:8080 in your browser. Use ctrl-c to shutdown the webserver when you are finished.

*python example.py -test*

This will run all the unit tests.

*python example.py -load*
   
Reinitializes database and loads csv file.
**This has already been done for you.**   To reload data remove the database
   file (*sqlite_db/example.sqlite*) before using this command  and ensure that you
   have sqlite3 installed on your machine



### THE DEMO


The demo will display a sitter rank page with the following information for each
sitter: phone, sitter name and the rating score. The information is sorted by
overall sitter rank which is not displayed.

Across the top of the sitter rank page you'll see a slider to filter out
scores. There will be a display to show the threshold that is being
selected. Moving the slider and releasing the mouse button will trigger a
refresh of the page.

The bottom of the page will show the pagination feature.  Records are only
queried and loaded for the range of records being displayed.  Currently there
are 10 sitters to each page.

Sitter images have been resized to make the display more manageable.



### DATA INGESTION


Data from the csv file was ingested into the database with the following
mapping:
```
CSV                   DATABASE TABLE.COLUMN
=================== : ======================
text                : stay.review
rating              : stay.rating
start_date          : stay.start_date
end_date            : stay.end_date

sitter_image        : sitter.image
sitter              : sitter.name
sitter_phone_number : sitter.phone
sitter_email        : sitter.email

owner_image         : owner.image
owner               : owner.name

owner_phone_number  : owner.phone
owner_email         : owner.email

dogs                : dog.name
```

The user id from the image urls were used as the unique identifiers to identify
duplicate owners and sitters

Columns were renamed to prevent redundancy in the name conventions. Ex:
owner_image because owner.image instead of owner.owner_image

Data ingestion also resulted in foreign key relationships between the
tables. To view the full schema look in the *sqlite_db/schema.sql* file.

It's assumed that an owner can have multiple dogs but not all of which may be
present for any given stay. The data ingestion takes this into account.

The code for the data ingestion is in *example/ingest/dataloader.py*



### CALCULATED VALUES
These database columns are calculated values:

- sitter.score
- sitter.ratings_score
- sitter.overall_rank

Database triggers are used to calculate the ratings score and the overall sitter
rank. This ensures that as new records get added in the future that the scores
will remain updated. A concern with database triggers is that they separate the
logic from the code and put it in an out of the way place, the database, where
it's easy to get lost.  In this particular case the expediency of the solution
coupled with the deadline informed the decision to use triggers.

You can view the database triggers in the schema file: *sqlite_db/schema.sql*

The database engine used, *sqlite*, doesn't have the ability to calculate the
sitter score in a trigger due to the nature of the calculation.  Because access
to all the database tables is controlled through an object mapping, for the
sitter score we can move the calculation to that object.  You can see that in this file:  *example/tables/sitter.py*, as we use a descriptor for that data the
calculation will be transparent to the consumer of the data object.



### DATA ACCESS

All access to the database should be through data object mapping.  You can see
these data objects in this directory:  *example/tables*.



### WEB SERVER - STATIC AND DYNAMIC CONTENT

The webserver used for the demo is *web.py*. It serves static content from the
*static/* directory.

The webserver is also used to serve the dynamic content that populates the
sitter rank listing.  The content is requested via a GET request to:
```
http://localhost/items/<offset>/<filterby>
```
- offset is the number of records from the beginning of the recordset 
- filterby is the sitter rating that we use to filter the results.

Data is returned in json format. You can view an example of the return data
by navigating to this url while the demo server is running:
```
http://localhost/items/1/0
```
The sitter page html, css and javascript are located in:

- static/index.html
- static/css/index.css
- static/js/index.js

Boostrap is used as the css framework for it's responsiveness.  Jsgrid provides
the grid functionality and Jquery is used as the javascript framework/library.



### SEPARATION OF PRESENTATION AND CONTENT

The sitter rating page receives data from the backend in json format.  There is
no presentation information in that data.  All presentation markup is done by
the frontend javascript process.

```
backend                          frontend
-------                          --------
database -> webserver -> json |  json -> markup -> display
```


### TESTS

Tests are located in the *test/* directory.  There are tests for all the data
objects as well as the search algorithm.



### DIRECTORY STRUCTURE
```
.
+-- example
¦   +-- data_access
¦   +-- ingest
¦   +-- tables
+-- sqlite_db
+-- static
¦   +-- css
¦   +-- js
¦   +-- libs
¦       +-- bootstrap
¦       ¦   +-- bootstrap-slider
¦       ¦   +-- css
¦       ¦   +-- js
¦       ¦       +-- external
¦       +-- jquery
¦       +-- jquery-ui
¦       ¦   +-- images
¦       +-- jsgrid
¦           +-- i18n
+-- tests
```