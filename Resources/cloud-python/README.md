# Interactive Python in the Cloud

This repository contains a few small files that allow to easily deploy Python (cf. http://python.org) and Jupyter Notebook (cf. http://jupyter.org) in the cloud.

It all works even on the smallest **DigitalOcean droplet** (cf. https://m.do.co/c/fbe512dd3dac) which currently costs 5 USD per month with 1 CPU core, 512 MB of RAM and 20 GB of SSD storage.

When setting up such a droplet it is recommended to use a current version of **Ubuntu**.

I assume that you have **cloned the repository** to your local machine (Linux or Mac):

```
git clone --depth=1 https://github.com/yhilpisch/cloud-python
```

## DigitalOcean Droplet

If you do not have a **DigitalOcean account** yet, generate one here

https://m.do.co/c/fbe512dd3dac

You will start with 10 USD worth of compute power (= e.g. 2 monthly fees for the smallest droplet) although you'll only get charged the hours your droplet is alive.

Now **create a droplet** giving it a name like "cloud-python" and chosing the size, location and operating system (e.g. Ubuntu 14.04).

I recommend to post a public key for easy **ssh access** (cf. the tutorial under http://hilpisch.com/rpi/00_basic_config.html).

When you have created the droplet, you are redirected to the droplet overview page which shows, among others, the **IP address of the droplet** which you should copy.

Then navigate to the **repository folder** and do:

```
cd your-path-to/cloud-python
bash setup_server.sh THE-IP-ADDRESS
```

The setup might take a while (about 4 minutes; you'll see the progress on the shell). The last step in the setup fires up a **Jupyter Notebook** server on the **port 8888**. You can access it in the browser under

```
https://THE-IP-ADDRESS:8888
```

There is **SSL encryption** enabled which uses by default the certificate files as provided in the repo (you should replace them by your own; see the comments in the respective Jupyter Notebook configuration file). This feature might require you to add a security exception in your browser due to the nature of the certificate files used.

There is also **password protection** enabled (the password is by default **jupyter**). You should also replace the password hash key in the Jupyter Notebook config file by one of your own (again see the comments in the configuration file itself).

After a successful login, you can now click on the example notebooks and play around.

## Flask Web app

In Jupyter Notebook open a new **terminal** and navigate to the stock_int folder:

```
cd stock_int
```

Start the **example Flask application** as follows:

```
python stock_interactive.py &
```

The app should now be reachable under

```
http://THE-IP-ADDRESS:7777
```

## Security

Note that all this is quite **insecure**. All is run as root user and there is only password protection and encryption for the notebook server in place. It is only for illustration purposes. However, additional security features (e.g. for the Flask app) can easily be added to the set-up.

## datapark.io

The easiest way to securely use Python, R, Julia, etc. in the cloud is to register under http://datapark.io.

With a single registration you have a comprehensive set of **techonlogies, libraries and tools** available to do **data science in the browser**.

## Copyright, License & Disclaimer

© Dr. Yves J. Hilpisch \| The Python Quants GmbH

The code of this repository is BSD licensed (cf. http://opensource.org/licenses/BSD-3-Clause).

The code in this repository comes with no representations or warranties, to the extent permitted by applicable law.

http://tpq.io \| team@tpq.io \|
http://twitter.com/dyjh

**Python for Finance Training** \| http://training.tpq.io

**datapark.io** \| http://datapark.io

**Quant Platform** \| http://quant-platform.com

**Python for Finance (O'Reilly)** \|
http://python-for-finance.com

**Derivatives Analytics with Python (Wiley Finance)** \|
http://derivatives-analytics-with-python.com

**For Python Quants Conference** \| http://fpq.io
