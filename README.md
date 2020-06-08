# Tweetbrief

A user-controlled automation for generating daily Tweeter briefs.

__NOTE__: right now this repo contains a (declarative) description of the task to be implemented, no actual code is available at the moment.

## Why

Wouldn't it be nice and relaxing to be able to stay up to date with one's own Twitter bubble without the need to actually engage in all the Social Web nonsense? Without loosing oneself into the hopeless attempts to catch up with the endless Twitter timelines? Without pseudo social interactions? Without being subject to Twitter algorithms which decide what one sees and what we overlook?

## What

This project is a user-controlled automation (packaged to conveniently run in a  docker container) for generating daily Tweeter briefs. This machinery expects only one essential input parameter:

- `TARGET_USERNAME`

Once given the above target tweeter username, the following algorithm is used to assemble a daily brief:

1. The set of accounts being followed by the `TARGET_USERNAME` is read,

2. For each of these followed account, the list of max. 3 "top" tweets are read from that account's feed,

3. All these lists of the "Top 3" tweets from all the followed accounts are combined into one single list. This combined list is then sorted and trimmed so it fits on one page when tweets are printed (yes, that means lots of trimming!),

4. A one 2-column page PDF is generated, presenting all the top tweets obtained in the previous step. This PDF is made available through an `/output` volume for further consumption by the user.

The metric used for calculating the "Top 3" tweets are the number of retweets they got. In the future version, we will likely want to replace this metric with: "the number of RTs from the users being followed by the target user".

### Configuration

The whole configuration process via a `docker-compose.yaml`, e.g.

```yaml
tweetbrief:
  image: ...
  environment:
    - BRIEF_PERIOD=7 # Generate brief for the last 7 days 
    - TARGET_USERNAME=WildlandIO
    - BOT_ACCOUNT=TerminusBot
    - BOT_ACCOUNT_TOKEN=... # ?
  volumes:
    - /vols/dailybriefs:/output:w
```

As seen above, it is also possible to configure the some secondary params, which otherwise should get sane defaults:

- `BRIEF_PERIOD` -- the period of time, in days (24h), defining the window time of which tweets to gather in step `#1` above. Default `1` day.

- `SINGLE_AUTHOR_MAX_TWEETS` -- the maximum number of tweets from one user to include (step `#2`). Default `3`.

## How

TBD :)

### Notes for implementers

1. There is no assumption that the operator of this bot knows the credentials for the `TARGET_USERNAME` account.

2. A dummy account (`BOT_ACCOUNT`) might be needed to access Twitter API. In that case, the credentials for accessing this dummy account might be passed via the same configuration mechanism as shown above (the actual method will depend on the actual Twitter API used). Since this is a dummy account, it is ok to pass the credentials in plaintext via docker-compose.

3. The docker should use cron inside to schedule the execution of the actual tweet fetching script every `BRIEF_PERIOD` days, otherwise should be sleeping.
