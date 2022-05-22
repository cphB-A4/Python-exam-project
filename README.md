# Python-exam-project
## Python flight webscraper 
Group members:
* [Mathias P.](cph-mp557@cphbusiness.dk)
* [Mustafa](...)
* [Markus](...)

## Description
Projektet har i alt 3 'grene' og er alle med til at besvare spørgsmålene vi stillede os selv inden vi begyndte med projeket (se spørgsmål længere nede).

1. Gren 1(Hent data om fly til Cypern i perioden 2022-07-11 til 2022-07-20(+-2 dage) og send brugeren en mail hver dag kl 10 med resultaterne):
Send brugeren en mail med info omrking:
pris, destination, tidsinterval (både frem og tilbage) , antal stop,(både frem og tilbage), flyselskab(er) og url
Gennem hosting hos Amazon Web Services bliver der hver dag via et cronjob sendt en mail med 12 tur-retur rejser til Cypern. Gennem disse mails vil det (forhåbentligt) være muligt at skaffe sig en billig flybillet.

2. Gren 2(Hente data om fly til Cypern i perioden 2022-07-19 til 2022-08-15 for at svare på spørgsmål)
Ved brug af selenium web scrappes siden www.kayak.dk og data omkring pris, destination, tidsinterval, antal stop, flyselskab(er) og url bliver hentet. Derefter undersøges tendenser og dataen bliver visualiseret. Se under afsnittet 'List of Challenges'. Her bliver der taget udgangspunkt i en enkeltbillet.

3. Gren 3(Hente data om fly reviews og lave en machine learning model ud fra content [link til dataset](www.google.com))
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

# User guide (how to run the program)
Clone docker image...
# Status (What has been done (and if anything: what was not done))

# List of Challenges you have set up for your self (The things in your project you want to highlight)
1. Scrape fra Kayak. Load 50 resultater fra hver dag med selenium. Url string setup: https://www.momondo.dk/flight-search/CPH-63cy/2022-07-14-flexible-2days/2022-07-25-flexible-2days/2adults?sort=bestflight_a  https://www.momondo.dk/flight-search/{LuftHavnFra}-{LuftHavnTil}/{afrejseTidspunkt}-{flexible-2days}/{hjemrejseTidspunkt}-flexible-2days/{antalPersoner}?sort=bestflight_a
2. Hent data omkring:  pris/person antal stop / direkte selvskab(er) hjemmeside destination antal timer billet type link afgangs tidspunkter (7 til 10 - morgen. 10 til 17 dag. 17 til 22 aften. 22 til 7 nat.)
3. Vælg en destination og et tidsinterval vi vil tage udgangspunkt i. (Eks 2022-07-14-flexible-2days til 2022-07-25-flexible-2days)
4. Hvilket tidspunkt er billigst at rejse i? 
5. Hvilket selvskab er billigst at flyve med? 
6. Lav en sentiment analyse af reviews på flyseleskaber
7. Brug i forlængelse af sentiment analyse, machine learning til at finde ud af om et review er positivt eller negativt, samt hvilke ord som er postive og/eller negative
8. Lav et heatmap for at se tendenser. Undersøg disse tendenser nærmere 
9. Er det billigst at bestille fly om tirsdagen?   Hvordan man installere chromeDriver: https://www.swtestacademy.com/install-chrome-driver-on-mac/



