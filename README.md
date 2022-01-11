# Web information system of a logistics company based on Python-Flask framework
## Technologie & moduly

- Python (Flask framework) + MySQL (viz soubor requirements.txt)
    - modul Alembic na správu migrací databáze
    - modul SQLAlchemy na vytváření databázových modelů
    - modul FlaskWTForms na jednoduché vytváření formulářů
    - a další

## Architektura aplikace

#### Princip

- zcela opouštíme soubor routes.py. Zatím jsem tam původní funkce nechal pro překopírování jejich částí, ale používat je nebudeme. Modul se nakonec smaže.
- každý modul systému (zaměstnanci, vozidla, dovolená, moje dovolená....) <b>má svůj vlastní view soubor</b>
- ve <i>webapp/views/--init--.py</i> je funkce configure_views(), která tyto views "registruje" do aplikace
    - tedy přidáme-li nové view, je potřeba ho přidat do těla této funkce a o více se netřeba starat
    - samotná funkce configure_views() je volaná při inicializaci aplikace - funkce create_app() (viz webapp/--init--.py)

#### View moduly a jejich struktura

- view modul obsahuje vždy všechno, co se týká dané entity (související formuláře a potřebné třídy - viz dále)
- každá akce (přidat, smazat, upravit....) související s modulem má vlastní třídu (viz webapp/views/cars.py), přičemž <b>všechny tyto "view" třídy jsou potomkem třídy MethodView</b>
    - v každé takové třídě máme dostupné metody <i>get</i> a <i>post</i>, které stačí naimplementovat - s úplně stejnou logikou jako např <i>@app.route('/auth/<entity>/new',methods=['GET','POST'])</i> v routes.py 
- chceme-li metodu zpřístupnit jen uživateli s určitou rolí, stačí aplikovat dekorátor <i>@management</i> nebo <i>@employee</i>. Role budeme mít jen tyto dvě, zatím je tam i admin, ale toho odstraníme, abychom si to nekomplikovali zbytečně.
- součástí každého takto vytvořeného view je funkce configure(app), která po zavolání z hlavního registrátoru views toto view pojmenovává a nastavuje příslušné adresy

## Funkcionality & popis částí systému

- **Nástěnka**
    - role *vedoucí & admin & finance*:
        - přehled aktivit (denních činností zaměstnanců) ke schválení
        - přehled dovolených ke schválení (žádostí odeslaných zaměstnanci)
        - přehled upozornění (zobrazování brzo expirujících lékařských prohlídek, ale i dokumentů k vozidlům a jiných....)
    - role *zaměstnanec*:
        - přehled posledních odeslaných aktivit/jízd ke schválení
        - přehled vyčerpané / schválené / zbývající dovolené na současný rok
        - upozornění na vypršení platnosti školení řidičů a lékařské prohlídky
- **Evidence činností**
    - role *vedoucí & admin & finance*:
        - **Přehled aktivit**
            - přehled všech aktivit zaměstnanců seřazený podle data (a následně případně podle zaměstnanců) - obsahuje: zaměstnanec, popis, typ činnosti
            - vizuální odlišení schválených / neschválených aktivit a možnost schválení aktivity přímo na tomto přehledu
        - **Docházka**
            - kalendáře aktivit všech zaměstnanců (pro každého zaměstnance zvláštní kalendář) - tedy nahlásil-li zaměstnanec aktivitu na daný den, v tomto kalendáři bude mít pro daný den záznam
   - role *zaměstnanec*:
        - **Přehled aktivit**
            - možnost přidat novou aktivitu (přímo na stránce s přehledem)   
            - přehled všech aktivit daného zaměstnance - odeslaných, schválených i "zamítnutých" (tyto nutno upravit a odeslat k novému schválení, případně smazat)
        - **Docházka**
            - kalendář daného zaměstnance (stejná logika jako kalendář u vedoucího...)      
- **Zaměstnanci** (pouze pro roli *vedoucí*, *finance* a *admin*)
    - **Přehled zaměstnanců**
        - výpis všech zaměstnanců a jejich údajů - jméno, příjmení, dat.nar., trv.bydliště, přech.bydliště, telefon, e-mail.....
    - **Lékařské prohlídky**
        - výpis lékařských prohlídek seřazených od prohlídky, která vyprší nejdřív - jméno, příjmení, datum absolvování poslední prohlídky, platnost
    - **Pracovní smlouvy**
        - výpis pracovních smluv zaměstnanců - jméno, příjmení, typ
    - **Dovolená**
        - tabulka s přehledem dovolené všech zaměstnanců - jméno, příjmení, celkové dny dovolené, vyčerpané, schválené, zbývající...
    - **Úložiště dokumentů**
        - TBD
- **Zaměstnanec** (pouze pro roli *zaměstnanec*) - všechno na jedné stránce
    - Osobní údaje
        - výpis osobních údajů zaměstnance (viz přehled zaměstnanců u role vedoucí...) s možností cokoli upravit
    - Stav dovolené
        - vyčerpáno, schváleno, požádáno, zbývá....
    - Aktuální lékařská prohlídka 
        - kdy absolvována, do kdy platí
    - Platnost školení řidičů
        - kdy absolvováno, do kdy platí

- **Vozový park** (pouze pro roli *vedoucí*, *finance* a *admin*)
    - **Přehled vozidel**
        - výpis všech vozidel a jejich údajů (viz ERD, tabulka Vozidlo)
        - možnost přidat, upravit a smazat vozidlo
    - **Technické kontroly**
        - přehled všech provedených technických kontrol počínaje od kontroly, která nejdříve vyprší
        - možnost přidat, upravit a smazat technickou kontrolu
    - **Plánované servisní práce**
        - TBD
    - **Úložiště dokumentů**
        - TBD
- **Správa uživatelů** (pouze pro roli *vedoucí*, *finance* a *admin*)
    - přehled všech registrovaných uživatelů (login, e-mail, počet přihlášení, poslední přihlášení, čas poslední změny uživatele...) s možností měnit jejich role
    - možnost odstranit uživatele
