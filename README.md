# GitHub Contributions Art

Een Python-script dat tekst genereert op de GitHub-contributiegraph door commits te maken op specifieke data.

## Beschrijving

Dit script simuleert een 7x52 grid (52 weken, 7 dagen) en genereert commits die samen een tekstpatroon vormen op je GitHub-bijdragegraph. De tekst wordt automatisch gecentreerd en de commits hebben verschillende intensiteiten op basis van de helderheid van de pixels.

## Kenmerken

- 🎨 Genereer tekst op de GitHub-contributiegraph
- 📅 Automatische datum- en tijdstempelbeheer
- 🎯 Automatische tekstcentrering binnen het 52-weken grid
- 💪 Verschillende commit-intensiteiten voor betere zichtbaarheid
- 🐳 Devcontainer-ondersteuning voor consistente ontwikkelomgeving
- ✍️ Ondersteuning voor A-Z, 0-9 en spaties

## Vereisten

- Python 3.11 of hoger
- Git
- Pillow (Python Imaging Library)

## Installatie

### Optie 1: Met Devcontainer (aanbevolen)

Als je VS Code gebruikt met de Remote-Containers extensie:

1. Open de repository in VS Code
2. Klik op de groene knop linksonder of druk op `F1` en selecteer "Remote-Containers: Reopen in Container"
3. De devcontainer wordt automatisch opgebouwd met alle vereisten

### Optie 2: Lokale installatie

```bash
# Kloon de repository
git clone https://github.com/c3k90/github-contributions-art.git
cd github-contributions-art

# Installeer vereisten
pip install -r requirements.txt
```

## Gebruik

### Basisgebruik

```bash
python contributions_art.py "HELLO"
```

Dit creëert een nieuwe git-repository in `./contribution_repo` met commits die het woord "HELLO" vormen.

### Aangepast repository-pad

```bash
python contributions_art.py "CODE" ./my_custom_repo
```

### Voorbeelden

```bash
# Genereer "HI" 
python contributions_art.py "HI"

# Genereer "2024"
python contributions_art.py "2024"

# Genereer "PYTHON"
python contributions_art.py "PYTHON"

# Genereer met spaties
python contributions_art.py "HELLO WORLD"
```

## Hoe het werkt

1. **Tekst naar Grid**: Het script converteert de invoertekst naar een 7x52 pixelgrid met behulp van een ingebouwde 5x7 pixelfont
2. **Automatische Centrering**: De tekst wordt automatisch gecentreerd binnen het beschikbare grid
3. **Git Repository**: Een nieuwe git-repository wordt aangemaakt (of een bestaande gebruikt)
4. **Commit Generatie**: Voor elke actieve pixel worden meerdere commits gemaakt op de overeenkomstige datum
5. **Intensiteit**: Meer commits per dag = donkerdere kleur op de contributiegraph

## Grid Structuur

Het script simuleert de GitHub-contributiegraph structuur:
- **Breedte**: 52 kolommen (weken)
- **Hoogte**: 7 rijen (dagen van de week, zondag tot zaterdag)
- **Startdatum**: Standaard 52 weken geleden vanaf vandaag

## Ondersteunde Karakters

- Letters: A-Z (hoofdletterongevoelig)
- Cijfers: 0-9
- Spatie

## Tips

- **Korte teksten**: Werken het beste (max ~10 karakters afhankelijk van de breedte)
- **Visualisatie**: Het script toont een preview van het grid voordat commits worden gegenereerd
- **Validatie**: Het script valideert automatisch of de tekst past binnen het grid

## Output

Na het uitvoeren creëert het script:
- Een git-repository op het opgegeven pad
- Meerdere commit-bestanden gedateerd op specifieke data
- Een commit-geschiedenis die overeenkomt met het tekstpatroon

### Voorbeeld Output

```
============================================================
GitHub Contributions Art Generator
============================================================
Generating contributions starting from 2024-01-01...
Text: 'HELLO'

Grid visualization:
  0123456789012345678901234567890123456789012345678901
0 ············█████·█···█·█████·█···█···████··········
1 ············█···█·█···█·█·····█···█···█···█·········
2 ············█···█·█···█·█·····█···█···█···█·········
3 ············█████·█████·████··█···█···█···█·········
4 ············█···█·█···█·█·····█···█···█···█·········
5 ············█···█·█···█·█·····█···█···█···█·········
6 ············█···█·█···█·█████·█████···████··········

✓ Successfully generated 450 commits!
✓ Repository created at: /path/to/contribution_repo
============================================================
```

## Devcontainer Details

De devcontainer is geconfigureerd met:
- Python 3.11
- Git
- VS Code extensies voor Python-ontwikkeling
- Automatische installatie van vereisten

## Troubleshooting

### "Text is too long"
De tekst past niet binnen het 52-weken grid. Gebruik kortere tekst.

### "Unsupported characters"
De tekst bevat karakters die niet worden ondersteund. Gebruik alleen A-Z, 0-9 en spaties.

### Git configuratie
Het script configureert automatisch git user.name en user.email voor de contributie-repository.

## Licentie

Dit project is open source en beschikbaar onder de MIT-licentie.

## Bijdragen

Bijdragen zijn welkom! Voel je vrij om een issue te openen of een pull request in te dienen.

## Auteur

Gemaakt voor de GitHub Contributions Art community.