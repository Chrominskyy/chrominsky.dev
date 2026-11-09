#!/usr/bin/env python3
"""Generate pl/index.html from index.html.

Every pair below must match exactly once (or the stated count) in index.html,
so the build fails loudly when the English source changes and a translation
falls out of date. Run from the repository root:

    python3 scripts/build_pl.py
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
OUT = ROOT / "pl" / "index.html"

# (english, polish[, expected count])
PAIRS = [
    # ---- head
    ('<html lang="en">', '<html lang="pl">'),
    ('<title>Bartosz Chrominski | Senior .NET engineer</title>',
     '<title>Bartosz Chrominski | Senior .NET engineer, backend i aplikacje Apple</title>'),
    ('<meta property="og:title" content="Bartosz Chrominski | Senior .NET engineer">',
     '<meta property="og:title" content="Bartosz Chrominski | Senior .NET engineer, backend i aplikacje Apple">'),
    ('content="Bartosz Chrominski (Chrominsky), senior C# and .NET engineer: event-driven AWS services and native Apple apps DevPulse, Mighty Markdown, CloudLatch, TapVault."',
     'content="Bartosz Chrominski (Chrominsky), senior C# i .NET engineer: serwisy event-driven na AWS i aplikacje Apple DevPulse, Mighty Markdown, CloudLatch, TapVault."'),
    ('<meta property="og:description" content="Backend in C#. Apps in Swift. Built to be trusted. Event-driven .NET on AWS, plus native apps for macOS, iPhone and iPad.">',
     '<meta property="og:description" content="Backend w C#. Aplikacje w Swift. Zbudowane, by im ufać. Event-driven .NET na AWS i natywne aplikacje na macOS, iPhone i iPad.">'),
    ('<meta property="og:url" content="https://chrominsky.dev/">', '<meta property="og:url" content="https://chrominsky.dev/pl/">'),
    ('<meta property="og:locale" content="en_GB">\n<meta property="og:locale:alternate" content="pl_PL">',
     '<meta property="og:locale" content="pl_PL">\n<meta property="og:locale:alternate" content="en_GB">'),
    ('<meta property="og:image:alt" content="Bartosz Chrominski. Backend in C#. Apps in Swift. Built to be trusted.">',
     '<meta property="og:image:alt" content="Bartosz Chrominski. Backend w C#. Aplikacje w Swift. Zbudowane, by im ufać.">'),
    ('<link rel="canonical" href="https://chrominsky.dev/">', '<link rel="canonical" href="https://chrominsky.dev/pl/">'),
    ('href="assets/', 'href="../assets/', None),
    ('src="assets/', 'src="../assets/', None),
    ('srcset="assets/', 'srcset="../assets/', None),
    (' 480w, assets/', ' 480w, ../assets/', None),
    (' 760w, assets/', ' 760w, ../assets/', None),

    # ---- header
    ('<a class="skip" href="#main">Skip to content</a>', '<a class="skip" href="#main">Przejdź do treści</a>'),
    ('aria-label="Chrominsky, home"', 'aria-label="Chrominsky, strona główna"'),
    ('<nav class="links" aria-label="Sections">', '<nav class="links" aria-label="Sekcje">'),
    ('<span>01</span> Apps</a>', '<span>01</span> Aplikacje</a>'),
    ('<span>03</span> Principles</a>', '<span>03</span> Zasady</a>'),
    ('<span>05</span> Contact</a>', '<span>05</span> Kontakt</a>'),
    ('<a class="lang" href="pl/" hreflang="pl" lang="pl" aria-label="Wersja polska">PL</a>',
     '<a class="lang" href="../" hreflang="en" lang="en" aria-label="English version">EN</a>'),
    ('aria-label="Toggle color theme"', 'aria-label="Przełącz motyw kolorów"'),

    # ---- hero
    ('Bartosz Chrominski · Senior .NET engineer · Poland', 'Bartosz Chrominski · Senior .NET engineer · Polska'),
    ('Backend in C#. Apps in Swift. <i>Built to be trusted.</i>', 'Backend w C#. Aplikacje w Swift. <i>Zbudowane, by im ufać.</i>'),
    ('Senior .NET engineer. By day I build event-driven services on AWS (DynamoDB, Step Functions, EventBridge, Pulumi), track production defects down to a proven root cause, and ship test-first fixes. After hours I build focused native apps for macOS, iPhone and iPad, each one doing a single job and claiming only what it can actually do.',
     'Senior .NET engineer. Na co dzień buduję serwisy event-driven na AWS (DynamoDB, Step Functions, EventBridge, Pulumi), szukam przyczyn defektów produkcyjnych aż do udowodnionego źródła i dostarczam poprawki zaczynając od testu. Po godzinach tworzę natywne aplikacje na macOS, iPhone i iPad: każda robi jedną rzecz i obiecuje tylko to, co naprawdę potrafi.'),
    ('See the apps\n', 'Zobacz aplikacje\n'),
    ('aria-label="Career timeline shown as a pipeline run"', 'aria-label="Przebieg kariery pokazany jako uruchomienie pipeline\'u"'),
    ('<span class="badge dev">running</span></div>', '<span class="badge dev">w toku</span></div>'),
    ('Foundations in C#<small>desktop tools, first services</small>', 'Fundamenty w C#<small>narzędzia desktopowe, pierwsze serwisy</small>'),
    ('.NET 8 backends<small>clean architecture, Redis, Docker</small>', 'Backendy w .NET 8<small>clean architecture, Redis, Docker</small>'),
    ('Chrominsky.Utils on NuGet', 'Chrominsky.Utils w NuGet'),
    ('<span class="time">day job</span>', '<span class="time">praca</span>'),
    ('Native Apple apps<small>SwiftUI, WidgetKit, iCloud</small>', 'Natywne aplikacje Apple<small>SwiftUI, WidgetKit, iCloud</small>'),
    ('App Store release<small>2 of 4 apps live on the Mac App Store</small></span><span class="time">now</span>', 'Premiera w App Store<small>2 z 4 aplikacji w Mac App Store</small></span><span class="time">teraz</span>'),
    ('<span>4 apps · 4 .NET repos public</span><span>view: <code>ascii</code></span>',
     '<span>4 aplikacje · 4 publiczne repo .NET</span><span>widok: <code>ascii</code></span>'),

    # ---- apps
    ('01 / Now building', '01 / W budowie'),
    ('Four apps,<br><i>one job each.</i>', 'Cztery aplikacje,<br><i>każda do jednego.</i>'),
    ('Native utilities for macOS, iOS and iPadOS. Each comes with a public website, a support guide and a privacy policy, and each one states its availability honestly. DevPulse and Mighty Markdown are on the Mac App Store worldwide. The rest say exactly how far along they are.',
     'Natywne narzędzia na macOS, iOS i iPadOS. Każde ma publiczną stronę, poradnik i politykę prywatności, i każde uczciwie podaje swój status. DevPulse i Mighty Markdown są już w Mac App Store na całym świecie. Pozostałe mówią dokładnie, na jakim są etapie.'),
    ('alt="DevPulse pipeline run view with stages, jobs and tasks"', 'alt="DevPulse: widok uruchomienia pipeline\'u z etapami, jobami i zadaniami"'),
    ('Azure DevOps, out of the browser. Follow pipeline runs, read stage logs and work through boards in a native app.',
     'Azure DevOps poza przeglądarką. Śledź uruchomienia pipeline\'ów, czytaj logi etapów i pracuj na tablicach w natywnej aplikacji.'),
    ("Draws each run as stages, jobs and tasks in the order of that run's compiled YAML, as cards or as an ASCII graph.",
     'Rysuje każde uruchomienie jako etapy, joby i zadania w kolejności ze skompilowanego YAML tego uruchomienia: jako karty albo graf ASCII.'),
    ("A real work item editor: every save checks the baseline revision, so it can't silently overwrite a colleague's change.",
     'Prawdziwy edytor work itemów: każdy zapis sprawdza rewizję bazową, więc nie nadpisze po cichu zmiany kolegi.'),
    ('Desktop widgets for pinned runs. Sign in with Microsoft Entra ID or a personal access token.',
     'Widgety na pulpit dla przypiętych uruchomień. Logowanie przez Microsoft Entra ID albo personal access token.'),
    ('aria-label="Technologies"', 'aria-label="Technologie"', 4),
    ('<span class="badge dev">in development</span>', '<span class="badge dev">w trakcie rozwoju</span>'),
    ('<span class="badge live">on the Mac App Store</span>', '<span class="badge live">w Mac App Store</span>', 2),
    ('>Website ↗</a>', '>Strona ↗</a>', 4),
    ('alt="Mighty Markdown in Split mode, Markdown source beside the rendered preview"', 'alt="Mighty Markdown w trybie Split: źródło Markdown obok podglądu"'),
    ('A native place to read, write and move around Markdown files.', 'Natywne miejsce do czytania, pisania i poruszania się po plikach Markdown.'),
    ('Read, Edit and Split modes, with source and preview kept on the same part of the document.',
     'Tryby Read, Edit i Split, w których źródło i podgląd pokazują ten sam fragment dokumentu.'),
    ('A filterable heading outline and a draggable minimap for long files.', 'Filtrowany spis nagłówków i przeciągana minimapa dla długich plików.'),
    ('Your files stay ordinary .md files. No account, analytics or advertising.', 'Twoje pliki pozostają zwykłymi plikami .md. Bez konta, analityki i reklam.'),
    ('alt="CloudLatch artwork: a brushed metal cloud with a green latch"', 'alt="Grafika CloudLatch: chmura ze szczotkowanego metalu z zielonym zatrzaskiem"'),
    ('<div class="platform">macOS menu bar</div>', '<div class="platform">pasek menu macOS</div>'),
    ('AWS MFA sessions and IAM role switching from the menu bar.', 'Sesje AWS MFA i przełączanie ról IAM z paska menu.'),
    ('Assume a configured role with MFA, see when the role session expires, and get it renewed five minutes before it does.',
     'Przyjmij skonfigurowaną rolę z MFA, zobacz, kiedy wygasa sesja roli, i pozwól odnowić ją pięć minut wcześniej.'),
    ("Uses the AWS SDK for Swift in-process, so the AWS CLI isn't needed.", 'Korzysta z AWS SDK for Swift wewnątrz aplikacji, więc AWS CLI nie jest potrzebne.'),
    ('You choose which directory it can touch. Temporary source sessions are kept in the macOS Keychain.',
     'Ty decydujesz, do którego katalogu ma dostęp. Tymczasowe sesje źródłowe trzyma w pęku kluczy macOS.'),
    ('<span class="badge dev">preparing for App Store</span>', '<span class="badge dev">przygotowanie do App Store</span>'),
    ('alt="TapVault artwork: a glowing NFC symbol with orbit rings"', 'alt="Grafika TapVault: świecący symbol NFC z orbitami"'),
    ('Read, save and write compatible NFC tags, with a library synced across your devices.', 'Odczytuj, zapisuj i programuj zgodne tagi NFC, z biblioteką synchronizowaną między urządzeniami.'),
    ('Shows NDEF records, tag technology, capacity and write access on a compatible iPhone.', 'Pokazuje rekordy NDEF, technologię tagu, pojemność i możliwość zapisu na zgodnym iPhonie.'),
    ('Create links, text and vCard contacts. It asks before writing a tag, then reads it back to confirm the write worked.',
     'Twórz linki, tekst i kontakty vCard. Przed zapisem tagu pyta o potwierdzenie, a potem odczytuje go, by sprawdzić, czy zapis się udał.'),
    ('SwiftData library with private iCloud sync. Interface in Polish and English.', 'Biblioteka w SwiftData z prywatną synchronizacją iCloud. Interfejs po polsku i angielsku.'),

    # ---- .NET
    ('02 / Server side', '02 / Po stronie serwera'),
    ('Built on<br><i>.NET 8.</i>', 'Zbudowane na<br><i>.NET 8.</i>'),
    ('C# is where I started and where I still do most of my work. At my day job that means event-sourced domain services on AWS: DynamoDB key and GSI design, events published against expected versions, Step Functions orchestration, and table migrations run behind feature flags with dual projection and a planned cutover. In public, it means the libraries and reference APIs below.',
     'Od C# zaczynałem i w nim wciąż robię większość pracy. W pracy etatowej to serwisy domenowe z event sourcingiem na AWS: projektowanie kluczy i GSI w DynamoDB, zdarzenia publikowane z oczekiwaną wersją, orkiestracja w Step Functions i migracje tabel za feature flagami, z podwójną projekcją i zaplanowanym przełączeniem. Publicznie: biblioteki i referencyjne API poniżej.'),
    ('By day · production engineering on a multi-repo AWS platform', 'Na co dzień · praca produkcyjna na wielorepozytoryjnej platformie AWS'),
    ('<h3>Root cause, proven</h3>', '<h3>Przyczyna, udowodniona</h3>'),
    ("Defects get traced through HAR files, CloudWatch logs and production data until the cause is proven. More than once that showed the ticket's original theory was wrong, so the real cause got fixed instead of a symptom.",
     'Defekty śledzę w plikach HAR, logach CloudWatch i danych produkcyjnych, aż przyczyna jest udowodniona. Nieraz okazało się, że pierwotna teza zgłoszenia była błędna, więc naprawiona została prawdziwa przyczyna, a nie objaw.'),
    ('<h3>Test-first, verified live</h3>', '<h3>Najpierw test, potem weryfikacja na żywo</h3>'),
    ('A failing test first, then the fix, self-review, PR and review comments. Done means confirmed on dev and stable through Step Function executions, DynamoDB state and latency checks, not just a green CI run.',
     'Najpierw czerwony test, potem poprawka, samodzielny review, PR i uwagi z review. Gotowe znaczy potwierdzone na dev i stable przez wykonania Step Functions, stan DynamoDB i pomiary opóźnień, a nie tylko zielone CI.'),
    ('<h3>Flags &amp; migrations</h3>', '<h3>Flagi i migracje</h3>'),
    ('New behaviour ships behind AppConfig feature flags, with the code and config PRs kept separate. Reactors move to new projections, and tenant data migrates from written plans with a handover.',
     'Nowe zachowanie trafia na produkcję za feature flagami w AppConfig, z osobnymi PR-ami na kod i konfigurację. Reaktory przechodzą na nowe projekcje, a dane tenantów migrują według spisanych planów z przekazaniem.'),
    ('<h3>On-call &amp; RCAs</h3>', '<h3>Dyżury i RCA</h3>'),
    ('Incident triage across production regions: alarms, logs, queue redrives and follow-up tickets. Each incident closes with a short, client-ready RCA covering symptom, root cause, fix and status.',
     'Triage incydentów w regionach produkcyjnych: alarmy, logi, redrive kolejek i zgłoszenia następcze. Każdy incydent zamyka krótkie RCA gotowe dla klienta: objaw, przyczyna, poprawka, status.'),
    ('A fleet API split into Domain, Application, Infrastructure and API layers. Versioned CRUD endpoints with filtered, sorted search and tests.',
     'API floty podzielone na warstwy Domain, Application, Infrastructure i API. Wersjonowane endpointy CRUD z filtrowanym i sortowanym wyszukiwaniem oraz testami.'),
    ('A base repository with automatic object versioning, soft delete, filtered search and pagination for SQL Server and PostgreSQL. Also includes a Redis cache with fallback, BCrypt hashing and an SMTP sender.',
     'Bazowe repozytorium z automatycznym wersjonowaniem obiektów, soft delete, filtrowanym wyszukiwaniem i paginacją dla SQL Server i PostgreSQL. Do tego cache Redis z fallbackiem, hashowanie BCrypt i wysyłka SMTP.'),
    ('A discount coupon service with API versioning, Swagger, Redis caching and object version history. Runs with a single <code>docker-compose up</code>.',
     'Serwis kuponów rabatowych z wersjonowaniem API, Swaggerem, cache Redis i historią wersji obiektów. Startuje jednym <code>docker-compose up</code>.'),
    ('Tenant management with exact and partial-match search, plus edit, disable and restore flows.',
     'Zarządzanie tenantami z wyszukiwaniem dokładnym i częściowym oraz edycją, wyłączaniem i przywracaniem.'),

    # ---- principles
    ('03 / How I build', '03 / Jak pracuję'),
    ('Small promises,<br><i>kept.</i>', 'Małe obietnice,<br><i>dotrzymane.</i>'),
    ('The same rules run through every repository above, from the website copy down to the commit history.',
     'Te same zasady obowiązują w każdym repozytorium powyżej, od tekstów na stronach po historię commitów.'),
    ('<h3>Private by default</h3><p>No analytics, tracking, cookies or third-party font services on the product sites. Credentials stay in the Keychain or the user\'s own files.</p>',
     '<h3>Prywatność domyślnie</h3><p>Bez analityki, śledzenia, ciasteczek i zewnętrznych usług z fontami na stronach produktów. Dane logowania zostają w pęku kluczy albo w plikach użytkownika.</p>'),
    ("<h3>Honest status</h3><p>Nothing is called available until it is. Every limitation is written down: what isn't supported, what needs real hardware, what the simulator can't do.</p>",
     '<h3>Uczciwy status</h3><p>Nic nie jest „dostępne”, dopóki naprawdę nie jest. Każde ograniczenie jest spisane: czego brak, co wymaga prawdziwego sprzętu, czego nie zrobi symulator.</p>'),
    ('<h3>Explicit over magic</h3><p>Saves happen when you choose. Conflicts are caught before they overwrite anything. Writes ask for confirmation and are read back to check them. Access is granted one directory at a time.</p>',
     '<h3>Jawnie zamiast magicznie</h3><p>Zapis następuje wtedy, gdy go wybierzesz. Konflikty są wykrywane, zanim cokolwiek nadpiszą. Zapis wymaga potwierdzenia i jest odczytywany do sprawdzenia. Dostęp przyznaje się katalog po katalogu.</p>'),
    ('<h3>Preview before apply</h3><p>Infrastructure changes start with a <code>pulumi preview</code>. Deploys target dev only and touch as little as possible. Data migrations go through backup, restore and a feature flag, never a big-bang switch.</p>',
     '<h3>Podgląd przed wdrożeniem</h3><p>Zmiany infrastruktury zaczynają się od <code>pulumi preview</code>. Wdrożenia celują tylko w dev i dotykają jak najmniej. Migracje danych idą przez backup, restore i feature flagę, nigdy przez jednorazowe przełączenie.</p>'),
    ('<h3>Tested like it matters</h3><p>xUnit with explicit Moq setups and FluentAssertions. LocalStack and EventStoreDB fixtures for integration tests, Cypress on the front end. Semantic versions and a changelog entry with every change.</p>',
     '<h3>Testy, bo to ważne</h3><p>xUnit z jawnymi setupami Moq i FluentAssertions. Fixture\'y LocalStack i EventStoreDB do testów integracyjnych, Cypress na froncie. Wersjonowanie semantyczne i wpis w changelogu przy każdej zmianie.</p>'),
    ("<h3>AI does the work, I review it</h3><p>Agents run the defect-to-PR loop: red, green, verify, review. I keep them on the repository's existing conventions and the smallest change that works, ask for the evidence behind every claim, and approve everything that others will see before it goes out.</p>",
     '<h3>AI wykonuje, ja sprawdzam</h3><p>Agenci prowadzą pętlę od defektu do PR: red, green, verify, review. Pilnuję, by trzymali się istniejących konwencji repozytorium i najmniejszej działającej zmiany, żądam dowodów dla każdego twierdzenia i zatwierdzam wszystko, co zobaczą inni, zanim zostanie wysłane.</p>'),

    # ---- stack
    ('04 / Toolbox', '04 / Narzędzia'),
    ('What I<br><i>reach for.</i>', 'Po co<br><i>sięgam.</i>'),
    ('.NET and AWS on the server, Swift on the device, React where the product needs it, and an agent doing the repetitive work.',
     '.NET i AWS na serwerze, Swift na urządzeniu, React tam, gdzie produkt go potrzebuje, i agent do powtarzalnej pracy.'),
    ('<span>commands, multi-tenancy</span>', '<span>komendy, multi-tenancy</span>'),
    ('<span>logging, caching</span>', '<span>logowanie, cache</span>'),
    ('<span>orchestration</span>', '<span>orkiestracja</span>'),
    ('<span>messaging</span>', '<span>komunikacja</span>'),
    ('<span>root cause</span>', '<span>szukanie przyczyn</span>'),
    ('<span>integration tests</span>', '<span>testy integracyjne</span>'),
    ('<span>desktop widgets</span>', '<span>widgety na pulpit</span>'),
    ('<span>private sync</span>', '<span>prywatna synchronizacja</span>'),
    ('<span>NDEF read / write</span>', '<span>odczyt i zapis NDEF</span>'),
    ('<span>least privilege</span>', '<span>minimalne uprawnienia</span>'),
    ('<h3>Around it <span>delivery</span></h3>', '<h3>Wokół <span>dostarczanie</span></h3>'),
    ('<span>component, hooks</span>', '<span>komponenty, hooki</span>'),
    ('<span>local stacks</span>', '<span>lokalne środowiska</span>'),
    ('<span>on-call triage</span>', '<span>triage na dyżurze</span>'),
    ('<span>daily tools</span>', '<span>na co dzień</span>'),

    # ---- contact
    ('05 / Contact', '05 / Kontakt'),
    ('Got a problem that needs a <a href="#contact" data-mail>focused tool?</a>', 'Masz problem, który potrzebuje <a href="#contact" data-mail>konkretnego narzędzia?</a>'),
    ('<span class="mail-label">Write to me</span>', '<span class="mail-label">Napisz do mnie</span>'),
    ('>Compose email\n', '>Napisz e-mail\n'),
    ('>Copy address\n', '>Kopiuj adres\n'),
    ('Replies usually within two working days, in English or Polish.', 'Odpowiadam zwykle w ciągu dwóch dni roboczych, po polsku lub angielsku.'),
    ('<span><b>Based in</b> · Poland</span>', '<span><b>Lokalizacja</b> · Polska</span>'),
    ('<span><b>Languages</b> · English, Polish</span>', '<span><b>Języki</b> · polski, angielski</span>'),
    ("<span><b>App reports</b> · through each product's issue tracker</span>", '<span><b>Zgłoszenia do aplikacji</b> · przez issue tracker każdego produktu</span>'),
    ('<span><b>Off the clock</b> · rebuilding a 1994 MX-5, Home Assistant, ESP32</span>', '<span><b>Po godzinach</b> · odbudowa MX-5 z 1994, Home Assistant, ESP32</span>'),
    ('<span>Static HTML · self-hosted fonts · no tracking · no cookies</span>', '<span>Statyczny HTML · własne fonty · bez śledzenia · bez ciasteczek</span>'),

    # ---- script strings
    ("encodeURIComponent('Hello from chrominsky.dev')", "encodeURIComponent('Wiadomość z chrominsky.dev')"),
    ("status.textContent = 'Copied to clipboard';", "status.textContent = 'Skopiowano do schowka';"),
]


def main() -> int:
    text = SRC.read_text(encoding="utf-8")
    errors = []
    for pair in PAIRS:
        en, pl = pair[0], pair[1]
        expected = pair[2] if len(pair) > 2 else 1
        found = text.count(en)
        if expected is None:
            if found == 0:
                errors.append(f"not found: {en[:70]!r}")
        elif found != expected:
            errors.append(f"expected {expected}, found {found}: {en[:70]!r}")
        text = text.replace(en, pl)
    if errors:
        print("Translation out of date:\n  " + "\n  ".join(errors), file=sys.stderr)
        return 1
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
