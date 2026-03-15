# IAM Role Manager Lambda

A CloudFormation custom resource backed by AWS Lambda that automates the creation and management of IAM roles and policies with validation logic beyond what native CloudFormation IAM resources support.


## Overview

CloudFormation's built-in IAM resources (`AWS::IAM::Role`, `AWS::IAM::Policy`) provide straightforward role provisioning but offer no guardrails around what gets created. 

This custom resource fills that gap by intercepting IAM operations and applying a layer of policy validation, permission boundary enforcement, and naming convention checks before any IAM resource is actually created or modified.

The Lambda function handles CloudFormation's Create, Update, and Delete lifecycle events and communicates results back via a pre-signed S3 URL (the standard CloudFormation custom resource response protocol).
