# Description
## Context
Zomato restaurants with their ratings, votes, other crucial data attributes to do some research work.

## Content
What's inside is more than just rows and columns. This zomato exploratory data analysis is for the foodies to find best restaurants, value for money restaurants in their locality. It also helps to find their required cuisines in their locality.

The data is collected using zomato API. More information about zomato API documentation and API key can be found here Zomato_API. The extraction process involves two steps. In first step the city IDs of all the zomato available cities in India are stored using zomato "/cities" API. In the second step using these city IDs, restaurant details in the respective cities are stored in comma separated file (csv).

## Columns
* res_id
* name
* establishment
* url
* address
* city
* city_id
* locality
* latitude
* longitude
* zipcode
* country_id
* locality_verbose
* cuisines
* timings
* average_cost_for_two
* price_range
* currency
* highlights
* aggregate_rating
* rating_text
* votes
* photo_count
* opentable_support
* delivery
* takeaway
