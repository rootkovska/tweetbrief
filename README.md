# Tweetbrief (solution of github.com/rootkovska/tweetbrief)

A user-controlled automation for generating daily Tweeter briefs.

## Run
1. Create `.env` file containing credentails to Twitter API in the format below:
   - `CONSUMER_KEY=<TWITTER_CONSUMER_API_KEY>`
   - `CONSUMER_SECRET=<TWITTER_CONSUMER_API_SECRET>`
2. Inside docker `compose-compose.yml` set `TARGET_USERNAME` and optionally `BRIEF_PERIOD` and `SINGLE_AUTHOR_MAX_TWEETS`.
3. Execute the following command:
   ```sh
   docker-compose up -d
   ```
