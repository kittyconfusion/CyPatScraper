## CyberPatriot Scoreboard Scraper ##
Used for displaying team information from the CyberPatriot competition's live [scoreboard](https://scoreboard.uscyberpatriot.org/index.php?sort=Total).

### Example ###
A terminal with a monospaced font should produce an output such as this.
![image](https://github.com/kittyconfusion/CyPatScraper/assets/65476906/36a32c11-379e-4072-b74f-7bde83e1120e)

### Getting Running ###
The Python modules `Beautiful Soup 4` and `Requests` are required to run.

If using pip, run `pip install bs4` and `pip install requests` to install. 

Depending on whether Cisco scores are out (which will require the flipping of the HasCisco flag) and the current round, various table parameters may need to be specified in the script. If you are running into an error or garbage data, please review these settings.
