<h1 align="center"/>Marzban</h1>


<p align="center">
 <a href="./README.md">
 English
 </a>
  | 
 <a href="./README-fa.md">
 فارسی
 </a>
</p>

<p align="center">
  <a href="httpps://github.com/gozargah/marzban" target="_blank" rel="noopener noreferrer" >
    <img src="https://github.com/Gozargah/Marzban-docs/raw/master/screenshots/preview.png" alt="Marzban screenshots" width="600" height="auto">
  </a>
</p>

## Table of Contents

- [Overview](#overview)
		- [Features](#features)
- [Installation guide](#installation-guide)
- [Configuration](#configuration)
- [API](#api)
- [Backup](#backup)
- [Telegram Bot](#telegram-bot)
- [Marzban CLI](#marzban-cli)
- [Marzban Node](#marzban-node)
- [Webhook notifications](#webhook-notifications)

<details markdown="1">
<summary> Features </summary>

- Built-in **Web UI**
- Fully **REST API** backend
- [**Multiple Nodes**](#marzban-node) support (for infrastructure distribution & scalability)
- Supports protocols **Vmess**, **VLESS**, **Trojan** and **Shadowsocks**
- **Multi-protocol** for a single user
- **Multi-user** on a single inbound
- **Multi-inbound** on a **single port** (fallbacks support)
- **Traffic** and **expiry date** limitations
- **Periodic** traffic limit (e.g. daily, weekly, etc.)
- **Subscription link** compatible with **V2ray** _(such as V2RayNG, OneClick, Nekoray, etc.)_, **Clash** and **ClashMeta**
- Automated **Share link** and **QRcode** generator
- System monitoring and **traffic statistics**
- Customizable xray configuration
- **TLS** and **REALITY** support
- Integrated **Telegram Bot**
- Integrated **Command Line Interface (CLI)**
- **Multi-language**
- **Multi-admin** support (WIP)
</details>

Installation guide
Run the following command

```bash
sudo bash -c "$(curl -sL https://raw.githubusercontent.com/soltonali/Marzban0/master/easy_setup.sh)" @ install
```

Next, you need to create a sudo admin for logging into the Marzban dashboard by the following command

```bash
marzban-cli admin create 
```

That's it! You can login to your dashboard using these credentials


If you are eager to run the project using the source code, check the section below
<details markdown="1">
<summary><h3>Manual install (advanced)</h3></summary>

Install xray on your machine

You can install it using [Xray-install](https://github.com/XTLS/Xray-install)

```bash
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
```

Clone this project and install the dependencies (you need Python >= 3.8)

```bash
git clone https://github.com/Gozargah/Marzban.git
cd Marzban
wget -qO- https://bootstrap.pypa.io/get-pip.py | python3 -
python3 -m pip install -r requirements.txt
```

Alternatively, to have an isolated environment you can use [Python Virtualenv](https://pypi.org/project/virtualenv/)

Then run the following command to run the database migration scripts

```bash
alembic upgrade head
```

If you want to use `marzban-cli`, you should link it to a file in your `$PATH`, make it executable, and install the auto-completion:

```bash
sudo ln -s $(pwd)/marzban-cli.py /usr/bin/marzban-cli
sudo chmod +x /usr/bin/marzban-cli
marzban-cli completion install
```

Now it's time to configuration

Make a copy of `.env.example` file, take a look and edit it using a text editor like `nano`.

You probably like to modify the admin credentials.

```bash
cp .env.example .env
nano .env
```

> Check [configurations](#configuration) section for more information

Eventually, launch the application using command below

```bash
python3 main.py
```

To launch with linux systemctl (copy marzban.service file to `/var/lib/marzban/marzban.service`)

```
systemctl enable /var/lib/marzban/marzban.service
systemctl start marzban
```

To use with nginx

```
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name  example.com;

    ssl_certificate      /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key  /etc/letsencrypt/live/example.com/privkey.pem;

    location ~* /(dashboard|api|docs|redoc|openapi.json) {
        proxy_pass http://0.0.0.0:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # xray-core ws-path: /
    # client ws-path: /marzban/me/2087
    #
    # All traffic is proxed through port 443, and send to the xray port(2087, 2088 etc.).
    # The '/marzban' in location regex path can changed any characters by yourself.
    #
    # /${path}/${username}/${xray-port}
    location ~* /marzban/.+/(.+)$ {
        proxy_redirect off;
        proxy_pass http://127.0.0.1:$1/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

or

```
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name  marzban.example.com;

    ssl_certificate      /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key  /etc/letsencrypt/live/example.com/privkey.pem;

    location / {
        proxy_pass http://0.0.0.0:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

By default the app will be run on `http://localhost:8000/dashboard`. You can configure it using changing the `UVICORN_HOST` and `UVICORN_PORT` environment variables.
</details>

# Configuration

> You can set settings below using environment variables or placing them in `.env` file.

| Variable                        | Description                                                                                           |
| ------------------------------- | ----------------------------------------------------------------------------------------------------- |
| SUDO_USERNAME                   | Superuser's username                                                                                  |
| SUDO_PASSWORD                   | Superuser's password                                                                                  |
| SQLALCHEMY_DATABASE_URL         | Database URL ([SQLAlchemy's docs](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls)) |
| UVICORN_HOST                    | Bind application to this host (default: `0.0.0.0`)                                                    |
| UVICORN_PORT                    | Bind application to this port (default: `8000`)                                                       |
| UVICORN_UDS                     | Bind application to a UNIX domain socket                                                              |
| UVICORN_SSL_CERTFILE            | SSL certificate file to have application on https                                                     |
| UVICORN_SSL_KEYFILE             | SSL key file to have application on https                                                             |
| XRAY_JSON                       | Path of Xray's json config file (default: `xray_config.json`)                                         |
| XRAY_EXECUTABLE_PATH            | Path of Xray binary (default: `/usr/local/bin/xray`)                                                  |
| XRAY_ASSETS_PATH                | Path of Xray assets (default: `/usr/local/share/xray`)                                                |
| XRAY_SUBSCRIPTION_URL_PREFIX    | Prefix of subscription URLs                                                                           |
| XRAY_FALLBACKS_INBOUND_TAG      | Tag of the inbound that includes fallbacks, needed in the case you're using fallbacks                 |
| XRAY_EXCLUDE_INBOUND_TAGS       | Tags of the inbounds that shouldn't be managed and included in links by application                   |
| CUSTOM_TEMPLATES_DIRECTORY      | Customized templates directory (default: `app/templates`)                                             |
| CLASH_SUBSCRIPTION_TEMPLATE     | The template that will be used for generating clash configs (default: `clash/default.yml`)            |
| SUBSCRIPTION_PAGE_TEMPLATE      | The template used for generating subscription info page (default: `subscription/index.html`)          |
| HOME_PAGE_TEMPLATE              | Decoy page template (default: `home/index.html`)                                                      |
| TELEGRAM_API_TOKEN              | Telegram bot API token  (get token from [@botfather](https://t.me/botfather))                         |
| TELEGRAM_ADMIN_ID               | Numeric Telegram ID of admin (use [@userinfobot](https://t.me/userinfobot) to found your ID)          |
| TELEGRAM_PROXY_URL              | Run Telegram Bot over proxy                                                                           |
| JWT_ACCESS_TOKEN_EXPIRE_MINUTES | Expire time for the Access Tokens in minutes, `0` considered as infinite (default: `1440`)            |
| DOCS                            | Whether API documents should be available on `/docs` and `/redoc` or not (default: `False`)           |
| DEBUG                           | Debug mode for development (default: `False`)                                                         |
| WEBHOOK_ADDRESS                 | Webhook address to send notifications to. Webhook notifications will be sent if this value was set.   |
| WEBHOOK_SECRET                  | Webhook secret will be sent with each request as `x-webhook-secret` in the header (default: `None`)   |

# API

Marzban provides a REST API that enables developers to interact with Marzban services programmatically. To view the API documentation in Swagger UI or ReDoc, set the configuration variable `DOCS=True` and navigate to the `/docs` and `/redoc`.

# Backup

It's always a good idea to backup your Marzban files regularly to prevent data loss in case of system failures or accidental deletion. Here are the steps to backup Marzban:

1. By default, all Marzban important files are saved in `/var/lib/marzban` (Docker versions). Copy the entire `/var/lib/marzban` directory to a backup location of your choice, such as an external hard drive or cloud storage.
2. Additionally, make sure to backup your env file, which contains your configuration variables, and also, your Xray config file. If you installed Marzban using marzban-scripts (recommended installation approach), the env and other configurations should be inside `/opt/marzban/` directory.

By following these steps, you can ensure that you have a backup of all your Marzban files and data, as well as your configuration variables and Xray configuration, in case you need to restore them in the future. Remember to update your backups regularly to keep them up-to-date.

# Telegram Bot

Marzban comes with an integrated Telegram bot that can handle server management, user creation and removal, and send notifications. This bot can be easily enabled by following a few simple steps, and it provides a convenient way to interact with Marzban without having to log in to the server every time.

To enable Telegram Bot:

1. set `TELEGRAM_API_TOKEN` to your bot's API Token
2. set `TELEGRAM_ADMIN_ID` to your Telegram account's numeric ID, you can get your ID from [@userinfobot](https://t.me/userinfobot)

# Marzban CLI

Marzban comes with an integrated CLI named `marzban-cli` which allows administrators to have direct interaction with it.

If you've installed Marzban using easy install script, you can access the cli commands by running

```bash
marzban cli [OPTIONS] COMMAND [ARGS]...
```

For more information, You can read [Marzban CLI's documentation](./cli/README.md).

# Marzban Node

The Marzban project introduces the [Marzban-node](https://github.com/gozargah/marzban-node), which revolutionizes infrastructure distribution. With Marzban-node, you can distribute your infrastructure across multiple locations, unlocking benefits such as redundancy, high availability, scalability, flexibility. Marzban-node empowers users to connect to different servers, offering them the flexibility to choose and connect to multiple servers instead of being limited to only one server.
For more detailed information and installation instructions, please refer to the [Marzban-node official documentation](https://github.com/gozargah/marzban-node)

# Webhook notifications

You can set a webhook address and Marzban will send the notifications to that address.

the requests will be sent as a post request to the adress provided by `WEBHOOK_ADDRESS` with `WEBHOOK_SECRET` as `x-webhook-secret` in the headers.

Example request sent from Marzban:

```
Headers:
Host: 0.0.0.0:9000
User-Agent: python-requests/2.28.1
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
x-webhook-secret: something-very-very-secret
Content-Length: 107
Content-Type: application/json



Body:
{"username": "marzban_test_user", "action": "user_updated", "enqueued_at": 1680506457.636369, "tries": 0}
```

Different action typs are: `user_created`, `user_updated`, `user_deleted`, `user_limited`, `user_expired`, `user_disabled`, `user_enabled`
