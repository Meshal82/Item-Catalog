# Item Catalog 

> Meshal AL-hossan

## About the project

To Develop an application that provides a list of items that are represeanted as cars , in this project ,within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own cars. Also, this project focus on Implementing CRUD (create, read, update and delete) operations and Developing a web application using the Python framework Flask.




##  Used Technolgies 
1. Python
2. HTML
3. CSS 
4. OAuth
5. Flask Framework

## Installation
There are some dependancies you need to set up first: 

- [Vagrant](https://www.vagrantup.com/)
- [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

## How to Install
1. Install Vagrant & VirtualBox
2. Clone the Udacity Vagrantfile
3. Go to Vagrant directory and either clone this repo or download and place zip here
3. Launch the Vagrant VM (`vagrant up`)
4. Log into Vagrant VM (`vagrant ssh`)
5. Navigate to `cd/vagrant` as instructed in terminal
6. The app imports requests which is not on this vm. Run sudo pip install requests
7. Setup application database `python /catalog/database_setup.py`
8. Insert fake data `python /catalog/seeder.py`
9. Run application using `python /catalog/webserver.py`
10. Access the application locally using http://localhost:8000






#### Launch Project
  1. Launch the Vagrant VM using command:
  
  ```
    $ vagrant up
     
    $ vagrant ssh
  ```
  2. Run your application within the VM
  
  ```
  
    $ python /vagrant/catalog/webserver.py
  ```
  3. Access and test your application by visiting [http://localhost:8000](http://localhost:8000).


## Helpful Resources

* [PostgreSQL 9.5 Documentation](https://www.postgresql.org/docs/9.5/static/index.html)
* [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://www.vagrantup.com/downloads)