# Riot Developer Example App
This project is a consumption example of [Riot Games Developer API](https://developer.riotgames.com/apis) (RGAPI).


# Project Setup
To setup this project locally a few steps are needed, they are:
- [Configure environment variables](#configure-environment-variables)
- [Add rule for localhost domain (only for oauth2 authentication)](#add-rule-for-localhost-domain-only-for-oauth2-authentication)

## Configure environment variables
### API Key
You can get the API Key after sign in at [Riot Games Developer Portal](https://developer.riotgames.com/login). This token will be used as environment variable `APP_KEY`.

### Get credentials for oauth2
For oauth2 authentication are needed two credentials, they are `CLIENT_ID` and `CLIENT_SECRET` and will be used respectively for environment variables `RSO_CLIENT_ID` and `RSO_CLIENT_SECRET`. Provided by (https://developer.riotgames.com/)

### Create .env file
Copy file `.env.example` to a new file named `.env`.

### Update .env file
Set the environment variables with the credentials created in the last steps. For example:
```
APP_PORT=5000
APP_CALLBACK_PATH = <YOUR-CALLBACK-PATH>
RSO_CLIENT_ID=<YOUR-CLIENT-ID>
RSO_CLIENT_SECRET=<YOUR-CLIENT-SECRET>
APP_KEY=<YOUR-API-KEY>

```

## Add rule for localhost domain (only for oauth2 authentication)
To use oauth2 authentication redirect flows is needed to match your app hostname with the `redirect_uri` provided when [getting credentials for oauth2](#get-credentials-for-oauth2).

### Windows
Open hosts file `C:\Windows\System32\Drivers\etc\hosts` \
Add your hostname to localhost ip
```
127.0.0.1  local.exampleapp.com
```

### MacOS and Linux
Open hosts file: `sudo nano /etc/hosts` \
Add your hostname to localhost ip
```
127.0.0.1  YOUR-REDIRECT-URI
```


## My Account
For this example we will authenticate through RSO (Riot SSO) and request account data by using oauth2 access token.

1. Open the example app with the [host you defined](#add-rule-for-localhost-domain-only-for-oauth2-authentication)
2. Follow the `Sign In` link

![App Home with signin link](./docs/img/app-home.png "App Home with signin link")

You will be redirected to Riot SSO Login Page. Authenticate using your account credentials.

![Riot Login Page](./docs/img/rso-form.png "Riot Login Page")

After login you will be redirected to local app. Click `My Account`. The app will request [/riot/account/v1/accounts/me](https://developer.riotgames.com/apis#account-v1/GET_getByAccessToken) using an access token of your account.

![App Home Signed](./docs/img/app-home-signed.png "App Home Signed")

When following `My Account` you receive a response with the same structure of this example:

```json
{
    "puuid": "Player Universal Unique ID",
    "gameName": "Game Name",
    "tagLine": "Tag Line"
}
```
> The json values are only examples. For puuid you will receive an encrypted string.

## Logout
Go to app home page and click `Logout`.

