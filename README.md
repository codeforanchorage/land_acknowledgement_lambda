# Land Acknowledgement SMS App
Land Acknowledgement is a simple api that links data about native lands to current locations.
Designed to run with AWS Lambda and API Gateway and produce output suitable for Twilio's SMS messaging. Hi

# Data Sources
This project does two basic things:
- determines a lat/lon from a city/state
- looks up the native land from that point

Contributions that improve either of these are welcome. Currently the data comes from:

- Data about boundaries of Native land is from: [native-land.ca](https://native-land.ca)
- Geolocations from MapBox

# Dependencies:
**Python 3**

**AWS Chalice**
This uses [AWS Chalice](https://aws.github.io/chalice/) to simplify deploying apps using Lambda and API Gateway. It also makes it easy to run and test code locally. You will need to install the Chalice command-line tool in order to run this code.

**MapBox API Key**
The ability to convert locations like "Chicago, IL" into geographic coordinates requires a geocoding service. This uses MapBox for that service. To run locally, you will need a mapbox api key:
[Mapbox api](https://www.mapbox.com/pricing/#search)

The free tier should easily cover local development and testing.

# Running Locally

**Install dependencies**
Clone this repo
```
git clone https://github.com/codeforanchorage/land_acknowledgement_lambda.git
```

Create a virtual env (Optional, but a good practice)
```
cd land_acknowledgement_lambda/
python -m venv .venv
source .venv/bin/activate
```

Make sure pip is up-to-date and install dependencies
```
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

**Set MapBox API Key**
The app will look for a MapBox API key in order:
1. An Environmental Variable `MAPBOX_TOKEN`
This is all you need to run locally. The easiest way to set this is from the command line:
```
export MAPBOX_TOKEN=some_long_token_string
```
2. AWS Secrets at the arn
This is best for production since it allows you to keep the token out of sight.
The app will try to access the arn set in .chalice/secrets_policy.json.

**Start it up**
```
chalice local
```
