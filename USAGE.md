# Gebruikshandleiding / Usage Guide

## Quick Start

```bash
python contributions_art.py "HELLO"
```

## Stap-voor-stap / Step-by-step

### 1. Installeer vereisten / Install requirements
```bash
pip install -r requirements.txt
```

### 2. Genereer tekst / Generate text
```bash
# Basis voorbeeld
python contributions_art.py "HI"

# Met aangepast pad
python contributions_art.py "CODE" ./my_art_repo
```

### 3. Bekijk het resultaat / View the result
```bash
cd contribution_repo  # of je aangepaste pad
git log --oneline | head -10
git log --stat
```

### 4. Upload naar GitHub (optioneel) / Upload to GitHub (optional)
```bash
# Maak een nieuw repository op GitHub
# Create a new repository on GitHub

# Voeg remote toe en push
# Add remote and push
git remote add origin https://github.com/yourusername/your-art-repo.git
git branch -M main
git push -u origin main
```

## Voorbeelden / Examples

### Korte teksten / Short texts
```bash
python contributions_art.py "HI"
python contributions_art.py "OK"
python contributions_art.py "YES"
```

### Met nummers / With numbers
```bash
python contributions_art.py "2024"
python contributions_art.py "ABC 123"
```

### Langere teksten / Longer texts
```bash
python contributions_art.py "PYTHON"
python contributions_art.py "CODE ART"
```

## Tips

1. **Tekst lengte**: Maximaal ~10 karakters werken het beste
2. **Visualisatie**: Het script toont een preview voordat commits worden gemaakt
3. **Testen**: Test eerst lokaal voordat je naar GitHub pusht
4. **Karakters**: Alleen A-Z, 0-9 en spaties worden ondersteund

## Veelgestelde vragen / FAQ

**Q: Hoe lang duurt het om te genereren?**
A: Enkele seconden tot een minuut, afhankelijk van de tekstlengte.

**Q: Kan ik de startdatum aanpassen?**
A: Ja, pas de `start_date` parameter aan in de code.

**Q: Werkt dit op mijn echte GitHub profiel?**
A: Alleen als je het gegenereerde repository naar GitHub pusht en de commits vooraf zijn gedaan.

**Q: Kan ik speciale karakters gebruiken?**
A: Momenteel alleen A-Z, 0-9 en spaties. Voor andere karakters moet je de font dictionary aanpassen.

## Problemen oplossen / Troubleshooting

### "Text is too long"
De tekst is te lang voor het 52-weken grid. Gebruik een kortere tekst.

### "Unsupported characters"
De tekst bevat niet-ondersteunde karakters. Gebruik alleen A-Z, 0-9 en spaties.

### Git configuratie fouten
Het script configureert automatisch git voor je. Als je problemen hebt, controleer of git correct is geïnstalleerd:
```bash
git --version
```

## Devcontainer

Als je VS Code gebruikt met Remote-Containers:
1. Open de repository in VS Code
2. Klik op "Reopen in Container"
3. Alle vereisten worden automatisch geïnstalleerd

## Licentie

Open source onder MIT licentie.
