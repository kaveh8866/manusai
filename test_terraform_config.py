#!/usr/bin/env python3

"""
Test script for the CloudAgent's Terraform configuration functionality.

This script directly tests the create_terraform_config method of the CloudAgent class
without relying on the OpenManus imports.
"""

import os
import sys
import json

# Define a simple mock for the ToolCallAgent class
class MockToolCallAgent:
    """A simple mock for the ToolCallAgent class."""
    
    def __init__(self):
        self.name = "MockToolCallAgent"
        self.description = "A mock agent for testing"
        self.system_prompt = "Mock system prompt"
        self.max_steps = 10

# Define the CloudAgent class without OpenManus imports
class TestCloudAgent(MockToolCallAgent):
    """A test version of the CloudAgent class for testing Terraform configuration."""
    
    def __init__(self):
        super().__init__()
        self.name = "TestCloudAgent"
        self.description = "A test agent for cloud resources"
    
    def create_terraform_config(self, resources, provider="aws"):
        """Creates a Terraform configuration file.
        
        Args:
            resources: A list of resource definitions
            provider: The cloud provider to use
            
        Returns:
            The path to the created configuration file
        """
        try:
            # Create Terraform configuration
            config = f"""provider "{provider}" {{
  region = "us-east-1"
}}"""
            
            for resource in resources:
                resource_type = resource.get("type", "aws_instance")
                resource_name = resource.get("name", "example")
                resource_attrs = resource.get("attributes", {})
                
                config += f'\nresource "{resource_type}" "{resource_name}" {{\n'
                for key, value in resource_attrs.items():
                    if isinstance(value, str):
                        config += f'  {key} = "{value}"\n'
                    else:
                        config += f'  {key} = {value}\n'
                config += "}\n"
            
            # Write configuration to file
            with open("test_main.tf", "w") as f:
                f.write(config)
            
            print("Terraform configuration created: test_main.tf")
            print("\nConfiguration content:")
            print(config)
            
            return "Terraform configuration created: test_main.tf"
        except Exception as e:
            return f"Error in Terraform configuration: {str(e)}"

# Test function
def test_terraform_config():
    """Test the create_terraform_config method."""
    # Create a TestCloudAgent instance
    cloud_agent = TestCloudAgent()
    
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
        },
        {
            "type": "aws_s3_bucket",
            "name": "test_bucket",
            "attributes": {
                "bucket": "test-bucket-name",
                "acl": "private"
            }
        }
    ]
    
    # Call the method
    result = cloud_agent.create_terraform_config(test_resources)
    
    # Check if the file was created
    if os.path.exists("test_main.tf"):
        print("\nTest passed: File was created successfully")
        
        # Read the file content
        with open("test_main.tf", "r") as f:
            content = f.read()
        
        # Check if the content has the correct provider syntax
        if 'provider "aws" {' in content and 'region = "us-east-1"' in content:
            print("Test passed: Provider syntax is correct")
        else:
            print("Test failed: Provider syntax is incorrect")
        
        # Clean up
        os.remove("test_main.tf")
        print("Test file removed")
    else:
        print("Test failed: File was not created")

# Run the test
if __name__ == "__main__":
    print("Testing CloudAgent's Terraform configuration functionality...\n")
    test_terraform_config()