# No-Profit Catalog
No-Profit Catalog is a simple project create to the Udacity Fullstack Nanodegree.
The website lists some no-profit organizations. The users can:
- Login with third part applications (Google and Facebook)
- Create, Edit and Delete no-profit organizations according to authorizations rules.
- Can consult no-profit organization data with JSON endpoints

# Pre-requisites
- Python installed (Python 3 recommended)
- VirtualBox
- Ngrok
- Facebook app

# install
## Virtual Machine setup
1. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads).
2. To configure the virtual machine, download or clone the repository: `git clone https://github.com/udacity/fullstack-nanodegree-vm`. Either way, you will end up with a new directory containing the VM files.
3. Change to this directory in your terminal with `cd`. Inside, you will find another directory called vagrant. Change directory to the vagrant directory. Using the command:
  `$ vagrant up`
4. When vagrant up is finished running, you will get your shell prompt back. At this point, you can run `$ vagrant ssh` to log in to your newly installed Linux VM.
5. Inside the VM, change directory to `cd /vagrant`.

## Configure the data
1. Download or clone this repository to the vagrant directory: `git clone https://github.com/Pedroknoll/No-Profit-Catalog.git`
2. Go to the repository diretory `cd achaong`
3. Run the noprofit.sql script to create the database. For that  type `psql -f noprofit.sql`
4. Run `python models.py` to setup the DATABASE
5. Run `python populates_database.py` to populate the DATABASE with data samples.

## Configure the logins:
### Configure Ngrok
1. In order to running the facebook login you will need to configure a secure url (https). For that go to [Ngrok](https://ngrok.com/).
2. Create an account, download  and run the ngrok.exe file.
3. On openned command line type `ngrok http 5000` and copy the https url tunnel generated.

### Configure facebook Login
1. Go to [Facebook for developers](https://developers.facebook.com/).
2. Click + Add Product in the left column.
3. Find Facebook Login in the Recommended Products list and click Set Up.
4. Click Facebook Login that now appears in the left column.
5. Add the https generated with ngrok to the Valid OAuth redirect URIs section.
6. Copy the app_id and app_secret and paste in the respectives sections at the `fb_client_secrets.json`

### Configure Google Login
1. Go to client_secrets.json and change the `https://9d94e4a4.ngrok.io/callback` with the https url generated with ngrok and add the final path `/callback` to the url.


## Running
1. On command line `\vagrant\achaong` type `python application.py`
2. Access the app with your ngrok https url.


## License
This project is licensed under the terms of the
