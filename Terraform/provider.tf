terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "Bucket Name" # "da7-terraform-state"
    region = "eu-central-1"
    profile = "AWS Profile" # "academy_trainee" 
    key    = "terraform-key"
  }
  
}

# Configure the AWS Provider
provider "aws" {
  region = "Region " # "eu-central-1"
  profile = "AWS Profile"  #"academy_trainee" 
}


