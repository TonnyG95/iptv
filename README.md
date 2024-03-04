# IPTV Platforma

![logo white](https://github.com/TonnyG95/iptv/assets/47572512/27638efe-5a19-4202-91bd-edfbcdb3f58a)

## O projektu

Ovaj projekt razvijen je kako bi olakšao i automatizirao upravljanje IPTV uslugama za prodavače. Koristeći Django framework na backendu i Bootstrap na frontendu, platforma pruža niz alata za efikasno upravljanje korisničkim računima, pretplatama i financijskim transakcijama. S integracijom PayPal-a za plaćanja, Google reCAPTCHA za sigurnost i potpunu podršku za AWS infrastrukturu, ova platforma cilja na pojednostavljenje operacija i uštedu vremena na rutinskim zadacima. Iako možda nije revolucionarna u tehničkom smislu, njezina vrijednost leži u automatizaciji procesa koji IPTV prodavačima omogućuje da se usredotoče na važnije aspekte poslovanja.

![smartmockups_ltaujkbk](https://github.com/TonnyG95/iptv/assets/47572512/731b1ef4-cded-4bca-850f-591f4e8795cb)

# Sadržaj

- [O projektu](#o-projektu)
- [Ključne značajke](#ključne-značajke)
  - [Automatizacija Korisničkog Računa](#automatizacija-korisničkog-računa)
  - [Financijske Transakcije i PayPal Integracija](#financijske-transakcije-i-paypal-integracija)
  - [Napredni Admin Panel](#napredni-admin-panel)
  - [Sigurnost i Prilagodljivost](#sigurnost-i-prilagodljivost)
- [Tehnologije](#tehnologije)
  - [Backend](#backend)
  - [Frontend](#frontend)
  - [Payment procesori](#payment-procesori)
  - [Sigurnost](#sigurnost)
  - [AWS Infrastruktura](#aws-infrastruktura)
- [Automatizirane Obavijesti](#automatizirane-obavijesti)
  - [Kontakt Forma](#kontakt-forma)
  - [Obavijest o kupnji usluge](#obavijest-o-kupnji-usluge)
  - [Obavijest o produživanju usluge](#obavijest-o-produživanju-usluge)
  - [Obavijest o isteku usluge](#obavijest-o-isteku-usluge)
  - [Obavijest o gašenju usluge](#obavijest-o-gašenju-usluge)
  - [Obavijest korisniku o kupnji ili produžetku usluge](#obavijest-korisniku-o-kupnji-ili-produžetku-usluge)
  - [Obavijest korisniku da mu usluga ističe za 5 dana](#obavijest-korisniku-da-mu-usluga-ističe-za-5-dana)
  - [Obavijest korisniku o isteku usluge](#obavijest-korisniku-o-isteku-usluge)
  - [Obavijest o gašenju usluge](#obavijest-o-gašenju-usluge-1)
  - [Obavijest o nadoplati novčanika](#obavijest-o-nadoplati-novčanika)
  - [Ostale obavijesti](#ostale-obavijesti)
- [Admin Panel](#admin-panel)
  - [Brandiranje](#brandiranje)
  - [Upravljanje Pretplatama](#upravljanje-pretplatama)
  - [Upravljanje Korisnicima](#upravljanje-korisnicima)
  - [Upravljanje Novčanicima](#upravljanje-novčanicima)
- [Obavijesti](#obavijesti)
- [Planovi Za Aplikaciju](#planovi-za-aplikaciju)
- [Cron Jobs](#cron-jobs)
- [Deployment na AWS](#deployment-na-aws)
- [Cron Jobs Workaround](#cron-jobs-workaround)
- [Kreiranje Cron Job-a](#kreiranje-cron-job-a)
- [Kreiranje Elastic Beanstalk aplikacije](#kreiranje-elastic-beanstalk-aplikacije)
- [Kreiranje S3 Bucketa](#kreiranje-s3-bucketa)
- [Code Potreban Za S3 Bucket](#code-potreban-za-s3-bucket)
- [Kako Pokrenuti Aplikaciju Lokalno?](#kako-pokrenuti-aplikaciju-lokalno)
- [Podatci za prijavu](#podatci-za-prijavu)
- [Zaključak](#zaključak)


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

Ova aplikacija koristi Django framework za backend i aplikacija je kompletno napisana u Python programskom jeziku. Osim Pythona i Djanga, ova aplikacija koristi i SQLite baze podataka za spremanje podataka, tako da je baza lokalna. Zato ću vam ovdje napisati login podatke za admina i demo korisnika, poslije vi možete sebi sve prilagoditi. Isto tako, Django se lako može povezati sa udaljenom bazom podataka i migracija na remote bazu podataka je super jednostavna i brza.

### Frontend

Iako primarni fokus ove aplikacije nije bio na frontendu već na backendu, opet sam se pobrinuo da aplikacija izgleda dobro i da je u potpunosti responzivna, tako da i korisnici na manjim ekranima neće biti zapostavljeni. Frontend framework korišten za ovu aplikaciju je Bootstrap, pošto mi je to bio najbrži i najjednostavniji način da napravim frontend s gotovim komponentama koje su responzivne.

### Payment procesori

Ova Django aplikacija je integrirana s PayPal-om kao jedinim payment procesorom, pošto s obzirom da se radi o IPTV usluzi, Stripe i većina drugih payment procesora nije bila ni potrebna instalirati jer se ne bi mogli koristiti za ovu uslugu. Tako da smo odlučili samo napraviti integraciju s PayPal-om.

### Sigurnost

Ova aplikacija je integrirana s Google reCAPTCHA sigurnosnim mehanizmom kako bi se izbjegle spam poruke i isto tako kako se botovi ne bi mogli registrirati na aplikaciju i bespotrebno spameti korisnike i admine. Ova integracija je jednostavna i brza, jedino što admin mora kreirati svoje reCAPTCHA podatke koje može kreirati [ovdje](https://www.google.com/recaptcha/) i upisati ih u env.py datoteku. U tu datoteku admin će morati upisati potrebne podatke za sve integracije koje su implementirane.

### AWS Infrastruktura

Ova aplikacija je u startu kreirana s fokusom na sigurnost, pouzdanost i skalabilnost, tako da od početka rada na ovoj aplikaciji smo kolega kojem sam radio ovu aplikaciju i ja odlučili da ju integriramo s što je više moguće AWS (Amazon Web Services) funkcionalnosti jer smo od starta znali da ćemo ju deployati na AWS. Tako da ova aplikacija je u potpunosti optimizirana za deployment na usluzi **Elastic Beanstalk** i isto tako je u potpunosti optimizirana i za korištenje **AWS S3 (Simple Storage Service)** tako da sve statične datoteke kao što su slike, JavaScript i CSS datoteke koriste S3 za skladištenje i tako se smanjuje latencija i povećava skalabilnost ove aplikacije.


## Automatizirane Obavijesti

Ova django aplikacija ima jako puno korisnih funkcija koje svaki IPTV prodavač može pronaći korisne. Počet ćemo s najvažnijim, a to je admin panel. Opisat ću vam neke od značajki koje admin panel ove aplikacije ima. Fokus ove aplikacije je bio automatizirati što je više moguće funkcija kako bi admin uštedio vrijeme a opet da ne propusti ništa što je bitno za IPTV prodavača. Tako da od registracije korisnika do gašenja usluge korisniku je sve automatizirano i admin je obaviješten o svemu na e-mail. Ispod ću vam navesti neke od automatizacija koje ova aplikacija ima.

### Kontakt Forma

Ova aplikacija ima u sebi ugrađenu kontakt formu koja je najbrži i najlakši način za korisnika da kontaktira admina i dobije potrebnu pomoć.

![image](https://github.com/TonnyG95/iptv/assets/47572512/88a83478-105b-4da5-b236-713c4ea62c51)

Nakon što je korisnik poslao email adminu on će o tom biti obaviješten uz pomoć django messages. Isto tako, admin ima pristup kontakt formi i može vidjeti sve e-mailove koje su mu poslali klijenti kroz admin panel, ali isto tako će biti obaviješten i na e-mail.

![image](https://github.com/TonnyG95/iptv/assets/47572512/fc1d4041-6858-4761-ace8-8aa0d86c7ce5)

### Obavijest o kupnji usluge

Pošto je za svakog admina najvažnija informacija da vidi kad je netko kupio uslugu i koju uslugu je kupio, ova aplikacija u sebi ima ugrađenu funkciju koja će obavijestiti admina na e-mail za svaku kupnju ili produživanje usluge. E-Mail koji se šalje adminu je dinamičan i koristit će podatke o tipu usluge i korisniku tako da ako je korisnik kupio M3U uslugu admin će u emailu vidjeti da je korisnik kupio M3U uslugu, zajedno sa automatski generiranim M3U korisnikom, M3U lozinkom i M3U linkom koji će korisnik koristiti za pristup usluzi. Ukoliko je korisnik kupio MAG uslugu adminu će biti proslijeđeni podaci za Mag model, Mag MAC adresu i Mag serijski broj.

### Obavijest o produživanju usluge

Ova aplikacija ima u sebi ugrađenu funkciju koja će obavijestiti admina na e-mail kad je već postojeći korisnik produžio svoju uslugu i kad ju je platio zajedno sa informacijama do kojeg datuma je usluga produžena. Taj datum je automatski izračunat ovisno o planu pretplate koji se može podesiti kroz admin panel.

![image](https://github.com/TonnyG95/iptv/assets/47572512/10a71ab1-8226-40bb-9fc3-998fbbb65603)

Zahvaljujući podatku "Trajanje u danima" aplikacija će sama izračunati važenje usluge tako da se admin neće morati brinuti oko tih podataka.

### Obavijest o isteku usluge

Ova aplikacija ima funkciju koja će obavijestiti admina 5 dana prije isteka usluge korisniku zajedno sa informacijama o kojem korisniku se radi i do kad mu traje usluga tako da će admin uvijek biti u toku kad nekom korisniku ističe pretplata.

### Obavijest o gašenju usluge

Ukoliko korisnik nije produžio svoju uslugu u roku 5 dana od isteka njegove usluge admin će dobiti sve potrebne informacije da bi mogao korisniku ugasiti uslugu, isto tako aplikacija će korisnika automatski obavijestiti da je njegova usluga ugašena zato što nije produžio uslugu.

### Obavijest korisniku o kupnji ili produžetku usluge

Korisnik nakon svake kupnje ili produžetka usluge dobije povratni e-mail u kojem mu se potvrđuje da je kupio ili produžio uslugu zajedno sa njegovim podacima za pristup usluzi (M3U ili MAG), cijenom usluge i datumom isteka usluge.

### Obavijest korisniku da mu usluga ističe za 5 dana

Napravili smo funkciju koja će korisnika obavijestiti na e-mail da mu usluga ističe za 5 dana. Osim e-maila, korisnik ako ode na stranicu "Pretplate" ima jasna doznanja da mu usluga ističe uskoro i potrebno je samo da mu je balans dovoljan za produživanje usluge i klikom na button produži njemu se odmah naplati i produži usluga. Naravno, ukoliko balans nije dovoljan za produživanje, vidjet će obavijest da nema dovoljno sredstava u novčaniku i da si nadoplati novčanik da bi produžio uslugu.

![image](https://github.com/TonnyG95/iptv/assets/47572512/bbf7d4d7-7ad5-47af-b167-e134033e41e6)

### Obavijest korisniku o isteku usluge

Isto tako, korisnik će biti obaviješten putem e-maila na dan kad mu je usluga istekla da ima 5 dana da produži uslugu u protivnom će izgubiti pristup usluzi.

### Obavijest o gašenju usluge

Ukoliko je prošlo 5 dana od isteka usluge i korisnik nije produžio uslugu, aplikacija će mu poslati e-mail da je usluga ugašena i je potrebno da je kupi ponovo ukoliko ju želi koristiti, isto tako odmah će i admin biti obaviješten da treba korisniku ugasiti uslugu.

### Obavijest o nadoplati novčanika

Naravno, bitna obavijest je i potvrdni e-mail koji se šalje korisniku kad je nadoplatio novčanik za uslugu. Tako da smo napravili funkciju koja će poslati korisniku e-mail da je uspješno nadoplatio svoj novčanik zajedno sa iznosom koji je uplatio i podacima o PayPal transakciji.

### Ostale obavijesti

Sve ove gore navedene obavijesti nisu jedine. Tu su još obavijesti za zahvalu korisniku za produživanje usluge, aktivacijski e-mail nakon kreiranja računa i e-mail koji se šalje korisniku kad je aktivirao svoj račun.

## Admin Panel

Ova aplikacija ima robustan Admin panel koji adminu omogućava upravljanje kompletnom platformom sa jednog mjesta, od tekstova prikazanih na frontendu do upravljanja korisnicima, novčanicima, pretplatama i naravno kompletno brandiranje aplikacije.

### Brandiranje

Najvažnije za svakog admina je da platformu može prilagoditi svom brandu. Ovo je moguće u admin panelu. Admin može postaviti svoj logo u 2 verzije: klasičan i svijetli, pošto je bila u planu implementacija dark moda, ali taj dio nije uključen u ovoj verziji. Tu su i mogućnosti za linkove do društvenih mreža koje se prikazuju kroz cijelu aplikaciju, uključujući i e-mail obavijesti. Osim toga, admin može dodati i custom linkove ako želi, npr. linkovi do njegove web stranice, politike privatnosti i uvjeta korištenja. Par screenshotova će biti prikazano ovdje, Isto tako kompletan branding se koristi i u e-mail obavjestima.

1. **Glavne postavke**

![image](https://github.com/TonnyG95/iptv/assets/47572512/e238b260-0c00-49b5-b04c-def3f7df9b62)

2. **Postavke društvenih mreža**

![image](https://github.com/TonnyG95/iptv/assets/47572512/de947a2d-6b10-4da3-b48f-cd48aae87ff5)

3. **Frontend tekstovi**

![image](https://github.com/TonnyG95/iptv/assets/47572512/86ca625f-80e6-4480-9007-5fac88e3ebf2)

4. **Kartice na početnoj stranici**

![image](https://github.com/TonnyG95/iptv/assets/47572512/9f399a1f-90cb-4c6e-ac1b-aaeca5dba4ba)

5. **Linkovi specifični za e-mail obavijesti**

![image](https://github.com/TonnyG95/iptv/assets/47572512/9ed3dfdd-e2be-40d1-9a77-5ace2c59b442)

### Upravljanje Pretplatama

Naravno, najvažnija opcija je upravljanje planovima za pretplatu, to uključuje ime plana, trajanje u danima, cijena usluge, i značajke koje će razdvajati planove. Isto tako, upravljanje postojećim pretplatama svojih korisnika.

**Upravljanje Planovima**

![image](https://github.com/TonnyG95/iptv/assets/47572512/c1864f6c-da04-493a-a0bc-dd80cb4ef5ca)

**Upravljanje aktivnim pretplatama**

![image](https://github.com/TonnyG95/iptv/assets/47572512/9b94870e-2958-46f6-8535-d13451a60576)

Opcije:

- **Korisnik obaviješten o isteku**
- **Admin obaviješten o isteku**
- **Korisnik obaviješten o prekidu usluge**

Ove opcije su namijenjene za automatizaciju obavijesti tako izbjegavamo da svaki dan šaljemo obavijest korisniku, tako da kad se korisnika obavijesti ta polja će se automatski uključiti a nakon produživanja usluge te opcije će se automatski isključiti, tako da se korisniku ne zatrpava inbox s istim e-mailovima što će ujedno i sprječiti da vaše poruke budu označene kao spam. Kao što imena kažu, ukoliko admin želi ručno obavijestiti korisnika o isteku usluge, može samo kliknuti na checkboxove i to će pokrenuti slanje e-mail obavijesti korisniku. Ali u većini slučajeva te opcije admin nikad neće koristiti jer to će aplikacija sama regulirati. Opcije kao checkbox za "Is MAG Active" će isto biti automatizirane i ako je checkbox uključen to će korisniku odmah biti prikazano na početnoj stranici dashboarda. Ukoliko korisnik koristi M3U uslugu, iste postavke za korisnika se mogu pronaći u "User Profiles", ne u "Subscriptions", pošto je M3U povezan s profilom korisnika jer će automatski kreirati nove M3U podatke čim se korisnik registira na web stranicu.

**Admin -> Subscriptions**

![image](https://github.com/TonnyG95/iptv/assets/47572512/268e3adb-822b-47f1-adb1-fe14ad92a395)

**Admin -> User Profiles**

![image](https://github.com/TonnyG95/iptv/assets/47572512/8d65d162-48bc-446b-963f-7359773e6388)

**Dashboard -> Početna**

![image](https://github.com/TonnyG95/iptv/assets/47572512/28e7b7c6-c6b0-4db4-9764-d0fa85cd0926)


### Upravljanje Korisnicima

Kao što sam gore naveo, admin može upravljati korisnicima. Aplikacija će automatski kreirati "User Profile" kad se korisnik registrira na stranicu i sve vezano za korisnika se nalazi u **User Profiles**.

![image](https://github.com/TonnyG95/iptv/assets/47572512/7cf07988-d9cb-41ee-9171-cca836e1999f)

Kao što se vidi na screenshotu, u admin panelu postoji i **Users** u vrhu izbornika. Ta sekcija dashboarda je samo za upravljanje glavnim podacima korisnika kao što su e-mail i lozinka, ime i prezime korisnika. Isto tako, također tamo se mogu pronaći i postavke **Permissions** gdje se korisniku mogu dodijeliti određene dozvole, dodavati statuse kao što su **Staff** ili **Admin**. Ali osim toga, u toj sekciji se neće ništa raditi vezano za upravljanje klijentima i pretplatama, ali isto je bitno napomenuti ukoliko admin želi dodati još admina ili svoje resellere ili kombinaciju svega može to brzo i jednostavno odraditi u toj sekciji, ukratko kreativnost admina je jedina limitacija ove aplikacije i to su sve opcije koje su moguće samo zbog odabira Djanga kao glavnog frameworka za ovu aplikaciju.

![Screenshot_2024-03-03_21-38-51](https://github.com/TonnyG95/iptv/assets/47572512/13985748-23e2-4109-bc98-76ef459b3744)

### Upravljanje Novčanicima

Nakon što se korisnik registrira na aplikaciju, njemu će automatski biti kreiran i dodijeljen novčanik koji će on koristiti da uplati sredstva na svoj račun i to će se sve raditi kroz PayPal API tako da će adminu odmah biti uplaćen iznos koji je korisnik uplatio. Naravno, pošto ova aplikacija ima samo integraciju s PayPal-om, ja nisam želio da admina ograničim samo na korištenje PayPal-a, tako da imamo opciju da admin može ručno promijeniti stanje novčanika za svakog korisnika. Tako da, ukoliko korisnik plati admina u gotovini, Revolut, bankovnim transferom ili bilo kojim drugim načinom plaćanja, admin će moći ažurirati iznos korisnikovog novčanika u par minuta i sredstva će korisniku biti ažurirana odmah.

**Lista Novčanika**

![image](https://github.com/TonnyG95/iptv/assets/47572512/be56cc5c-819d-4e62-8173-83067de51dda)

**Upravljanje Odabranim Novčanikom**

![image](https://github.com/TonnyG95/iptv/assets/47572512/e4f71a1c-d3c3-46dc-a4c1-cc2dc00ba7fb)

## Obavijesti

Kao i svaka aplikacija, admin mora imati mogućnost da kreira obavijest koja će biti prikazana svim korisnicima aplikacije. Ja sam ovdje to odlučio napraviti kao **Announcements** funkciju koja će biti prikazana svim korisnicima direktno na početnoj stranici aplikacije, kao što se može vidjeti na screenshotu. Za svaku obavijest imamo opciju da dodamo početni datum prikazivanja obavjesti isto tako admin ima opciju da odabere do kojeg datuma će se ta obavjesti prikazivati, i po isteku obavijest će se automatski prestati prikazivati korisnicima.

**Admin -> Announcements**

![image](https://github.com/TonnyG95/iptv/assets/47572512/9687c736-9521-4d4e-9401-a77f531eb87b)

**Dashboard -> Početna**

![image](https://github.com/TonnyG95/iptv/assets/47572512/ac6c1782-4aa3-4d11-9169-53cd4d58f559)

## Planovi Za Aplikaciju

Kao što sam spomenuo, ova aplikacija je otkazana jer se kolegi platforma nije svidjela, tako da **ova aplikacija je u stanju kakvom je. Ako bude interesa, možda ću odraditi još koji update za aplikaciju, ali razvoj ove aplikacije je završen prije više od godinu dana i ostala je u ovom stanju**. Iako smo planirali odraditi i frontend sa **ReactJS-u** i **Django Rest Frameworku**, nažalost to se neće desiti. Ja sam na ovoj aplikaciji krenuo raditi API tako da **postoji već kod za API** koji se već može koristiti, ali je daleko od završenog. Ako se dobro sjećam, samo je napravljen API endpoint za registraciju i prijavu, ali nisam siguran pošto je prošlo preko godinu i pol dana, ako ne i 2 godine, otkako sam zadnji put radio na ovoj aplikaciji. Daljnji planovi su bili integrirati i 2FA (Two-factor authentication) i bio je u planu da se odradi kompletan dark mode, ali nažalost pošto je on odustao od ove aplikacije i to u relativno ranoj verziji, ovo što možete vidjeti je sve što je implementirano, i ovo je odrađeno kroz tjedan dana.

## Cron Jobs

**Što je Cron Job?**

Cron Jobs su zapravo zadaci zakazani da se automatski izvode u predodređeno vrijeme. Ovaj mehanizam omogućava Linux i Unix operacijskim sustavima da izvode skripte ili komande u redovitim intervalima. Konfiguracija Cron Job-a odvija se kroz datoteku poznatu kao "crontab", gdje se definira vrijeme izvršenja tako da možeš specificirati u kojem trenutku želiš da se zadatak izvrši, bilo to svakih nekoliko minuta, sati, dana, tjedana ili mjeseci.

**Zašto ova aplikacija koristi Cron Jobs?**

- **Automatizacija**: Umjesto da ručno provjeravaš svakog korisnika i status njegove usluge, Cron Jobs može automatski obaviti ovaj posao. To štedi vrijeme i smanjuje mogućnost greške.
- **Redovito praćenje**: Postavljanjem Cron Jobs-a da redovito provjeravaju trajanje usluge, osiguravaš da nijedan korisnik neće biti zanemaren. Možeš postaviti da se zadatak izvršava svakog dana u ponoć, što će omogućiti aplikaciji da zna kada kojem korisniku istječe usluga.
- **Pravovremene obavijesti**: Kada Cron Job otkrije da je usluga nekog korisnika na izmaku ili je već istekla, može automatski poslati obavijest korisniku i/ili administratoru. To omogućava poduzimanje odgovarajućih mjera, poput obnove usluge.
- **Održavanje kvalitete usluge**: Redovitim i automatiziranim nadzorom usluga, možeš osigurati visoku razinu zadovoljstva korisnika i održati integritet aplikacije ili sustava.

## Deployment na AWS

Kao što sam napisao, ova je aplikacija od starta planirana da se deploya na AWS, tako da ću vam ovdje napisati kako to uraditi i naravno ostaviti vam tango tutorijale ispod da vam olakšam ovaj postupak dodatno. Naravno, podrazumijeva se da već imate AWS račun ili ako ga nemate, kreirajte ga besplatno, jer bez AWS računa ne možete ništa. Naravno, ova aplikacija se može deployati na Vercel, PythonAnywhere ili Netlify, ali za druge platforme potrebne su neke izmjene, dok je za AWS sve spremno i super jednostavno za deployati zato što je aplikacija dobro pripremljena za AWS. Potrebne usluge za deployment ove aplikacije su Elastic Beanstalk i S3. E sad, ova aplikacija ima i Cron Jobs tako da možete i to napraviti u AWS-u, ali to već postaje malo kompliciranije. Ali računao sam ja i na to, tako da sam napravio i workaround za to da bude super jednostavno za bilo koga tko bude koristio ovu aplikaciju.

## Cron Jobs Workaround

Kao što sam napisao iznad, ova aplikacija zahtijeva korištenje Cron Jobs kako bi automatski obavljala neke poslove, kao što su praćenje isteka pretplata korisnika, obavještavanje korisnika i admina o isteku ili gašenju usluge. Da bi ta funkcija radila, potrebno je imati funkciju koja će pokrenuti provjeru svih korisnika i njihovih pretplata svaki dan ili svakih sat vremena. Ja sam našao da je najbolji balans da se ta funkcija pokreće svakih sat vremena tako da se kroz dan ta funkcija pokrene 24 puta i da pronađe sve korisnike kojima ističe ili je već istekla pretplata.

**Kako je ova funkcija napravljena?**

Da bi napravio da ovo bude što jednostavnije za koristiti i da admin ima opciju da manualno pokrene tu funkciju, ja sam napravio URL koji kad se pozove pokrene funkciju koja će provjeriti svakog korisnika i njegovu pretplatu. URL za tu funkciju je **/provjera-preplata** npr. ***www.tvoja-domena.com/provjera-preplata/*** i ako je operacija uspjela dobit ćeš odgovor "Provjera obavljena".

![image](https://github.com/TonnyG95/iptv/assets/47572512/b3c8a964-5898-4635-938c-6004863c018e)

### Kreiranje Cron Job-a

Kao što sam spomenuo, za pokretanje funkcije za provjeru pretplata korisnika potrebno je kreirati Cron Job. Taj Cron Job treba se pokretati svakih sat vremena i slati zahtjev na URL /provjera-preplata/. Odlučio sam koristiti web stranicu [EasyCron](https://www.easycron.com/) koja će svakih sat vremena poslati zahtjev na navedeni URL, čime će se automatski pokrenuti funkcija koja provjerava status pretplate svakog korisnika.

Tutorial možete pronaći -> [Ovdje](https://app.tango.us/app/workflow/Setting-up-Cron-Jobs-with-EasyCron-6c832942485d4919bc08ec8f6e1c9fd9)

### Kreiranje Elastic Beanstalk aplikacije

**Što je AWS Elastic Beanstalk?**

AWS Elastic Beanstalk je PaaS (Platform as a Service) usluga koju nudi Amazon Web Services, dizajnirana da olakša deployment i skaliranje web aplikacija i servisa razvijenih u Java, .NET, PHP, Node.js, Python, Ruby, Go, i Docker na poznate web servere kao što su Apache, Nginx, Passenger, i IIS.

Korištenjem AWS Elastic Beanstalk-a, developeri mogu jednostavno i brzo implementirati i upravljati aplikacijama u AWS-u bez potrebe za detaljnim razumijevanjem infrastrukture koja stoji iza toga. Elastic Beanstalk automatski rukuje detaljima implementacije, od kapaciteta provisioninga, balansiranja opterećenja, auto-scalinga, do monitoringa zdravlja aplikacije.

**Zašto Elastic Beanstalk za ovu aplikaciju?**

Odlučio sam koristiti AWS Elastic Beanstalk za ovu Django aplikaciju iz nekoliko ključnih razloga:

- **Brz i jednostavan deployment**: Elastic Beanstalk omogućava brz deployment aplikacije, automatski upravljajući infrastrukturom bez potrebe za ručnim konfiguriranjem servera.
- **Automatsko skaliranje**: Mogućnost automatskog skaliranja Elastic Beanstalk-a osigurava da aplikacija uvijek ima potrebne resurse, bez nepotrebnog troška za resurse koji trenutno nisu u upotrebi.
- **Integracija s AWS servisima**: Elastic Beanstalk se lako integrira s drugim AWS servisima poput Amazon RDS (za baze podataka) i Amazon S3 (za pohranu statičkih datoteka), što pruža dodatnu fleksibilnost i snagu aplikaciji.
- **Upravljanje verzijama i deployment proces**: Elastic Beanstalk podržava upravljanje verzijama aplikacije, omogućavajući jednostavno ažuriranje i vraćanje na prethodne verzije ako je potrebno.

**Optimizacija aplikacije za Elastic Beanstalk i S3**

Aplikacija je od samog početka optimizirana za deployment na AWS Elastic Beanstalk, uzimajući u obzir najbolje prakse za skaliranje, sigurnost i performanse. Također, aplikacija koristi Amazon S3 za pohranu statičkih i medija datoteka, osiguravajući brz i efikasan pristup resursima bez obzira na opterećenje aplikacije.

Tutorial možete pronaći -> [Ovdje](https://app.tango.us/app/workflow/Creating-an-Elastic-Beanstalk-application-for-IPTV-Demo-4c39bb585dab4a0f812efcf571501bb7)

### Kreiranje S3 Bucketa

Da bi ova aplikacija radila, potrebno je kreirati S3 bucketa u kojem će se nalaziti statične datoteke kao što su slike, JavaScript i CSS datoteke.

**Zašto je S3 obavezan da bi ova aplikacija radila?**

Nažalost, Django sam po sebi ne radi sa statičnim datotekama kao što su CSS, JavaScript i slike u produkciji, tako da je potreban workaround da bi Django u produkciji učitavao statične datoteke. Kad kažem na produkciju, mislim na to da je **DEBUG mode uključen** odnosno postavljen kao True ili 1, ako radimo u development verziji, tad će Django bez problema učitavati statične fajlove, no čim se DEBUG postavi na False ili 0, odnosno čim Django zna da je aplikacija live i da korisnici mogu koristiti aplikaciju, on tad više neće učitavati statične datoteke. Ne znam zašto je tako, ali nažalost tako je. Naravno, postoje Django paketi kao što su Whitenoise koji će omogućiti Djangu da učita statične datoteke u produkciji, ali to može biti komplicirano za postaviti, tako da sam ja odlučio koristiti S3 za statične datoteke da izbjegnem potencijalne probleme i da olakšam proces deploymenta za sebe i za sve koji odluče koristiti ovu aplikaciju. Osim što će to izbjeći moguće probleme sa statičnim datotekama, korištenje S3 za statične datoteke ujedno će znatno ubrzati rad aplikacije, što je bitno za SEO i iskustvo koje će admini i korisnici imati dok koriste aplikaciju.

Tutorial možete pronaći -> [Ovdje](https://app.tango.us/app/workflow/Setting-Up-S3-Bucket-Permissions-for-Public-Access-1d0d72b1a3254262971e9da0ec3a589e)

## Code Potreban Za S3 Bucket

Amazon S3 -> BucketName -> Permissions

**Bucket policy**

```
{
    "Version": "2012-10-17",
    "Id": "Policy1650556415415",
    "Statement": [
        {
            "Sid": "Stmt1650556411764",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::ime-bucketa/*"
        }
    ]
}


```

**Cross-origin resource sharing (CORS)**

```
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "PUT",
            "GET",
            "POST",
            "DELETE"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    },
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "PUT",
            "GET",
            "POST",
            "DELETE"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    },
    {
        "AllowedHeaders": [],
        "AllowedMethods": [
            "GET"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    }
]
```

## Kako Pokrenuti Aplikaciju Lokalno?

Da biste ovu aplikaciju pokrenuli lokalno, prvo je potrebno da imate instaliran Python i VSCode ili bilo koji drugi IDE. Ja preferiram VSCode. Prije nego što aplikaciju pokrenete lokalno, **pobrinite se da prvo kreirate S3 bucket** jer će to biti neophodno za učitavanje statičkih datoteka aplikacije. Također, **pobrinite se da ste `example.env.py` preimenovali u `env.py`** i da ste ažurirali vrijednosti unutar `env.py` datoteke, jer bez toga aplikacija neće raditi. Ovo **isto morate uraditi prije nego što deployujete aplikaciju na Elastic Beanstalk**.

Nakon toga, možete desnim klikom na folder gdje se nalazi aplikacija odabrati "Open With Code" (u slučaju korištenja VSCode-a). Kada otvorite aplikaciju u code editoru, otvorite terminal. VSCode ima ugrađeni terminal, stoga možete jednostavno otići u gornji navigacijski bar gdje se nalaze opcije kao što su File, Edit, itd., pronaći opciju "Terminal", i kliknuti na "New Terminal". Zatim, u terminalu unesite sljedeće komande, jednu po jednu:

```
pip install -r requirements.txt
```

Ova komanda instalira sve potrebne pakete da bi aplikacija radila.

```
Python manage.py collectstatic 
```
Ova funkcija će kopirati sve statične datoteke iz aplikacije na vaš S3 Bucket.

```
Python manage.py startserver 
```

Ova komanda će pokrenuti lokalni server i nakon toga aplikacija će raditi na linku http://127.0.0.1:8000/.

Ukoliko koristite macOS kao svoj operativni sustav, da bi ove komande iznad radile na macOS-u, morate koristiti python3 umjesto python, tako da komande koje će macOS korisnici morati upisati su:

```
pip install -r requirements.txt
python3 manage.py collectstatic
python3 manage.py runserver
```

## Podatci za prijavu

Kao što sam napisao ova aplikacija koristi lokalnu bazu podataka tako da možete koristiti ove podatke za prijavu čak i nakon deploymenta na AWS. 

Podatci za prijavu na Admina su:

```
Admin URL: /admin primjer www.tvoja-domena.com/admin

UserName: iptvadmin
Password: Admin

```

Podatci za prijavu na Demo Korisnika su: 

```
Login URL: /login primjer www.tvoja-domena.com/login

UserName: demo@klijent.com
Password: KlijenUser!

```


## Zaključak

Ovo je Django aplikacija koju sam ja radio za kolegu kojem se na kraju aplikacija nije svidjela, tako da sam stao s razvojem ove aplikacije. Ovo što vidite ovdje je odrađeno kroz nekih tjedan dana. Što se tiče glavne funkcionalnosti, ova aplikacija je spremna za korištenje i nakon svih testiranja ja osobno nisam našao ni jedan bug koji je preostao, tako da ovo bi trebala biti bug-free aplikacija sa puno legacy koda koji je tu ostao zbog pripreme za nove funkcije aplikacije, sve u svemu ova je sprmna aplikacija za depolyment koja se može jednostavno i brzo deployati na AWS Elastic Beanstalk. Prije deploymenta potrebno je preimenovati datoteke example.env.py u env.py i da se napravi novi S3 bucket kako bi se aplikacija mogla učitati statične datoteke za aplikaciju. Ja osobno više neću raditi na ovoj aplikaciji, ali ovo je odlična početna točka za nekog Django developera koji želi nastaviti raditi na ovoj aplikaciji, bilo to za edukativne svrhe ili komercijalne. Isto tako, ovo je dobra solucija za end-usera koji želi dashboard koji je automatiziran za svoju IPTV uslugu besplatno, jedino što će se morati malo potruditi da aplikaciju deploya na AWS i trebat će se malo poigrati s integracijama kao što su SMTP, Google reCAPTCHA i PayPal. Ukoliko bude interesa za ovu aplikaciju, lako ja odradim još koji update s nekim sitnim izmjenama, ali veliki updateovi kao što su završavanje API-a da se može integrirati s nekim frontend JavaScript frameworkom sigurno neću raditi. Ali puno je Python i Django developera ovdje pa ako netko bude htio odraditi, može klonirati ovaj repository i nastaviti raditi. I ako se netko odluči na taj korak, bilo bi mi drago da mi se javi i da mi javi što je novo napravljeno ili popravljeno na ovoj aplikaciji, jer aplikacija je stvarno dobra početna točka da se napravi nešto veće od nje. Eto, toliko od mene. LP