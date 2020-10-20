# Dependencyless numverify for russian phone numbers
## Installation
```
python setup.py install
```
## Usage

### Load database
```
from numverify_rossvyaz_client import Loader

loader = Loader('/workspace/numverify_rossvyaz_client/db_loader/db.sqlite')
loader.load()
```
#### Outputs:
```
File download started
ABC-3xx.csv is loading...
ABC-4xx.csv is loading...
ABC-8xx.csv is loading...
DEF-9xx.csv is loading...
Database file ready, path: /workspace/numverify_rossvyaz_client/db_loader/db.sqlite
```
### Get phone number info
```
from numverify_rossvyaz_client import Client

client = Client('db.sqlite')
print(client.get_carrier('79990001111'))
# ООО "Скартел"
print(client.get_info('79990001111'))
# {'phone': '79990001122', 'carrier': 'ООО "Скартел"', 'region': 'г. Москва * Московская область'}
```