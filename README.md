# KI-gestützter Entwicklerassistent mit OpenManus

Dieses Projekt implementiert einen KI-gestützten Entwicklerassistenten, der auf dem OpenManus-Framework basiert. Der Assistent kann bei verschiedenen Entwicklungsaufgaben unterstützen, wie Code-Generierung, Terminal-Interaktion, Cloud-Ressourcenverwaltung und mehr.

## Funktionen

### Basisversion (dev_assistant.py)
- **Planung von Entwicklungsaufgaben**: Zerlegt komplexe Aufgaben in logische Teilschritte
- **Code-Generierung**: Generiert Code mit OpenAI-Modellen
- **Terminal-Interaktion**: Führt Shell-Befehle aus
- **Git-Integration**: Klont Repositories
- **Paketmanagement**: Installiert benötigte Bibliotheken
- **Terraform-Integration**: Erstellt Terraform-Konfigurationen für Cloud-Ressourcen
- **Debugging-Unterstützung**: Analysiert und behebt Fehler im Code

### Erweiterte Version (dev_assistant_extended.py)
- **Multi-Sprachen-Unterstützung**: Kann Code in Python, Java und Julia ausführen
- **Erweiterte Debugging-Funktionen**: Detaillierte Fehleranalyse und automatische Fehlerbehebung
- **Cloud-Integration**: Verwaltet AWS-Ressourcen mit AWS CLI und Terraform
- **Tool-Empfehlungen**: Empfiehlt automatisch die besten Frameworks und Bibliotheken für eine Aufgabe
- **Interaktive Ausführung**: Führt den generierten Code aus und zeigt die Ergebnisse an

## Installation

1. Klone das OpenManus-Repository:
   ```bash
   git clone https://github.com/kaveh8866/manusai.git
   ```

2. Installiere die benötigten Abhängigkeiten:
   ```bash
   cd OpenManus
   pip install -r requirements.txt
   pip install openai gitpython boto3
   ```

3. Setze deinen OpenAI API-Schlüssel als Umgebungsvariable:
   ```bash
   export OPENAI_API_KEY="dein-api-schlüssel"
   ```

## Verwendung

### Basisversion

```bash
python dev_assistant.py
```

### Erweiterte Version

```bash
python dev_assistant_extended.py
```

Beide Versionen werden dich nach einer Entwicklungsaufgabe fragen und dann einen Plan erstellen und ausführen, um diese Aufgabe zu lösen.

## Erweiterungsmöglichkeiten

1. **Lokale Sprachmodelle**: Integration von lokalen LLMs wie LLaMA oder GPT-4-All
2. **Erweiterte Multi-Sprachen-Unterstützung**: Hinzufügen weiterer Programmiersprachen
3. **Verbesserte Debugging-Funktionen**: Automatische Fehleranalyse und -behebung
4. **Kubernetes-Integration**: Verwaltung von Kubernetes-Clustern
5. **Docker-Integration**: Erstellung und Verwaltung von Docker-Containern

## Architektur

Der Entwicklerassistent basiert auf der modularen Architektur von OpenManus und verwendet verschiedene Agenten für spezifische Aufgaben:

- **PlanningAgent**: Zerlegt komplexe Aufgaben in Teilschritte
- **CodeExecutionAgent**: Führt Code in verschiedenen Sprachen aus
- **DebugAgent**: Analysiert und behebt Fehler im Code
- **CloudAgent**: Verwaltet Cloud-Ressourcen

Diese Agenten arbeiten zusammen, um eine vollständige Entwicklungsumgebung zu bieten, die bei der Erstellung, Ausführung und Bereitstellung von Code unterstützt.