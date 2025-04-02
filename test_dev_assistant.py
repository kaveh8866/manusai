import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Import the DevAssistantExtended class
from dev_assistant_extended import DevAssistantExtended, PlanningAgent, CodeExecutionAgent, DebugAgent, CloudAgent

class TestDevAssistantExtended(unittest.TestCase):
    """Test cases for the DevAssistantExtended class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a DevAssistantExtended instance with a mock API key
        self.dev_assistant = DevAssistantExtended(api_key="mock_api_key")
    
    def test_initialization(self):
        """Test if the DevAssistantExtended initializes correctly."""
        self.assertIsInstance(self.dev_assistant.planner, PlanningAgent)
        self.assertIsInstance(self.dev_assistant.code_executor, CodeExecutionAgent)
        self.assertIsInstance(self.dev_assistant.debugger, DebugAgent)
        self.assertIsInstance(self.dev_assistant.cloud_agent, CloudAgent)
        self.assertEqual(self.dev_assistant.api_key, "mock_api_key")
    
    @patch('subprocess.run')
    def test_execute_command(self, mock_run):
        """Test the execute_command method."""
        # Configure the mock
        mock_process = MagicMock()
        mock_process.stdout = "Command executed successfully"
        mock_process.returncode = 0
        mock_run.return_value = mock_process
        
        # Call the method
        result = self.dev_assistant.execute_command("echo 'test'")
        
        # Verify the result
        self.assertEqual(result, "Command executed successfully")
        mock_run.assert_called_once_with("echo 'test'", shell=True, capture_output=True, text=True)
    
    @patch('dev_assistant_extended.openai.ChatCompletion.create')
    def test_generate_code(self, mock_create):
        """Test the generate_code method."""
        # Configure the mock
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "def hello_world():\n    print('Hello, World!')"
        mock_create.return_value = mock_response
        
        # Call the method
        result = self.dev_assistant.generate_code("Write a hello world function", model="gpt-4")
        
        # Verify the result
        self.assertEqual(result, "def hello_world():\n    print('Hello, World!')")
        mock_create.assert_called_once()
    
    def test_cloud_agent_terraform_config(self):
        """Test the CloudAgent's create_terraform_config method."""
        # Define test resources
        test_resources = [
            {
                "type": "aws_instance",
                "name": "test_instance",
                "attributes": {
                    "ami": "ami-12345",
                    "instance_type": "t2.micro",
                    "tags": {
                        "Name": "TestInstance"
                    }
                }
            }
        ]
        
        # Call the method
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            result = self.dev_assistant.cloud_agent.create_terraform_config(test_resources)
        
        # Verify the result
        self.assertIn("Terraform-Konfiguration erstellt", result)
        mock_file.assert_called_once_with("main.tf", "w")
        
        # Get the written content
        written_content = ''
        for call in mock_file().write.call_args_list:
            written_content += call[0][0]
        
        # Verify the content has correct provider syntax
        self.assertIn('provider "aws" {', written_content)
        self.assertIn('  region = "us-east-1"', written_content)
        self.assertIn('resource "aws_instance" "test_instance"', written_content)

    @patch('dev_assistant_extended.CodeExecutionAgent.execute_python')
    def test_execute_code(self, mock_execute_python):
        """Test the execute_code method."""
        # Configure the mock
        mock_execute_python.return_value = "Hello, World!"
        
        # Call the method
        result = self.dev_assistant.execute_code("print('Hello, World!')", language="python")
        
        # Verify the result
        self.assertEqual(result, "Hello, World!")
        mock_execute_python.assert_called_once_with("print('Hello, World!')")

if __name__ == '__main__':
    unittest.main()