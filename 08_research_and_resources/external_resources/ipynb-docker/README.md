# Jupyter & IPython Notebook Servers in Docker Containers

This repository contains all ingredients to run a **Python Flask Web application** that starts multiple **Docker containers which in turn run a Jupyter Notebook server** using SSL encryption and password protection (cf. http://ipython.org).

You can see the **application in action** under http://docker.quant-platform.com.

![Jupyter Notebook](http://hilpisch.com/jupyter_docker.png "Jupyter Notebook")

Note, however, that this app runs on the smallest **DigitalOcean droplet** (cf. https://www.digitalocean.com/?refcode=fbe512dd3dac). When setting up such a droplet it is recommended to use the latest version of **Ubuntu** in combination with **Docker** (cf. http://docker.com).

In addition, when setting up an environment make sure to have Python, Flask, Flask-WTF and Flask-SQLAlchemy installed. Best you install **Anaconda** first (cf. http://continuum.io/downloads) and do then:

```
sudo apt-get install python-pip
pip install flask-wtf
pip install flask-sqlalchemy
```

I assume that you have **cloned the repository** on an appropriate infrastructure in the root directory ```/root```:

```
git clone --depth=1 https://github.com/yhilpisch/ipynb-docker
``` 

## Docker Containers

In order to run the Python Flask Web application on a server, you have to **first build two Docker containers**.

The first one is a basic **Ubuntu** container with some **Python** in it. Assuming you are in the repo folder do:

```
cd pythoncontainer
docker build -t pythoncontainer .
```

The second, which relies on the first, adds the **Notebook Server functionality**. Built it via

```
cd ../jupserver
docker build -t jupserver .
```

## Flask Web app

### Configuration

First some configurations. You need to adjust the URL to the server in the template file found under ```/root/ipynb-docker/serverapp/templates/server.html``` to reflect the correct IP address or the domain used. In that file replace the following link

```
<a href="https://docker.quant-platform.com:{{ port }}" target="_blank">link</a>
```

by a link containing your IP address

```
<a href="https://your-ip-address:{{ port }}" target="_blank">link</a>
```

When using a domain, make sure that both **http & https** are configured for the web server (e.g. nginx). The configuration (in the file ```/etc/nginx/sites-enabled/default```) used for the demo under http://docker.quant-platform.com is:

```
server {
        listen 80;
        listen 443 ssl;
        ssl_certificate     /root/ipynb-docker/jupserver/jup_cert.pem;
        ssl_certificate_key /root/ipynb-docker/jupserver/jup_cert.pem;
        server_name docker.quant-platform.com jupyter.quant-platform.com;
        location / {
            proxy_pass http://docker.quant-platform.com:8888;
            proxy_set_header Host $host;
            proxy_buffering off;
        }
}

```

If not installed yet, install nginx via ```sudo apt-get install nginx```.

A self-signed certificate for SSL encryption can be generated as follows:

```
openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout jup_cert.pem -out jup_cert.pem
```

Make sure that this certificate is stored in the folder ```/root/ipynb-docker/jupserver``` (best to generate it there).

### Running the Application

Now go the the directory of the app and start the app:

```
cd /root/ipynb-docker/serverapp
python run_app.py &
```

Your app should now be reachable under ```http://your-ip-address:8888```.

## Copyright, License & Disclaimer

© Dr. Yves J. Hilpisch \| The Python Quants GmbH

The code of this repository is BSD licensed (cf. http://opensource.org/licenses/BSD-3-Clause).

The code in this repository comes with no representations or warranties, to the extent
permitted by applicable law.

http://tpq.io \| team@tpq.io \|
http://twitter.com/dyjh

**Python Quant Platform** \| http://quant-platform.com

**Derivatives Analytics with Python (Wiley Finance)** \|
http://derivatives-analytics-with-python.com

**Python for Finance (O'Reilly)** \|
http://python-for-finance.com





