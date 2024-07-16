# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0]

### Added

- Newsbereich wurde hinzugefügt

### Changed

- Links werden auf rotem Hintergrund nun weiß ausgegeben.
- Dynamisch generierte Cardblöcke für Unterseiten zeigen jetzt keine Seiten mehr an die nicht in Menüs erscheinen sollen.

### Fixed

- Unterseite die über `DynamicSolutionBlock` angezeigt werden, werden jetzt nur dann angezeigt wenn diese Live geschaltet sind. Das gleiche gilt für Karten und Unterseiten auf der `Solution Application Page`. Damit bilden beide Komponenten das Verhalten von `DynamicSolutionBlock` ab.

## [1.1.1]

### Fixed

- Globale Listen Marker auf der Messeseite wurden entfernt. 
- In der mobilen Navigation werden keine ">" mehr angezeigt.

## [1.1.0]

### Added

- 3 / 4 Spalten Komponente hinzugefügt. #177
- Unterstützung für Englische und Deutsche Link URLs in Navigationsmenü hinzugefügt. #195
- "Link in neuem Tab öffnen" als Option bei der Erstellung von Menüelementen hinzugefügt. #195
- Scrollpfeil auf Solution page #167
- IconBlock Komponente implementiert #98
- SVG Upload unterstützung wurde hinzugefügt #98
- News Bereich #230

### Changed

- Alle Youtube URLs werden nun auf youtube-nocookie.com umgeschrieben und entsprechend #222 parametrisiert
- Unsortierte Listen haben nun ">" als marker.
- Linktext wird bei allen Komponenten deren Linktext kein Pflichtfeld ist nicht vorausgefüllt.
- Bilder werden jetzt hochauflösender angezeigt.
- Globaler Titel auf "Seitenname | PARAT Solutions" gesetzt #189
- Das Bilderfeld "attribution" wurde in "Alt Text" umbenannt. #139
- Das Bilderfeld "caption" wurde entfernt. #139
- Header Bilder auf Standard- und Homepages wurden auf 1000 Pixel in der Höhe beschränkt.

### Fixed

- Solution Seite Navigation mit anderen Seiten abgeglichen
- Die Kontaktbutton Platzierung auf der Solutionseite führt nicht mehr zu einem weißen Rand auf der rechten Seite #227
- Angleich der preheadlines Größe und Linehight #158.
- Fehler in der Verlinkung des Menüs der 404 Seite wurde behoben. #125

## [1.0.1]

### Changed

- Carousel Controls werden nun mobil nicht mehr angezeigt #219
- Die Pagination Indikation wird nun immer angezeigt und ist auch immer weiß hinterlegt #219

### Fixed

- Der Videohintergrund ist jetzt transparent eingestellt, sodass das Einfügen auf einer Seite mit angepasster Hintergrundfarbe auch das richtige Ergebnis erzielt. #221
- Die mobile Sortierung von Split Containern wurde behoben. #220

## [1.0.0]

### Added

- Initiale Version
