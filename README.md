# Rainy libraries 

A small data analysis project looking at the most rainy libraries in England.

## Prerequisites

What things you need to install the software and how to install them

* Python 3
* Pip

## Installing

The imports used in this project are visible in the ```rainy-libraries.py``` file. To install the required packages, run the following command in your terminal:


```console
pip install NetCDF4
pip install numpy
pip install pandas
pip install pyproj
```

## Data

There are 3 data files used in this project:

* ```rainfall-UK-2014.nc``` - NetCDF file containing rainfall data for the UK in 2021
* ```code-point-open.csv``` - [Code-Point Open](https://www.ordnancesurvey.co.uk/business-and-government/products/code-point-open.html)
* ```libraries.csv``` - a list of libraries in England, extracted from the Arts Council England website

Ensure before running that these data files are extracted into the same directory as the ```rainy-libraries.py``` file. By default they are zippped up.

## Running

To run the project, run the following command in your terminal:

```console
python rainy-libraries.py
```

## Authors

* **Dave Rowe** - *Initial work* - [DaveBathnes](https://github.com/DaveBathnes)

See also the list of [contributors](https://github.com/librarieshacked/rainy-libraries/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
