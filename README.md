# panda-dataset
### Pakistani News Dataset

### Notes
- Clone repo
- BeautifulSoup? Required?
$ pip install beautifulsoup4
- Yaml
$ pip install pyyaml


### How to generate Dataset
Change the paths in the **create-articles.yaml** file in **configurations** folder

$> cd [repo]

$> cd scripts/create-articles/

$> python3 create-articles.py ../../configurations/create-articles.yaml > log.txt

For windows run the following command
~~~
python [path to create-articles.yaml file] > [log filename.txt]
~~~


This will generate a log.txt file in scripts/create-articles folder

This will generate dataset.yaml in artifacts/articles folder
