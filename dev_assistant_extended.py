import asyncio
import subprocess
import os
import json
import sys
from typing import List, Dict, Any, Optional, Union

import openai

# Mock classes for OpenManus imports
class ToolCallAgent:
    """Mock class for ToolCallAgent"""
    pass

class BaseAgent:
    """Mock class for BaseAgent"""
    pass

class PlanningFlow:
    """Mock class for PlanningFlow"""
    pass

class Message:
    """Mock class for Message"""
    pass

class AgentState:
    """Mock class for AgentState"""
    pass

class ToolCollection:
    """Mock class for ToolCollection"""
    pass

class Terminate:
    """Mock class for Terminate"""
    pass

class logger:
    """Mock class for logger"""
    @staticmethod
    def info(msg):
        print(msg)


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
    - Infrastruktur- und Deployment-Anforderungen
    
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
            "Teste die Implementierung",
            "Erstelle Deployment-Konfiguration"
        ]
        
        return {"task": task, "steps": steps}


class CodeExecutionAgent(ToolCallAgent):
    """Ein Agent, der Code in verschiedenen Sprachen ausführen kann."""

    name: str = "CodeExecutionAgent"
    description: str = "Ein Agent, der Code in verschiedenen Programmiersprachen ausführen kann."

    system_prompt: str = """
    Du bist ein Code-Ausführungs-Experte, der Code in verschiedenen Programmiersprachen ausführen kann.
    Du kannst Python, Java, Julia und andere Sprachen verarbeiten und ausführen.
    """

    max_steps: int = 10

    def execute_python(self, code: str) -> str:
        """Führt Python-Code aus.
        
        Args:
            code: Der auszuführende Python-Code
            
        Returns:
            Die Ausgabe der Code-Ausführung
        """
        try:
            # Code in temporäre Datei schreiben
            with open("temp_script.py", "w") as f:
                f.write(code)
            
            # Code ausführen
            result = subprocess.run(
                [sys.executable, "temp_script.py"],
                capture_output=True,
                text=True
            )
            
            # Temporäre Datei löschen
            os.remove("temp_script.py")
            
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Fehler: {result.stderr}"
        except Exception as e:
            return f"Ausführungsfehler: {str(e)}"

    def execute_java(self, code: str, class_name: str = "Main") -> str:
        """Führt Java-Code aus.
        
        Args:
            code: Der auszuführende Java-Code
            class_name: Der Name der Hauptklasse
            
        Returns:
            Die Ausgabe der Code-Ausführung
        """
        try:
            # Code in temporäre Datei schreiben
            with open(f"{class_name}.java", "w") as f:
                f.write(code)
            
            # Code kompilieren
            compile_result = subprocess.run(
                ["javac", f"{class_name}.java"],
                capture_output=True,
                text=True
            )
            
            if compile_result.returncode != 0:
                return f"Kompilierungsfehler: {compile_result.stderr}"
            
            # Code ausführen
            run_result = subprocess.run(
                ["java", class_name],
                capture_output=True,
                text=True
            )
            
            # Temporäre Dateien löschen
            os.remove(f"{class_name}.java")
            os.remove(f"{class_name}.class")
            
            if run_result.returncode == 0:
                return run_result.stdout
            else:
                return f"Laufzeitfehler: {run_result.stderr}"
        except Exception as e:
            return f"Ausführungsfehler: {str(e)}"

    def execute_julia(self, code: str) -> str:
        """Führt Julia-Code aus.
        
        Args:
            code: Der auszuführende Julia-Code
            
        Returns:
            Die Ausgabe der Code-Ausführung
        """
        try:
            # Code in temporäre Datei schreiben
            with open("temp_script.jl", "w") as f:
                f.write(code)
            
            # Code ausführen
            result = subprocess.run(
                ["julia", "temp_script.jl"],
                capture_output=True,
                text=True
            )
            
            # Temporäre Datei löschen
            os.remove("temp_script.jl")
            
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Fehler: {result.stderr}"
        except Exception as e:
            return f"Ausführungsfehler: {str(e)}"


