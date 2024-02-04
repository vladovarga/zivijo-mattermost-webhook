# Živijó

...*via mattermost incoming webhook*.

This little piece of code is meant as an incoming webhook for [Mattermost](https://mattermost.com/) (*Mattermost is an open source platform that provides secure collaboration for technical and operational teams that work in environments with complex nation-state level security and trust requirements.*)

## What does Živijó mean?
Živijó is a slav version of the happy birthday song ([see for yourself](https://www.youtube.com/results?search_query=%C5%BEivij%C3%B3))

This code can be run periodically (each day) with an external trigger and if provided with the proper .csv file it checks regularly if someone from the list (csv) has birthday (or nameday) on that day. And if yes, it sends a message to configured mattermost channel tagging that person.

## Configuration

Since it's only a webhook, it does not have the full capabilities of a plugin (i.e. it can't read channels, channel members, ...) and hence the configuration is very simple, one could even say "stupid".

A sample configuration can be found in [.env.example](.env.example) or even the [docker-compose.yml](docker-compose.yml) file

The following are environment variables to be set:

| Config Parameter              | Required  | Default value                                                             | Description                                                   |
| ----------------------------- | --------- | ------------------------------------------------------------------------- | ------------------------------------------------------------- |
| `ZIVIJO_WEBHOOK_URL`          |     Y     | (None)                                                                    | Mattermost generated incoming webhook endpoint URL            |
| `ZIVIJO_CHANNEL`              |     N     | `town-square`                                                             | Channel to post in                                            |
| `ZIVIJO_BIRTHDAYS_CSV_PATH`   |     Y     | (None)                                                                    | Path to .csv file with birthdays                              |
| `ZIVIJO_ICON_EMOJI_CSV`       |     N     | `:champagne:,:tada:,:clinking_glasses:,:confetti_ball:,:gift:,:birthday:` | Comma separated list of emoji icons to be used in the message |
| `ZIVIJO_LOGLEVEL`             |     N     | `INFO`                                                                    | Log level respecting the defauly python logging levels: DEBUG, INFO, WARNING, ERROR, CRTICIAL |

## Birthday .csv file structure

There is a [birthdays.example.csv](birthdays.example.csv) file that you can have a look at. But in short, there are these rules:
* .csv file contains a header (1st line)
* only 2 (out of 4) fields are really necessary:
    * email - optional. It's present only for a better identification of a user
    * user_id - required. ID of the user as recognized by Mattermost. Should contain the beginning `@` sign
    * iso-birth-date - required. user's birth date in ISO format. The year part is not really taken in account, so if you're worried about data privacy (GDPR etc) the year can be of a random value
    * iso-name-date - optional. user's name date in ISO format. The year part is not really taken in account

The dates are expected to be in [ISO 8601 standard](https://www.iso.org/iso-8601-date-and-time-format.html) (i.e. YYYY-MM-DD).

Example value:
```
email,user_id,iso-birth-date,iso-name-date
jozko@mrkvicka.com,@jozko.mrkvicka,1990-01-01,1990-01-01
ferko@petrzlen.com,@ferko.petrzlen,1990-12-31,1990-12-31
```
