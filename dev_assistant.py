import asyncio
import subprocess
import os
import json
from typing import List, Dict, Any, Optional

import openai

# OpenManus-Importe
from OpenManus.app.agent.toolcall import ToolCallAgent
from OpenManus.app.agent.base import BaseAgent
from OpenManus.app.flow.planning import PlanningFlow
from OpenManus.app.schema import Message, AgentState
from OpenManus.app.tool import ToolCollection, Terminate
from OpenManus.app.logger import logger


class PlanningAgent(ToolCallAgent):
    """Ein Agent, der für die Planung von Entwicklungsaufgaben zuständig ist."""

    name: str = "PlanningAgent"
    description: str = "Ein Agent, der komplexe Entwicklungsaufgaben in Teilschritte zerlegt."

    system_prompt: str = """
    Du bist ein erfahrener Planungsexperte, der komplexe Entwicklungsaufgaben in logische Teilschritte zerlegt.
    Deine Aufgabe ist es, einen detaillierten Plan zu erstellen, der folgende Aspekte berücksichtigt:
    - Notwendige Bibliotheken und Tools
    - Erforderliche Code-Komponenten
    - Abhängigkeiten zwischen Teilschritten
    - Teststrategien
    
    Erstelle einen strukturierten Plan mit klaren, ausführbaren Schritten.
    """

    max_steps: int = 15

    def plan(self, task: str) -> Dict[str, Any]:
        """Erstellt einen Plan für die gegebene Aufgabe."""
        # In einer vollständigen Implementierung würde hier das LLM verwendet werden
        # Für dieses Beispiel verwenden wir eine vereinfachte Implementierung
        steps = [
            f"Analysiere die Anforderungen: {task}",
            "Identifiziere benötigte Bibliotheken",
            "Erstelle Projektstruktur",
            "Implementiere Kernfunktionalität",
            "Teste die Implementierung"
        ]
        
        return {"task": task, "steps": steps}


class DevAssistant:
    """Ein KI-gestützter Entwicklerassistent, der auf OpenManus basiert."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialisiert den DevAssistant.
        
        Args:
            api_key: Der OpenAI API-Schlüssel (optional, falls lokale Modelle verwendet werden)
        """
        self.planner = PlanningAgent()
        self.executor = ToolCallAgent()
        self.api_key = api_key
        
        if api_key:
            openai.api_key = api_key

    def generate_code(self, prompt: str, model: str = "gpt-4") -> str:
        """Generiert Code mit OpenAI.
        
        Args:
            prompt: Die Beschreibung des zu generierenden Codes
            model: Das zu verwendende Sprachmodell
            
        Returns:
            Der generierte Code als String
        """
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "Schreibe effizienten, gut dokumentierten Code."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    def execute_command(self, command: str) -> str:
        """Führt Terminal-Befehle aus.
        
        Args:
            command: Der auszuführende Befehl
            
        Returns:
            Die Ausgabe des Befehls oder eine Fehlermeldung
        """
        try:
            print(f"Ausführen: {command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return str(e)

    def clone_repo(self, repo_url: str, path: str = "./repo") -> str:
        """Klont ein GitHub-Repository.
        
        Args:
            repo_url: Die URL des zu klonenden Repositories
            path: Der Pfad, in den das Repository geklont werden soll
            
        Returns:
            Eine Erfolgsmeldung oder eine Fehlermeldung
        """
        try:
            result = self.execute_command(f"git clone {repo_url} {path}")
            print(f"Repository geklont nach {path}")
            return result
        except Exception as e:
            return str(e)

    def install_package(self, package: str) -> str:
        """Installiert eine Python-Bibliothek.
        
        Args:
            package: Der Name der zu installierenden Bibliothek
            
        Returns:
            Die Ausgabe des Installationsbefehls
        """
        return self.execute_command(f"pip install {package}")

    def configure_terraform(self, provider: str = "aws") -> str:
        """Erstellt eine Terraform-Konfigurationsdatei.
        
        Args:
            provider: Der zu verwendende Cloud-Provider
            
        Returns:
            Eine Erfolgsmeldung
        """
        tf_config = f"""
        provider "{provider}" {{
          region = "us-east-1"
        }}

        resource "aws_instance" "example" {{
          ami           = "ami-123456"
          instance_type = "t2.micro"
        }}
        """
        with open("main.tf", "w") as file:
            file.write(tf_config)
        return "Terraform-Konfiguration erstellt."

    def debug_code(self, code: str, error_message: str) -> str:
        """Analysiert und behebt Fehler im Code.
        
        Args:
            code: Der fehlerhafte Code
            error_message: Die Fehlermeldung
            
        Returns:
            Vorschläge zur Fehlerbehebung
        """
        prompt = f"""
        Analysiere den folgenden Code und die Fehlermeldung und schlage eine Lösung vor:
        
        ```python
        {code}
        ```
        
        Fehlermeldung:
        {error_message}
        """
        return self.generate_code(prompt)

    def run(self, task: str) -> None:
        """Verarbeitet eine Entwickleraufgabe.
        
        Args:
            task: Die zu erledigende Aufgabe
        """
        print(f"Planung der Aufgabe: {task}")
        plan = self.planner.plan(task)

        for step in plan["steps"]:
            print(f"Schritt: {step}")
            if "install" in step.lower():
                package = step.split()[-1]
                print(self.install_package(package))
            elif "git clone" in step.lower():
                repo_url = step.split()[-1]
                self.clone_repo(repo_url)
            elif "terraform" in step.lower():
                print(self.configure_terraform())
            else:
                print(self.generate_code(step))


async def main():
    # API-Schlüssel aus Umgebungsvariable oder Konfigurationsdatei laden
    api_key = os.environ.get("OPENAI_API_KEY", "")
    
    assistant = DevAssistant(api_key=api_key)
    
    try:
        task = input("Gib deine Entwicklungsaufgabe ein: ")
        if not task.strip():
            print("Keine Aufgabe eingegeben.")
            return

        print("Verarbeite deine Anfrage...")
        assistant.run(task)
        print("Aufgabe abgeschlossen.")
    except KeyboardInterrupt:
        print("\nOperation unterbrochen.")
    except Exception as e:
        print(f"Fehler: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())