class DebugAgent(ToolCallAgent):
    """Ein Agent, der Code-Fehler analysieren und beheben kann."""

    name: str = "DebugAgent"
    description: str = "Ein Agent, der Code-Fehler analysieren und beheben kann."

    system_prompt: str = """
    Du bist ein Debugging-Experte, der Code-Fehler analysieren und beheben kann.
    Deine Aufgabe ist es, Fehler zu identifizieren, zu verstehen und Lösungen vorzuschlagen.
    """

    max_steps: int = 10

    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        self.api_key = api_key
        if api_key:
            openai.api_key = api_key

    def analyze_error(self, code: str, error_message: str) -> str:
        """Analysiert einen Fehler im Code.
        
        Args:
            code: Der fehlerhafte Code
            error_message: Die Fehlermeldung
            
        Returns:
            Eine Analyse des Fehlers
        """
        prompt = f"""
        Analysiere den folgenden Code und die Fehlermeldung:
        
        ```
        {code}
        ```
        
        Fehlermeldung:
        {error_message}
        
        Erkläre, was der Fehler ist und warum er auftritt.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Du bist ein Debugging-Experte."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content

    def fix_error(self, code: str, error_message: str) -> str:
        """Behebt einen Fehler im Code.
        
        Args:
            code: Der fehlerhafte Code
            error_message: Die Fehlermeldung
            
        Returns:
            Der korrigierte Code
        """
        prompt = f"""
        Behebe den Fehler im folgenden Code:
        
        ```
        {code}
        ```
        
        Fehlermeldung:
        {error_message}
        
        Gib nur den korrigierten Code zurück, ohne Erklärungen.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Du bist ein Debugging-Experte."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content


