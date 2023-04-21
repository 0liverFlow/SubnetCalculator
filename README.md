<img width="900" alt="image" src="https://user-images.githubusercontent.com/64969369/210277615-2f481490-fdf2-4833-843f-fe30e82211d5.png">

# SubnetCalculator
[![Python](https://img.shields.io/badge/Python-%E2%89%A5%203.9-yellow.svg)](https://www.python.org/) 
![Version 1.0](http://img.shields.io/badge/version-v1.0-orange.svg) ![License](https://img.shields.io/badge/license-GPLv3-red.svg) <img src="https://img.shields.io/badge/Maintained%3F-Yes-96c40f"> 
 
 ## Purpose
SubnetCalculator is a python script which allows you to divide a network into subnetworks.<br>
It performs three main tasks:
- Determining the **network address**, the **broadcast address** and the **host id range** from a given IP address in CIDR notation.<br>
- Dividing a given network into a specific number of sub-networks(**FLSM**).
- Dividing a given network into sub-networks using a number of hosts for each subnet(**VLSM**).<br>
## Preview
<img width="738" alt="image" src="https://user-images.githubusercontent.com/64969369/210280663-e6853b08-9472-4694-aae1-c3b1d47cbaed.png">

## Installation & Usage
SubnetCalculator is a cross platform tool that you can works on **python 3.9 and above**.
```
git clone https://github.com/0liverFlow/SubnetCalculator
cd ./SubnetCalculator
pip3 install -r requirements.txt
```
Then you can run it
```
SubnetCalculator.py [-h] --network network/subnet [--flsm N] [--vlsm N[,N]]
```


