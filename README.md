# Markr Data Ingestion & Processing Microservice

## Approach
The approach was to create a FastAPI webserver, for numerous reasons that make it appealing
- FastAPI has inbuilt documentation through Swagger/Redoc, covering one of the core needs
- Has validation built in with Pydantic
- Fast for both coding and execution ( it's in the name c; )
- Integrates nice and easily with SqlAlchemy or other ORMs

The `/import` endpoint works in a typical way, where it consumes JSON (Wait? wasn't it supposed to be XML? More below.), caches the results in a dictionary which is subsequently overridden if a new result with higher available or obtained marks appears, and then persists the data. When persisting the data, it follows the same rules, checking to see if any data in the database should be overridden, or if the result should be ignored in favour of already present data.

Now, that XML and JSON mix-up. While the core functionality of the `/import` was nothing special, there was an important design decision that was made before the data even reaches the business end. I created a middleware that processes incoming requests, and if they have the content type of `text/xml+markr`, then it converts the XML document to JSON and forwards it to the endpoint business code. The reason I did this is that this microservice could then be effectively a part of the grander whole at Mark. Since it does all the business in pydantic/JSON, it means that the codebase could easily be unified with anything else across Markr. Presumably, it'd be easier to interface with existing Markr library code, as well as being 'future-proof' in case the endpoint would ever be used anywhere else. Essentially, by converting the XML to JSON, it means this microservice doesn't have to be relegated to some sort of 'legacy' code that works with a specific customer, and can be a part of the whole Markr platform. 

The general approach was straight forward for the `results/:test_id/aggregate` GET endpoint, where it simply read the data from the database, and then performed metrics on it. Currently, this is done in a quite naive way where it will calculate the endpoint whenever it is called. In order to speed this up, the metrics calculations could be done whenever data is ingested at the `/import` endpoint, and persisted in the database. All that the `.../aggregate` endpoint would do is simply fetch from the DB and display the results. The reason I haven't done this is I was already pushing it for time, so I made a ticket in Jira and left it for another day when I had some free time.

## Key Assumptions
About the system: 
- All (valid) results will have a test-id, student-number, and valid summary-marks; Assuming any of these are missing, then the test result will be considered invalid.
- Students can have different available marks for the same test 
- Standard deviation should be 0.0 if only one result 
- If getting the aggregate of a test with no results, then it should return a full json response, but each value should be zero

## Highlights
- To view documentation, simply navigate to `localhost/docs` or `localhost/redoc` (`localhost:8000` if running in debug mode) for your choice of Swagger or Redoc API documentation. This only has to be augmented for edge cases (such as the custom errors we throw in the business logic)
- Check out the pydantic models, I think they're pretty neat. The benefits of having typing and validation of JSON objects done straight out of the box with Python types is a powerful feature (and for not much code!)

## To build and run (docker / docker-compose)
From the root directory (where this file is located)
`docker-compose -f .\docker\docker-compose.yml up --build`

To access, simply go to `localhost/{endpoint of choice}` or `localhost/docs`

### With tests
Simply go into the docker compose file, and uncomment the two keys (`entrypoint` and `command`) under `web`
Note: make sure they're on the same indent as all the other keys in the docker-compose file


## To run in debug mode
- Install any python dependencies (virtualenv or otherwise) `pip install -r requirements.txt`
- run `uvicorn main:app --reload` to run in debug mode

You'll likely need to make sure that you have a Postgres DB running on your local machine as well. They will need credentials such as follows, and these can be changed in the `database.py` file. A setup sql script can be found under `docker/sql/create.sql`
- username: `postgres`
- password: `postgres`



p.s. I may have gotten a bit excited with this project, I was very eager to build something in FastAPI and it exceeded a lot of my expectations.