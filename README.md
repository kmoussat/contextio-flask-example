# Context.IO example Flask App

Excited about using the Context.io apis for your next app?  Thrilled about the explicit and readable nature of Python code? Overflowing with enthusiasm about Flask?  Look no further!  

Here at Context.IO we love experimenting.  As one of our "Hack" days we decided it would be cool to put together a simple application using our [Context.IO Python library](https://github.com/contextio/Python-ContextIO
) and Flask to demonstrate how easily you can get started!

In order to get up and running with this application follow these steps.

1. Head to [Context.IO](https://context.io) to sign up for a free developer account 
2. Log in to your [Context.IO developer console](https://console.context.io) to obtain your `CIO_CONSUMER_KEY` and `CIO_CONSUMER_SECRET` (go to settings)
3. clone this repo `git clone https://github.com/contextio/contextio-flask-example`

## Docker Users

We have included a `Dockerfile` to make things nice an easy for you

*NOTE:* docker-machine users - Make sure your `docker-machine` is ready to go
    
    eval $(docker-machine env <name-of-machine>)

To build and run the container

    docker build -t contextio/cio-flask-example .
    docker run --rm -ti -e "CIO_CONSUMER_KEY=YOUR KEY" -e "CIO_CONSUMER_SECRET=YOUR SECRET" -p 8080:8080 contextio/cio-flask-example

Once you have the container running point your browser at `http://localhost:8080` to see the application in all of it's glory!

*Note:* docker-machine users will need to replace `localhost` in the above url with the IP of their docker-machine.  To find this run `docker-machine ip`

## Non Docker Users

Not to worry! To get up and running simply:

      pip install -r requirements.txt
      export CIO_CONSUMER_KEY=YOUR KEY && export CIO_CONSUMER_SECRET=YOUR SECRET && python app.py

Again, point your browser at `http://localhost:8080` 
