# recipinator
Um bot de telegram para auxiliar a busca de receitas e organização de cardápios.


## Contribuindo:
1- Poetry
```
curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
echo 'export PATH=$PATH:$HOME/.poetry/bin' >> ~/.bashrc
source ~/.bashrc

# A versão atual de poetry tá bugada, sendo necessário usar os prereleases
# Atualmente, usa-se a versão 1.1.0b3
poetry self update --preview
```


## Inicializando o projeto:
Rodar `make init_project` deveria funcionar, mas eu ainda nao arrumei os bug dele, entao eu recomendo ir olhando o makefile, deve servir pelo menos como documentação (>:

## Scrapers
Para rodar o scraper "recipes" e colocar seu output em "data.json":
* Ative o shell com `poetry shell` no diretorio inicial.
* Va até a pasta que possui o arquivo `scrapy.cfg` (no caso, recipinator/recipinator/scrapers)
* Rode o comando `scrapy crawl recipes -o data.json`

## Database
Estamos usando sqlite no projeto, depois de criar o banco de dados com `make database`, você pode visualizar o banco de dados com alguma ferramenta como o `sqlitebrowser`

Em sistemas baseados em arch é possível instalá-lo com
`sudo pacman -S sqlitebrowser`

E para ver o banco de dados rodar
`sqlitebrowser recipinator/databases/recipinator.db`

