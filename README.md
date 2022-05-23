# Python-exam-project
## Python flight webscraper 
Group members:
* [Mathias E. Poulsen](cph-mp557@cphbusiness.dk)
* [Mustafa Tokmak](cph-mt357@cphbusiness.dk)
* [Markus Agnsgaard](cph-ma587@cphbusiness.dk)

## Description
Projektet har i alt 3 'grene' og er alle med til at besvare spørgsmålene vi stillede os selv inden vi begyndte med projeket (se spørgsmål længere nede).

1. Gren (Hent data om fly til Cypern i perioden 2022-07-11 til 2022-07-20(+-2 dage) og send brugeren en mail hver dag kl 10 med resultaterne):
Send brugeren en mail med info omrking:
pris, destination, tidsinterval (både frem og tilbage) , antal stop,(både frem og tilbage), flyselskab(er) og url
Gennem hosting hos Amazon Web Services bliver der hver dag via et cronjob sendt en mail med 12 tur-retur rejser til Cypern. Gennem disse mails vil det (forhåbentligt) være muligt at skaffe sig en billig flybillet.

2. Gren (Hente data om fly til Cypern i perioden 2022-07-19 til 2022-08-15 for at svare på spørgsmål)
Ved brug af selenium web scrappes siden www.kayak.dk og data omkring pris, destination, tidsinterval, antal stop, flyselskab(er) og url bliver hentet. Derefter undersøges tendenser og dataen bliver visualiseret. Se under afsnittet 'List of Challenges'. Her bliver der taget udgangspunkt i en enkeltbillet.

3. Gren (Hente data om fly reviews og lave en machine learning model ud fra content [link til dataset](www.google.com))
Ud fra teksten i de 30.000 reviews laves en sentiment analysis og der trænes en model til at forudsige hvorvidt et review er positivt eller negativt. Resultaterne bruges også til at undersøge om der findes en sammenhæng mellem pris og rating ud fra det enkelte flyselskab.

Gennem disse 2 dataset vil vi svare på følgende spørgsmål (Se List of Challenges) 

# List of used technologies:
* Pandas
* Selinium (for scraping www.kayak.dk)
* Beautiful Soup
* Plotly (for data visualization)
* sklearn (for machine learning)
* sns (for data visualization)
* wordcloud (for machine learning)
* nltk (for word steming, stopwords)

# Installation guide (if any libraries need to be installed)
Dette projekt tager udgangspunkt i det udleverede docker miljø. Kun et biblotek skal installeres (plotly)
Install plotly:
```sh
   pip install plotly==5.8.0
   ```
Install selenium webdriver

# User guide (how to run the program)
Clone docker image...
Kør 'scrape-single-flight.py'
Kør begge notebooks
# Status (What has been done (and if anything: what was not done))
Vi har færdiggjort alle spørgsmål vi har stillet os selv.

# List of Challenges you have set up for your self (The things in your project you want to highlight)
1. Scrape fra Kayak. Load 50 resultater fra hver dag med selenium. Url string setup: https://www.momondo.dk/flight-search/CPH-63cy/2022-07-14-flexible-2days/2022-07-25-flexible-2days/2adults?sort=bestflight_a  https://www.momondo.dk/flight-search/{LuftHavnFra}-{LuftHavnTil}/{afrejseTidspunkt}-{flexible-2days}/{hjemrejseTidspunkt}-flexible-2days/{antalPersoner}?sort=bestflight_a
2. Hent data omkring:  pris/person antal stop / direkte selskab(er) url destination antal timer afgangs tidspunkter (7 til 10 - morgen. 10 til 17 dag. 17 til 22 aften. 22 til 7 nat.)
3. Scrap data fra tidsintervalet 2022-07-19 til 2022-08-15
4. Sende en mail med fly rejser til Cypern hver dag gennem et cron job hostet på en server
5. Hvilket tidspunkt er billigst at rejse i? 
6. Hvilket selvskab er billigst at flyve med? 
7. Hvilke dage kan man rejse billigst (ugedag) i sommerferie perioden? 
8. Er der sammenhæng mellem antal stop/total rejsetid og pris?
9. Lav et heatmap for at se tendenser. Undersøg disse tendenser nærmere 
10. Lav en sentiment analyse af reviews på flyseleskaber
11. Brug i forlængelse af sentiment analyse, machine learning til at finde ud af om et review's tekst er positivt eller negativt, samt hvilke ord som er postive og/eller negative
12. Findes der nogen sammenhæng mellem længde af review teksten og ratingen? 




