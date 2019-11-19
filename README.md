# CSEC 380 Group Project
This has all the files for our group project along with 
the agile set up for our workflow.

## To Run it
``` 
cd servers
docker-compose up --build
```

## Documentation
This folder contains all of the documentation that we initially created to start the project. This is where we got the guide lines to most of the work that we have been doing. There may be tweaks made to these through out the project as we realize stuff needs to be implemented or is no longer needed.

## Servers
This is where all the main server files are kept along with the docker-compose to start up the whole application. The servers that can be located in here are:
* Mariadb databse
* Flask web application with needed requirements
* docker-compose file to start the whole thing

## Tests
This is where all the unit testing that is being implemented takes place. These are to ensure that the application is working properly when we push new content to it. 
