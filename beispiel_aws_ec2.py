#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Beispiel: Verwendung des DevAssistant zur Erstellung eines Python-Skripts,
das AWS EC2-Instanzen mit Terraform provisioniert.

Dieses Skript demonstriert, wie der KI-gestützte Entwicklerassistent verwendet werden kann,
um eine spezifische Aufgabe zu lösen: Die Erstellung eines Python-Skripts, das AWS EC2-Instanzen
mit Terraform provisioniert.
"""

import asyncio
import os
from dev_assistant_extended import DevAssistantExtended


async def main():
    # API-Schlüssel aus Umgebungsvariable laden
    api_key = os.environ.get("OPENAI_API_KEY", "")
    
    if not api_key:
        api_key = input("Bitte gib deinen OpenAI API-Schlüssel ein: ")
    
    # DevAssistant initialisieren
    assistant = DevAssistantExtended(api_key=api_key)
    
    # Aufgabenbeschreibung
    task = "Erstelle ein Python-Skript, das AWS EC2-Instanzen mit Terraform provisioniert."
    
    print(f"\nAufgabe: {task}\n")
    print("Verarbeite die Anfrage...\n")
    
    # Aufgabe ausführen
    assistant.run(task)


if __name__ == "__main__":
    asyncio.run(main())