class CloudAgent(ToolCallAgent):
    """Ein Agent, der Cloud-Ressourcen verwalten kann."""

    name: str = "CloudAgent"
    description: str = "Ein Agent, der Cloud-Ressourcen mit AWS CLI und Terraform verwalten kann."

    system_prompt: str = """
    Du bist ein Cloud-Experte, der Cloud-Ressourcen mit AWS CLI und Terraform verwalten kann.
    Deine Aufgabe ist es, Cloud-Infrastruktur zu planen, zu erstellen und zu verwalten.
    """

    max_steps: int = 15

    def configure_aws(self, region: str = "us-east-1") -> str:
        """Konfiguriert die AWS CLI.
        
        Args:
            region: Die zu verwendende AWS-Region
            
        Returns:
            Die Ausgabe des Konfigurationsbefehls
        """
        try:
            # AWS CLI konfigurieren
            result = subprocess.run(
                ["aws", "configure", "set", "region", region],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return f"AWS-Region auf {region} gesetzt."
            else:
                return f"Fehler bei der AWS-Konfiguration: {result.stderr}"
        except Exception as e:
            return f"AWS-Konfigurationsfehler: {str(e)}"

    def create_terraform_config(self, resources: List[Dict[str, Any]], provider: str = "aws") -> str:
        """Erstellt eine Terraform-Konfigurationsdatei.
        
        Args:
            resources: Eine Liste von Ressourcen-Definitionen
            provider: Der zu verwendende Cloud-Provider
            
        Returns:
            Der Pfad zur erstellten Konfigurationsdatei
        """
        try:
            # Terraform-Konfiguration erstellen
            config = f"""provider "{provider}" {{
  region = "us-east-1"
}}"""
            
            for resource in resources:
                resource_type = resource.get("type", "aws_instance")
                resource_name = resource.get("name", "example")
                resource_attrs = resource.get("attributes", {})
                
                config += f'resource "{resource_type}" "{resource_name}" {{\n'
                for key, value in resource_attrs.items():
                    if isinstance(value, str):
                        config += f'  {key} = "{value}"\n'
                    else:
                        config += f'  {key} = {value}\n'
                config += "}\n\n"
            
            # Konfiguration in Datei schreiben
            with open("main.tf", "w") as f:
                f.write(config)
            
            return "Terraform-Konfiguration erstellt: main.tf"
        except Exception as e:
            return f"Fehler bei der Terraform-Konfiguration: {str(e)}"

    def apply_terraform(self) -> str:
        """Wendet die Terraform-Konfiguration an.
        
        Returns:
            Die Ausgabe des Terraform-Befehls
        """
        try:
            # Terraform initialisieren
            init_result = subprocess.run(
                ["terraform", "init"],
                capture_output=True,
                text=True
            )
            
            if init_result.returncode != 0:
                return f"Terraform-Initialisierungsfehler: {init_result.stderr}"
            
            # Terraform-Plan erstellen
            plan_result = subprocess.run(
                ["terraform", "plan", "-out=tfplan"],
                capture_output=True,
                text=True
            )
            
            if plan_result.returncode != 0:
                return f"Terraform-Planungsfehler: {plan_result.stderr}"
            
            # Terraform anwenden (in einer echten Anwendung würde hier eine Bestätigung erfolgen)
            apply_result = subprocess.run(
                ["terraform", "apply", "-auto-approve", "tfplan"],
                capture_output=True,
                text=True
            )
            
            if apply_result.returncode == 0:
                return "Terraform-Konfiguration erfolgreich angewendet."
            else:
                return f"Terraform-Anwendungsfehler: {apply_result.stderr}"
        except Exception as e:
            return f"Terraform-Ausführungsfehler: {str(e)}"


class DevAssistantExtended:
    """Ein erweiterter KI-gestützter Entwicklerassistent, der auf OpenManus basiert."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialisiert den erweiterten DevAssistant.
        
        Args:
            api_key: Der OpenAI API-Schlüssel (optional, falls lokale Modelle verwendet werden)
        """
        self.api_key = api_key
        
        # Agenten initialisieren
        self.planner = PlanningAgent()
        self.code_executor = CodeExecutionAgent()
        self.debugger = DebugAgent(api_key=api_key)
        self.cloud_agent = CloudAgent()
        
        # OpenAI API-Schlüssel setzen, falls vorhanden
        if api_key:
            openai.api_key = api_key

    def generate_code(self, prompt: str, model: str = "gpt-4", language: str = "python") -> str:
        """Generiert Code mit OpenAI.
        
        Args:
            prompt: Die Beschreibung des zu generierenden Codes
            model: Das zu verwendende Sprachmodell
            language: Die gewünschte Programmiersprache
            
        Returns:
            Der generierte Code als String
        """
        full_prompt = f"Generiere {language}-Code für folgende Aufgabe: {prompt}"
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": f"Schreibe effizienten, gut dokumentierten {language}-Code."},
                {"role": "user", "content": full_prompt}
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

    def execute_code(self, code: str, language: str = "python") -> str:
        """Führt Code in der angegebenen Sprache aus.
        
        Args:
            code: Der auszuführende Code
            language: Die Programmiersprache des Codes
            
        Returns:
            Die Ausgabe der Code-Ausführung
        """
        if language.lower() == "python":
            return self.code_executor.execute_python(code)
        elif language.lower() == "java":
            return self.code_executor.execute_java(code)
        elif language.lower() == "julia":
            return self.code_executor.execute_julia(code)
        else:
            return f"Nicht unterstützte Sprache: {language}"

    def debug_code(self, code: str, error_message: str) -> Dict[str, str]:
        """Analysiert und behebt Fehler im Code.
        
        Args:
            code: Der fehlerhafte Code
            error_message: Die Fehlermeldung
            
        Returns:
            Ein Dictionary mit Analyse und korrigiertem Code
        """
        analysis = self.debugger.analyze_error(code, error_message)
        fixed_code = self.debugger.fix_error(code, error_message)
        
        return {
            "analysis": analysis,
            "fixed_code": fixed_code
        }

    def setup_cloud_infrastructure(self, resources: List[Dict[str, Any]], provider: str = "aws") -> str:
        """Richtet Cloud-Infrastruktur ein.
        
        Args:
            resources: Eine Liste von Ressourcen-Definitionen
            provider: Der zu verwendende Cloud-Provider
            
        Returns:
            Die Ausgabe der Infrastruktur-Einrichtung
        """
        # AWS konfigurieren
        aws_config_result = self.cloud_agent.configure_aws()
        print(aws_config_result)
        
        # Terraform-Konfiguration erstellen
        tf_config_result = self.cloud_agent.create_terraform_config(resources, provider)
        print(tf_config_result)
        
        # Bestätigung vom Benutzer einholen
        confirmation = input("Möchtest du die Terraform-Konfiguration anwenden? (j/n): ")
        
        if confirmation.lower() == "j":
            # Terraform anwenden
            return self.cloud_agent.apply_terraform()
        else:
            return "Terraform-Anwendung abgebrochen."

    def recommend_tools(self, task_description: str) -> Dict[str, List[str]]:
        """Empfiehlt Tools und Frameworks für eine Aufgabe.
        
        Args:
            task_description: Die Beschreibung der Aufgabe
            
        Returns:
            Ein Dictionary mit Empfehlungen für verschiedene Kategorien
        """
        prompt = f"""
        Basierend auf der folgenden Aufgabenbeschreibung, empfehle die besten Tools, Frameworks und Bibliotheken:
        
        {task_description}
        
        Gib deine Empfehlungen in folgendem JSON-Format zurück:
        {{"frameworks": ["framework1", "framework2"], "libraries": ["lib1", "lib2"], "tools": ["tool1", "tool2"]}}
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Du bist ein Experte für Softwareentwicklungstools und -frameworks."},
                {"role": "user", "content": prompt}
            ]
        )
        
        try:
            # Versuche, die Antwort als JSON zu parsen
            recommendations = json.loads(response.choices[0].message.content)
            return recommendations
        except json.JSONDecodeError:
            # Fallback, falls die Antwort kein gültiges JSON ist
            return {
                "frameworks": ["Konnte keine Frameworks extrahieren"],
                "libraries": ["Konnte keine Bibliotheken extrahieren"],
                "tools": ["Konnte keine Tools extrahieren"]
            }

    def run(self, task: str) -> None:
        """Verarbeitet eine Entwickleraufgabe.
        
        Args:
            task: Die zu erledigende Aufgabe
        """
        print(f"Planung der Aufgabe: {task}")
        
        # Tool-Empfehlungen
        print("\nEmpfohlene Tools und Frameworks:")
        recommendations = self.recommend_tools(task)
        for category, items in recommendations.items():
            print(f"  {category.capitalize()}: {', '.join(items)}")
        
        # Aufgabe planen
        plan = self.planner.plan(task)
        
        print("\nAusführungsplan:")
        for i, step in enumerate(plan["steps"]):
            print(f"  {i+1}. {step}")
        
        # Plan ausführen
        print("\nPlan wird ausgeführt:")
        for i, step in enumerate(plan["steps"]):
            print(f"\nSchritt {i+1}: {step}")
            
            if "install" in step.lower() or "bibliothek" in step.lower():
                # Bibliotheken installieren
                package_prompt = f"Welche Bibliotheken werden für folgende Aufgabe benötigt: {task}"
                packages = self.generate_code(package_prompt).strip().split('\n')
                
                for package in packages:
                    if package.strip():
                        print(f"Installiere {package}...")
                        print(self.execute_command(f"pip install {package}"))
            
            elif "projektstruktur" in step.lower():
                # Projektstruktur erstellen
                structure_prompt = f"Erstelle eine Projektstruktur für folgende Aufgabe: {task}"
                structure = self.generate_code(structure_prompt)
                print(structure)
                
                # Verzeichnisse erstellen
                for line in structure.strip().split('\n'):
                    if line.strip().startswith('mkdir'):
                        print(self.execute_command(line))
            
            elif "implementiere" in step.lower() or "kernfunktionalität" in step.lower():
                # Code generieren
                code_prompt = f"Implementiere die Kernfunktionalität für folgende Aufgabe: {task}"
                code = self.generate_code(code_prompt)
                
                print("Generierter Code:")
                print(code)
                
                # Code in Datei speichern
                filename = input("Dateiname für den generierten Code: ")
                with open(filename, "w") as f:
                    f.write(code)
                
                print(f"Code in {filename} gespeichert.")
                
                # Code ausführen (optional)
                run_code = input("Möchtest du den Code ausführen? (j/n): ")
                if run_code.lower() == "j":
                    language = filename.split('.')[-1]
                    if language == "py":
                        language = "python"
                    elif language == "java":
                        language = "java"
                    elif language == "jl":
                        language = "julia"
                    
                    print("Ausgabe:")
                    print(self.execute_code(code, language))
            
            elif "teste" in step.lower():
                # Tests generieren und ausführen
                test_prompt = f"Schreibe Tests für folgende Aufgabe: {task}"
                tests = self.generate_code(test_prompt)
                
                print("Generierte Tests:")
                print(tests)
                
                # Tests in Datei speichern
                test_filename = input("Dateiname für die Tests: ")
                with open(test_filename, "w") as f:
                    f.write(tests)
                
                print(f"Tests in {test_filename} gespeichert.")
                
                # Tests ausführen (optional)
                run_tests = input("Möchtest du die Tests ausführen? (j/n): ")
                if run_tests.lower() == "j":
                    language = test_filename.split('.')[-1]
                    if language == "py":
                        language = "python"
                    elif language == "java":
                        language = "java"
                    elif language == "jl":
                        language = "julia"
                    
                    print("Testergebnisse:")
                    print(self.execute_code(tests, language))
            
            elif "deployment" in step.lower() or "terraform" in step.lower():
                # Cloud-Infrastruktur einrichten
                infra_prompt = f"Erstelle eine Terraform-Konfiguration für folgende Aufgabe: {task}"
                infra_description = self.generate_code(infra_prompt)
                
                print("Infrastrukturbeschreibung:")
                print(infra_description)
                
                # Einfache Beispiel-Ressourcen
                resources = [
                    {
                        "type": "aws_instance",
                        "name": "example",
                        "attributes": {
                            "ami": "ami-123456",
                            "instance_type": "t2.micro"
                        }
                    }
                ]
                
                setup_infra = input("Möchtest du die Cloud-Infrastruktur einrichten? (j/n): ")
                if setup_infra.lower() == "j":
                    print(self.setup_cloud_infrastructure(resources))
            
            else:
                # Allgemeiner Code-Generator für andere Schritte
                code = self.generate_code(step)
                print(code)
        
        print("\nAufgabe abgeschlossen.")


async def main():
    # API-Schlüssel aus Umgebungsvariable oder Konfigurationsdatei laden
    api_key = os.environ.get("OPENAI_API_KEY", "")
    
    if not api_key:
        api_key = input("Bitte gib deinen OpenAI API-Schlüssel ein (oder drücke Enter, um fortzufahren ohne Schlüssel): ")
    
    assistant = DevAssistantExtended(api_key=api_key if api_key else None)
    
    try:
        task = input("Gib deine Entwicklungsaufgabe ein: ")
        if not task.strip():
            print("Keine Aufgabe eingegeben.")
            return

        print("Verarbeite deine Anfrage...")
        assistant.run(task)
    except KeyboardInterrupt:
        print("\nOperation unterbrochen.")
    except Exception as e:
        print(f"Fehler: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())