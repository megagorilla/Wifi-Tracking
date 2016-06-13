Contents
Inleiding	2
UML	3
Toekomstig werk	4
Conclusie	5

 
Inleiding
In dit verslag wordt de uitwerking van de opdracht “locatie-bepaling op basis van wifi” beschreven. Allereerst zal er een beschrijving worden geleverd van de klassen, compleet met uitleg werking en een UML. Ook zal er een flowchart in dit hoofdstuk voorkomen die een korte globale uitleg van het systeem geeft. Daarna zal er worden gekeken naar toekomstig werk, wat nog kan worden toegevoegd aan het project en wat kan worden vervangen voor een betere werking van het product. Ook zal nog een conclusie worden gegeven voor de onderzoeksvraag. 
 
UML
Classdiagram
 
Figuur 1 Classdiagram van server en sniffer
Hierboven staat een korte uitleg van het classdiagram van de server en de sniffer. Waarbij er een informatie wordt uitgedeeld tussen sniffer en SockServer. Hieronder korte uitleg over de classes.
Server
De server class is de controller van het systeem, het is de class die objecten maakt van andere classes en de database genereert als deze nog niet bestaat. De aanroep van functies regelt de vulling van database met locaties, die ook weer uit de database worden gehaald. In-depth uitleg van de functies staan in de code zelf in de vorm van comments.
Calculator
De calculator class bevat de methodes om locatie berekeningen te maken. Deze methodes worden aangeroepen vanuit een centrale methode, deze kiest uit of er een 2d locatie moet worden berekend of een 3d locatie. Ook bestaat de Class uit een methode die een weergave geeft van de radii en de locatie die daarop is berekent
Databaseserver
De server Databaseserver is een class die de communicatie met de database regelt. Er staat een functie in die de class in verbinding stelt met de database en een functie die deze verbinding uitschakelt. Verder staan er nog functies in die informatie in de database zetten, de informatie in de database updaten en de informatie in de database verwijdert. Er staat ook een functie in geprogrammeerd die SQL bestanden buiten de class kan aanroepen en uitvoeren voor het gemakkelijk toevoegen van SQL bestanden. Telkens als er een functie wordt uitgevoerd wordt er verbinding gemaakt met database, de query uitgevoerd en de verbinding verbroken. De natuurlijke staat van de class is dus ook dat er geen verbinding is met de database, dit om errors tegen te gaan.
 
Database
Als de database nog niet bestaat wordt deze aangemaakt tijdens het opstarten van de server.
 
Figuur 2 De database 

Flowcharts
 
Op het moment dat de sniffer
 
Gebruiksaanwijzing
Om gebruik te maken van dit systeem zijn een aantal voorbereidingen en materialen nodig. Hier zal worden uitgelegd welke stappen ondernomen moeten worden om dit systeem werkend te krijgen.
Materieel
Om dit systeem te gebruiken zijn in ieder geval 3 wifi adapters nodig. Om de kwaliteit van het systeem te garanderen moeten deze adapters van hetzelfde type zijn. 
Computer
Verder is er een computer nodig voor de centrale server. Deze computer kan een reguliere PC zijn (X86/X64) of een raspberry pi (ARM) en moet een linux distributie (debian)draaien met root(sudo) rechten. Ook moet deze computer aan een centrale router verbonden zitten. In kleine opstellingen kan deze computer ook gebruikt worden om direct de software voor de sniffers op te draaien. In grotere opstellingen moet er per sniffer een losse computer gebruikt worden die aan dezelfde vereisten moet voldoen als de eerdergenoemde computer.
Afhankelijkheden
Voordat het systeem gestart kan worden moeten er software bibliotheken en andere softwarepakketten geïnstalleerd worden. Eerst zal de goede driver voor de wifi adapters geïnstalleerd moeten worden als die al niet automatisch gedaan is. Daarnaast zullen de volgende pakketten geïnstalleerd moeten worden:
Voor de server:
Naam	Link
Python 2.7	https://www.python.org/

Scipy	https://www.scipy.org/

Numpy	http://www.numpy.org/

MySQLdb	http://mysql-python.sourceforge.net/MySQLdb.html

Matplotlib	http://matplotlib.org/

PyCrypto	https://pypi.python.org/pypi/pycrypto


Voor de sniffers:
Naam	Link
Python 2.7	https://www.python.org/

Aircrack-ng	http://www.aircrack-ng.org/

PyCrypto	https://pypi.python.org/pypi/pycrypto


Database
Er moet een MySQL database worden aangemaakt met de naam “tracking”, en een user met de username “root” en wachtwoord “Biertaart”. Verder worden de nodige tabellen automatisch gegenereerd wanneer de server gestart word.
Website
Als de gebruiker wenst gebruik te maken van de website zal er een apache server moeten worden geïnstalleerd waar ook PHP code op kan worden uitgevoerd.
Gebruik
Om de server te starten moet er met een terminal naar de map “server” genavigeerd worden om daar het volgende commando uit te voeren “sudo python server.py”.
Om de sniffer te starten moet er een kopie van de map “sniffer” worden gemaakt. Vervolgen kan met het volgende terminal commando de sniffer gestart worden “sudo python sniffer.py”. Als de gebruiker al weer welk apparaat en kanaal de sniffer moet gaan gebruiken kan dit met de volgende argumenten worden meegegeven “sudo python sniffer.py <device> <channel>”.
 
Toekomstig werk
 
Conclusie

