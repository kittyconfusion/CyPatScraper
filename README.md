## CyberPatriot Scoreboard Scraper ##
Used for displaying team information from the CyberPatriot competition's live [scoreboard](https://scoreboard.uscyberpatriot.org/index.php?sort=Total).

### Example ###
A terminal with a monospaced font should produce an output such as this:
![scoreboard-preview](https://github.com/kittyconfusion/CyPatScraper/assets/144735570/b7cba5c5-d5f5-4404-889f-6fe701f28ce1)

### Getting Running ###
The Python modules `Beautiful Soup 4`, `Requests`, and `Tabulate` are required to run.

If using pip, run the following:
```
pip install bs4
pip install requests
pip install tabulate
``` 

Configure Team IDs, Location, and if applicable, Tier/Division to search within. Change TopTeams to replace listed teams with the top 10 teams.
