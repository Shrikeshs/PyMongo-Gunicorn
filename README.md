# PyMongo-Gunicorn

This repo represents a flask project along with MongoDb as the Backend DB and Gunicorn as the Websever.
This serves as an example to AsyncIO Flask API's

A detailed readme file will be published soon..
Cheers

### Rest API Design
The following document contains the API design for report generation on movies database (mongo)

## Design Constraints:
* Reusable
* Easy to integrate
* Other developers can adopt and add more reports with ease
* Following REST principles
* More reports can be added under this design without change to the previous code


## Proposal 1: 

Endpoint :  v1/movies/<report-name>?page=0&page_size=10
v1 -> we can rely of v1 version working as we upgrade any report
<report-name> -> naming as per REST specifications  
Page and page number -> these params represent pagination	

#### Example:
For movies collection, 
Get top 10 directors as per number of  comments on movies 
	Endpoint:   POST v1/movies/directors-per-comments
	Request params : page and page number
	Request body:  comment_threshold (gt & lt), time ranges, exclude/include (directors)

Get top movies as per rating
Endpoint:   POST v1/movies/movies-per-rating
	Request params : page and page number
	Request body:  rating_threshold (gt), time ranges, exclude/include (actors, directors, writors)


Likewise for other collections, the endpoints can be 
v1/comments/<report-name>?page=0&page_size=10
v1/users/<report-name>?page=0&page_size=10

#### Notes with this design:
* Each time a new report is created, a new endpoint should also be created.
* Is there a way to make this generic?


## Proposal 2: 
Endpoint :  v1/reports?page=0&page_size=10
v1 -> we can rely of v1 version working as we upgrade any report
Page and page number -> these params represent pagination
Body will contain report specific key words which can be later translated to the report
Request  :
We store the report objects in a collection and depending upon the keyword, we execute that report.	
 Will contain filters like comment_threshold (gt & lt), time ranges, exclude/include (directors, actors, writers) and  
		report_name -> “top-directors-per-comment”, “top-movies-per-rating”


{
   "report_name":"top-directors-per-moving-rating",
   "movie_released_at":{
      "$gt":"1990",
      "$lt":"2021"
   }
     .....
     //Other report related filters
}




Response :
	JSON responses with the corresponding HTTP codes depending on the status of the report generation //structure

{ 
"name" : "Mark Anthony"
"average_rating":"3.4",
"average_screen_playtime" : "340"
......
},
{ 
"name" : "Mark Anthony II"
"average_rating":"3.8",
"average_screen_playtime" : "180"
......
},



Under this there can be multiple ways to achieve asynchronicity.
## Problems with synchronization:
* The reports that are generated can take larger times to complete.
* The client side timeout can occur waiting for the results.
* Reports can be complex to generate.

## Proposal 2.1:
Under this, we can have the response which indicated the name of the report and status
Response Example:		
	
{
   "report_name":"top-directors-per-moving-rating",
   "status":"running"/”completed”/”error”,
   "report_date":"2022-10-27 16:55:15.894000"
}


We can have a bigger threshold at server-side to wait for the report to get generated/ the async operation to complete
This response will be shown until the status=completed, after which, we show the results of the report to the client as a JSON response.



Proposal 2.2:
Under this, we can have the response similar to the one above along with the url link to GCS bucket where the report csv file will be stored after completion.

{
   "report_name":"top-directors-per-moving-rating",
   "status":"running"/”completed”/”error”,
   "report_date":"2022-10-27 16:55:15.894000",
   "gcs_link":"link_to_bucket"
}


The response will be stored in the gcs link the report gets generated/ the async operation to complete.


#### Example:
For movies collection, 
Get top 10 directors as per number of  comments on movies 
	Endpoint:   POST v1/reports
	Request params : page and page number
	Request body:  comment_threshold (gt & lt), time ranges, exclude/include (directors)

		report_name -> “top-directors-per-comment”
Get top movies as per rating
Endpoint:   POST v1/movies-per-rating
	Request params : page and page number
	Request body:  rating_threshold (gt), time ranges, exclude/include (actors, directors, writors)
		report_name -> “top-movies-per-rating”

#### Notes with this design:
* Solves the issue of creating a huge number of endpoints for each report.
* This is generic




