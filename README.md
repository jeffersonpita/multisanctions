# Multiple Sanctions Search

Thank you for taking the time to complete our code challenge!

For this problem, you will build an application for searching publicly available sanctions data. You may take as long as you like with your solution. The data provided is a subset of many different sources of sanctions data. So, while we have not asked you to build all the other integrations, please take into account the idea that your solution will be thought about in the context of a more general set of datasets.

## Important

A couple notes to hopefully help make this a low-stress experience:

First, please do not hesistate to ask us any questions you may have. You will not be penalized for asking questions; your questions help us improve the clarity of the instructions so it benefits you and future candidates.

Second, do not be shy about using your preferred language, libraries, databases, or frameworks. We do not expect you to learn our stack for this challenge; your time is better spent using the tools you know that are suitable for the problem at hand.

Third, if you need to learn anything while working on the challenge, that's okay! We know you have many skills and experiences, so it's not a strike against you if you need to do some reading.

Finally, we value your time so we don't expect you to spend more time than necessary on polish. Just focus on the fundamentals! Feel free to include a README.md in your solution covering polish you would make if you have ideas for improvements.

## Requirements

Your solution:

1. may use any language, libraries, database, or frameworks
2. must be dockerized.
   - Please update [Dockerfile](./Dockerfile) and [docker-compose.yml](./docker-compose.yml) as needed.
   - Please build any dependencies within one or many Docker containers
3. must pass the [smoke-tests](#Testing)
4. must contain an [api](#API) and [ui](#UI)

### Testing

We provide a smokescreen test that can be run against your api with `make smoke-test`.

The api is stubbed with fixtures that pass all the tests for a sanity check. If `make smoke-test` does not work for you and you believe you have `docker` and `docker-compose` installed and up-to-date, please let us know.

To ensure the smoke-test works properly, make sure you update the value of `API` for the `test` service in [docker-compose.yml](./docker-compose.yml).

We may run additional test cases against your solution.

### Ingesting Sanctions Data
Your objective is to create service(s) that handle ingesting the below sanctions data into a persistent datastore. Your ingestion solution should run when `docker-compose up` is run and should provide the user of this code the ability to refresh the data on the timeframe of their choice (minutely, hourly, daily, etc).

Requirements:

  - All of the data from the source should be ingested, not just the fields used in the subsequent API.
  - Partial ingestion should be avoided, either all the data should be written to the store or none of it if there is an error.
  - The timestamp of ingestion should be persisted for each sanctions list.
  - Reruning the ingestion process should not disrupt user accessibility to the API requested below.

Other Notes:

  - The choice of datastore and schema is completely up to you, please be prepared to defend your choices.
  - There are no limits on services in the docker-compose, feel free to add additional services and tools if they are necessary.



#### OFAC Consolidated List

[OFAC Sanctions Data](OFAC Consolidated List) is available for free via the [Open Sanctions Project](https://github.com/alephdata/opensanctions). The data is provided as a CSV directly by Open Sanctions but a link to the original XML data file is also present.


#### European Sanctions


European Sanctions data is publicly available with an [EU Login](https://webgate.ec.europa.eu/cas/login?loginRequestId=ECAS_LR-5816125-a3R1xh1RhIp0ZBXrLAZHmwuuL5f3jUR3W2nf3cLoeaIetewOSzQ6gkC1LBG07tG9c4ZYd0PHLOwCoXGK4Nbj38-rS0vSrmBGYCtzg7YLRrbJx-n9FPWblzzJ1zdy1GE5ysZ6saqwZ5zxHJwZI6V5A9ZYoo). After you have created an account. You can navigate [here](https://webgate.ec.europa.eu/europeaid/fsd/fsf#!/files) to acquire a link to the sanctions data. The site can provide you an authenticated link that can be used programatically without logging in to the site. You will have the choice of CSV, XML, or PDF data. Make sure to click `Show Settings for Crawler/Robot` expander to get the correct link.
https://webgate.ec.europa.eu/europeaid/fsd/fsf/public/files/csvFullSanctionsList_1_1/content?token=n00378g1

In order to communicate to the smoke-test when the server is ready, create a /status endpoint that returns an error code until the ingestion is complete and the server is ready to serve requests.

## API
The ingested data should be used to power a simple one endpoint search service. This endpoint should provide a consumer the ability to search both (or eventually any number) of ingested sanctions lists.

Your server should have a `/search` endpoint that takes a `name` query parameter with a legal or natural person's name. It should respond with an array of matches with the following shape:
```json
{
  "name": "Kim Jung Un",
  "aliases": ["Rocket Man"],
  "is_person": true,
  "sanctioned": true,
  "list": "european_sanctions_list",
  "relevance": 0.92,
}
```

Relevance should be a float in the range [0,1] indicating how close the result is to the users search. relevance=1 indicates an exact string match between the search and either the name or one of the aliases.



## UI
You do not need to create any user interface beyond the API endpoint.
