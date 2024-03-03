# IPTV Platforma
![logo white](https://github.com/TonnyG95/iptv/assets/47572512/27638efe-5a19-4202-91bd-edfbcdb3f58a)
## O projektu

Ova IPTV platforma predstavlja revolucionarno rješenje za distribuciju digitalnog sadržaja koristeći Django framework na backendu i Bootstrap na frontendu. Dizajnirana s fokusom na automatizaciju i korisničko iskustvo, ova platforma nudi kompletan set alata za upravljanje IPTV uslugama, uključujući automatizirano kreiranje korisnika, upravljanje pretplatama, integrirane financijske transakcije preko PayPal-a, i napredne administrativne funkcionalnosti. Uz potpunu integraciju s AWS infrastrukturom i Google reCAPTCHA sigurnosnim mehanizmima, IPTV platforma pruža stabilno, sigurno i lako upravljivo okruženje za distribuciju digitalnog sadržaja.

![smartmockups_ltaujkbk](https://github.com/TonnyG95/iptv/assets/47572512/731b1ef4-cded-4bca-850f-591f4e8795cb)

## Ključne značajke

### Automatizacija Korisničkog Računa

- Automatsko kreiranje korisničkih računa i M3U korisničkih imena i lozinki.
- Automatizirane email obavijesti korisnicima o statusu pretplate.
- Automatsko gašenje usluge nakon isteka pretplate i obavijesti adminu o neobnovljenim pretplatama.

### Financijske Transakcije i PayPal Integracija

- Kompletna integracija s PayPalom za sigurno online plaćanje.
- Korisnički novčanici za upravljanje sredstvima i olakšano produživanje pretplata.
- Mogućnost manualnog ažuriranja korisničkih novčanika od strane admina za alternativne načine plaćanja.

### Napredni Admin Panel

- Robustan admin panel za potpunu kontrolu nad korisnicima, pretplatama, i sadržajem.
- Dinamičko upravljanje sadržajem dashboarda, uključujući tekstove, slike, i custom linkove.
- Pregled i upravljanje zadnjim transakcijama i direktna komunikacija s korisnicima.


### Sigurnost i Prilagodljivost

- Integracija s Google reCAPTCHA za dodatnu sigurnost registracijskog procesa.
- Prilagodljivost planova pretplate i mogućnost odabira između M3U i MAG uređaja pri kupnji.
- AWS S3 integracija za pouzdano hostanje statičkih resursa.

## Tehnologije

### Backend

Ova aplikacija koristi Djnago framework za backend i aplikacija je kompletno napisana u Python programskom jeziku, osim Python i Djanga ova aplikacija koristi i SQLite baze podataka za spremanje podataka, tako da je baza lokalna zato cu vam ovdje napisati login podatke za admina i demo usera, poslje vi mozete sebi sve prilagoditi, isto tako Django se lako moze povezati sa remonte (udaljenom) bazom podataka i migracija na remote bazu podataka je super jednostavna i brza.

### Frontend

Iako primarni focus ove aplikacije nije bio na frontendu vec na backendu opet sam se pobrinio da aplikacija izgleda dobro i da je u potpunosti rasponzivna tako da i useri na manjim ekranima nece biti zapostavljeni, Frontend framework koristen za ovu aplikaciju je Bootstrap posto mi je to bio najbrzini i najjednostavniji nacin da napravim frontend sa gotivim komponentama koje su rasponzivne.

### Payment procesori

Ova Django aplikacija je intrgrirana sa PayPal-om kao jedinim paymnent procesorom posto s obzirom da se radi o IPTV usluzi Stripe i vecinu drugih payment procesora nije bilo ni potrbne instalirati jel se nebi mogli koristi za ovu uslugu, tako da smo odlucili samo napraviti integraciju sa PayPal-om.

### Sigurnost

Ova aplikacija je integrirana sa Google reCAPTCHA sigurnosnim mehanizmom kako bi se izbjegle spam poruke i isto tako kako se botovi nebi mogli registirati na aplikaciju i bespotrbeno spremneti korisnike i admine, ova integracija je jednostavna i brza jedino sto admin mora kreirati svoje reCAPTCHA podatke koje moze kreirati [ovdje](https://www.google.com/recaptcha/) i upisati ih u env.py datoteku, u tu datotku admin ce morati upisati potrbne podatke za sve integracije koje su implementirane.

### AWS Infrastruktura

Ova aplikacija je u startu kreirana sa fokusom na sigurnost,pouzdanost i skalabiln, tako da od pocetka rada na ovoj aplikaciji smo kolega kojem sam radio ovu aplikaciju i ja odlucili da ju intergiramo sa sto je vise moguce AWS (Amazon Web Services) funkcionalnosti jel smo od stara znali da cemo ju deployati na AWS. Tako da ova aplikacija je u potpunosti optimizirana za deployment na usluzi **Elastic Beanstalk** isto tako u potpunosti je optimizirana i za koristenje **AWS S3 (Simple Storage Service)** tako da sve staticne datoteke kao sto su slike, JavaScript i CSS datoteke koriste S3 za skladistenje i tako se smanjuje latencija i povećava skalabilnost ove aplikacije.


## Značajke

Ova django aplikacija ima jako puno korisnih funkcija koje svaki IPTV prodavac moze pronaci korisne, pocetiti cemo sa najvaznijim a to je admin panel opisati cu vam neke od značajki koje admin panel ove aplikacije ima, fokus ove aplikacija je bio automatizirati sto je vise moguce funkcija kako bi admin ustedio vrijeme a opet da ne propusti nista sto je bitno za IPTV prodavca. Tako da od registracije koristinka do gasenja usluge korisniku je sve automatizirano i admin je obavjest o svemu na e-mail. Ispod cu vam navesti neke od automatizacija koje ova aplikacija ima.

### Kontakt Forma

Ova aplikacija ima u sebi ugradjenu kontakt formu koja je najbrzi i najlaksi nacin za korisnika da kontaktira admina i dobije potrebnu pomoc.

![image](https://github.com/TonnyG95/iptv/assets/47572512/88a83478-105b-4da5-b236-713c4ea62c51)

Nakon sto je korisnik poslao email adminu on ce o tom biti obavjesten uz pomoc django messages, Isto tako admin ima pristup kontakt formi i moze vidjeti sve e-mailove koje su mu poslali klijenti kroz admin panel, ali isto tako ce biti obavjesten i na e-mail

![image](https://github.com/TonnyG95/iptv/assets/47572512/fc1d4041-6858-4761-ace8-8aa0d86c7ce5)

### Obavjest o kupnji usluge

Posto je za svakog admina najvaznija informacija da vidi kad je netko kupio uslugu i koju uslugu je kupio, ova aplikacija u sebi ima ugradjenu funkciju koja ce obavjestiti admina na e-mail za svaki kupnju ili produzivanje usluge, E-Mail koji se salje adminu mu dinamican i koristi ce podatke o tipu usluge i korisniku tako da ako je korisnik kupio M3U uslugu admin ce u emailu vidjeti da je korisnik kupio M3U uslugu, zajedno sa automatski generiranim M3U Userom, M3U password i M3U linkom koji ce korisnik koristiti za pristup usluzi. Ukoliko je koristnik kupio MAG uslugu adminu ce biti prosljedjeni podatci za Mag model, Mag mac adressu i Mag Serijski Broj

### Obavjest o produzivanju usluge

Ova aplikacija ima u sebi ugradjenu funkciju koja ce obavjestiti admina na e-mail kad je vec postojuci korisnik produzio svoju uslugu i kad ju je platio zajedno sa informacijama do kojeg datuma je usluga produzena, Taj datum je automatski izracuna ovisino o planu preplate koja se moze podesiti kroz admin panel 

![image](https://github.com/TonnyG95/iptv/assets/47572512/10a71ab1-8226-40bb-9fc3-998fbbb65603)

Zahvaljujuci podatku "Trajanje u danima" aplikacija ce sama izracunati vazenje usluge tako da se admin nece morati brinuti oko tih podataka.

### Obavjest o isteku usluge

Ova aplikacija ima funkciju koja ce obavjesiti admina 5 dana prije isteka usluge korisniku zajedno sa informacijama o kojem korisniku se radi i do kad mu traje usluga tako da ce admin uvijek biti u toku kad nekom korisniku istice preplata. 

### Obavjest o gasenju usluge

Ukoliko korisnik nije produzio svoju uslugu u roku 5 dana od isteka njegove usluge admin ce dobiti sve potrbne informacije da bi mogao korisniku ugasiti uslugu, isto tako aplikacija ce korisnika automatski obavjesti da je njegova usluga ugasena zato sto nije produzio uslugu.

### Obavjest korisniku o kupnji ili produzetku usluge

Korisnik nakon svake kupnje ili produzetka usluge dobije povratni e-mail u kojem mu se potrvdjuje da je kupio ili produzio uslugu zajedno sa njegovim podacima za pristup usluzi (M3U ili MAG ), cjenom usluge i datumom isteka usluge.

### Obavjest korisniku da mu usluga istice za 5 dana 

Napravili smo funkciju koja ce korisnika obavjesti na e-mail da mu usluga istice za 5 dana, osim e-maila korisnik ako ode na stranicu "Preplate" ima jasna doznanja da mu usluga istice uskoro i potrebno je samo da mu je balans dovoljan za produzivanje usluge i klikom na button produzi njemu se odmah naplati i produzi usluga, Naravno ukoliko balans nije dovoljan za produzivanje vidjeti ce obavjest da nema dovoljno sredstava u novaniku i da si nadoplati novcanik da bi produzio uslugu.

![image](https://github.com/TonnyG95/iptv/assets/47572512/bbf7d4d7-7ad5-47af-b167-e134033e41e6)

### Obavjest korisniku o isteku usluge

Isto tako korisnik ce biti obavjesten putem e-mail na dan kad mu je usluga istekla da ima 5 dana da produzi uslugu u protivnom ce izgubiti pristup usluzi 

### Obavjest o gasnju usluge

Ukoliko je proslo 5 dana od isteka usluge i korisnik nije produzio uslugu aplikacija ce mu poslati e-mail da je usluga ugasena i da mu je potrebno da ga produzi ponovo ukoliko ju zeli koristi, isto tako odmah ce i admin biti obavjest da treba tom korisniku ugasiti uslugu

### Obavjest o nadoplati novcanika

Naravno bitna obavjest je i potvrdni e-mail koji se salje korisniku kad je nadoplatio novcanik za uslugu, tako da smo napravili funkciju koja ce poslati korisniku e-mail da je uspjesno nadoplatio svoj novcanik zajedno sa iznosom koji je uplatio i podatcima o PayPal transakciji. 

### Ostale obavjesti 

Sve ove gore navedene obavjesti nisu jedine, tu su jos obavjesti vezano za zahvalu korisniku za produzivanje usluge, aktivacijski e-mail nakon kreiranja racuna, tu je naravno i 2FA koji je u ovoj verziji iskljucen posto je aplikacija u toku razvoja bila za vrijeme kreiranja ove dukumentacija.

