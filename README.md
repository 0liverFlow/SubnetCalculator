<img width="900" alt="image" src="https://user-images.githubusercontent.com/64969369/210277615-2f481490-fdf2-4833-843f-fe30e82211d5.png">

# SubnetCalculator
[![Python](https://img.shields.io/badge/Python-%E2%89%A5%203.10-yellow.svg)](https://www.python.org/) 
![Version 1.0](http://img.shields.io/badge/version-v1.0-orange.svg) ![License](https://img.shields.io/badge/license-GPLv3-red.svg) <img src="https://img.shields.io/badge/Maintained%3F-Yes-96c40f"> 
 
 ## Purpose
SubnetCalculator is a python script which allows you to divide a network into subnetworks.<br>
It performs three main tasks:
- Determining the **network address**, the **broadcast address** and the **host id range** from a given IP address in CIDR notation.<br>
- Dividing a given network into a specific number of sub-networks(**FLSM**).
- Dividing a given network into sub-networks using a number of hosts for each subnet(**VLSM**).<br>
## Preview
![image](https://user-images.githubusercontent.com/64969369/233727082-4ddb1706-d8f3-4043-8f65-136740c26c7e.png)

## Important Notes
Before using this script, thanks in advance to respect the following rules:
- This program works only for IPv4 addresses.
- The format of an IP address must be as follows : x.x.x.x or x-x-x-x (with x between 0 and 255).
- The ip address's separator must be a dot(.) or a dash(-)
- The subnet mask must be given in CIDR notation /x with x between 1 and 31
- Thank you very much for taking the information above into consideration.
Hope you're gonna like subnet/calculator :)

## Installation & Usage
SubnetCalculator is a cross platform script that works with **python 3.10 and above**.
```
git clone https://github.com/0liverFlow/SubnetCalculator
cd ./SubnetCalculator
pip3 install -r requirements.txt
```
Then you can run it
```
SubnetCalculator.py [-h] --network network/subnet [--flsm N] [--vlsm N[,N]]
```

## Docker
You can also execute the program using the Dockerfile. This can be simply done using the instructions below:
```
git clone https://github.com/0liverFlow/SubnetCalculator
cd ./SubnetCalculator
docker build -t subnet-calculator
```
Once the image is built, you can run it
```
docker run -it subnet-calculator --network 192.168.1.0/24 --flsm 2
docker run -it subnet-calculator --network 192.168.1.0/24 --vlsm 20 40 80
docker run -it subnet-calculator --network 192.168.1.0/24
docker run -it subnet-calculator --help
```

## Preview
<img width="1077" alt="image" src="https://user-images.githubusercontent.com/64969369/233792020-673d6b8d-734a-433c-9439-ed78c3b607cd.png">
