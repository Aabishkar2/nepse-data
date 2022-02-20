# nepse-data

nepse-data is the collection of all the datasets (from past to present) of various companies listed in the Nepal Stock Market. This repository is built for the students and people who want to perform analysis on Nepal Stock Market using historical (& current) data.

## Data

The data can be found in `data/company` folder. The data is arranged according to the company. For example: in `NMB.csv` you can find all the data of NMB Bank Limited. They are arranged in ascending order (datewise).

The Github Actions updates the data on an almost daily basis so that the datasets available here are up to date.

## Code

The code through which the data were/are being collected resides on the `src/` folder. The code is written in `python3.8` and the required library is stored in `src/requirements.txt`

If you want to run and collect the datasets by yourself then you can run the following command. 


Firstly, Just make sure you have `python3` installed. If not please find python3 installation procedure over [here](https://www.python.org/downloads/) 

```bash
# go into the src folder
cd src

# install requirements
pip3 install -r requirements.txt

# for historical data collection
# if you just want the datasets only then you can just run this only
python3 allDataScrapper.py

# optional -- for daily data updates
python3 dailyDataScrapper.py

```

The code that updates data on a daily basis resides on the `.github/.workflows` directory and runs on Github Action as a CRON job.

## Contributing
Pull requests are welcome. Please open an issue first to discuss what you would like to change.

Things you can consider doing:
- Github action to update code on daily basis on Kaggle
- Datewise Collection of data from past to present


## License
[MIT](https://choosealicense.com/licenses/mit/)