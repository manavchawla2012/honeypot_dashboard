# Honeypot Dashboard

![N|Solid](https://avatars2.githubusercontent.com/u/27804?s=280&v=4)

#### Honeypot For Visualization and With admin and role management

  - Create new users with priviledges
  - Admin User with Complete Access
  - Currently Supporting Bar/Pie/Donught/Comarison Charts
  - 2 Database for Authentication and Data of Dashboard

# New Features!

  - Can add new graphs to dashboard using simple query
  - STIX Visualization for Displaying attacks

### Tech

Honeypot Dashboard uses a number of open source projects to work properly:

* [React Js] - HTML enhanced for web apps!
* [Django] - Django 3.0.2 Framework
* [MySql] - Database for storing
* [Pandas] - For querying from database and performing optimized acrtions on data
* [Compress] - The streaming build system
* [Compress] - The streaming build system
* [Jquery] - For Javascript Operations

### Installation

Require Python 3.6+ to run
Create virtual environment 
Install dependencies using pip install -r requirements.txt
Coply .env.example file to .env and enter the credentials for database
```sh
$ python manage.py migrate --database="default" (For Database migrations)
$ python manage.py create_graph_type
$ python manage.py generate_rule_data
$ python manage.py generate_stix_Data
```

### Contact
[![](https://cdn1.iconfinder.com/data/icons/social-signature/512/Linkedin_Color-128.png)](https://www.linkedin.com/in/manav-chawla-9b1147120/)
