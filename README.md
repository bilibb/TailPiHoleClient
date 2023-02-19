# TailPiHoleClient

## TODO: 
* Farbe
* Einheitliche Formatierung der Liste
* Code Reduzierung

## Abhängigkeiten
* Nmap
* [python-nmap](https://pypi.org/project/python-nmap/)

## Installation
### Systemweit
```sh
git clone https://github.com/bilibb/TailPiHoleClient.git
cd TailPiHoleClient
pip install -r requirements.txt
```

### In virtueller Umgebung 
```sh
git clone https://github.com/bilibb/TailPiHoleClient.git
cd TailPiHoleClient
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

## Ausführen
* Ggf. Pfad zum Logfile und Netzwerk in `main.py` anpassen
* `python3 main.py`
* `python3 main.py -h` zum Anzeigen der Hilfe und möglichen Parameter
