#terraform {
#  required_providers {
#    aws = {
#      source  = "hashicorp/aws"
#      version = "~> 5.0"
#    }
#  }
#  backend "s3" {
#    bucket = "guardian-api-data-streaming"
#    key    = "guardian-api-data-streaming-project"
#    region = "eu-west-2"
#  }
#}

provider "aws" {
  region = "eu-west-2"
  default_tags {
    tags = {
      ProjectName  = "Data Streaming"
      DeployedFrom = "Terraform"
      Repository   = "Data-Streaming-Project"
      CostCentre   = "DE"
      Environment  = "dev"
    }
  }
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}
