---
name: terraform-expert
description: Expert-level Terraform IaC. Use when writing Terraform configs, providers, modules, state management, workspaces, remote backends, Terragrunt, or managing cloud infrastructure. Also use when the user mentions 'tfstate', 'terraform plan', 'terraform apply', 'module', 'provider', 'backend', 'Terragrunt', or 'infrastructure as code'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Terraform Expert

You are an expert in Terraform and infrastructure as code with deep knowledge of HCL, module design, state management, and multi-cloud patterns.

## Before Starting

1. **Cloud provider** — AWS, GCP, Azure, or multi-cloud?
2. **Terraform version** — 1.5, 1.6, 1.7, 1.8, OpenTofu?
3. **State backend** — S3, GCS, Terraform Cloud, Azure Blob?
4. **Team size** — solo or multiple engineers sharing state?
5. **Problem type** — writing configs, module design, state issues, CI/CD?

---

## Core Expertise Areas

- **HCL syntax**: variables, locals, outputs, expressions, functions, dynamic blocks
- **Providers**: version constraints, aliases, multiple providers in one config
- **Resources & data sources**: lifecycle, depends_on, count vs for_each, import blocks
- **Modules**: design patterns, input/output, versioning, composition, Terraform Registry
- **State management**: remote backends, locking, state mv/rm/import, workspaces
- **Functions**: string, collection, numeric, filesystem, encoding, hash functions
- **Terragrunt**: DRY patterns, dependency blocks, run-all, keep_state
- **CI/CD**: plan/apply pipelines, Atlantis, Terraform Cloud, GitHub Actions

---

## Key Patterns & Code

### Project Structure
```
infrastructure/
  modules/
    vpc/
      main.tf
      variables.tf
      outputs.tf
      versions.tf
    eks/
      main.tf
      variables.tf
      outputs.tf
    rds/
      main.tf
      variables.tf
      outputs.tf
  environments/
    prod/
      main.tf
      terraform.tfvars
      backend.tf
      versions.tf
    staging/
      main.tf
      terraform.tfvars
    dev/
      main.tf
      terraform.tfvars
  global/
    main.tf
    variables.tf
```

### versions.tf — Always Pin Versions
```hcl
terraform {
  required_version = ">= 1.6.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}
```

### backend.tf — Remote State with Locking
```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state-prod"
    key            = "prod/main/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

### variables.tf — Best Practices
```hcl
variable "environment" {
  description = "Deployment environment"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Must be one of: dev, staging, prod"
  }
}

variable "vpc_config" {
  description = "VPC configuration"
  type = object({
    cidr_block           = string
    availability_zones   = list(string)
    private_subnet_cidrs = list(string)
    public_subnet_cidrs  = list(string)
    enable_nat_gateway   = bool
  })
}

variable "db_password" {
  description = "Database master password"
  type        = string
  sensitive   = true  # never logged or shown in plan
}
```

### locals.tf — Computed Values
```hcl
locals {
  name_prefix = "${var.project}-${var.environment}"

  common_tags = merge(var.tags, {
    Environment = var.environment
    ManagedBy   = "terraform"
    Repository  = "github.com/myorg/infrastructure"
  })

  is_production = var.environment == "prod"
  instance_type = local.is_production ? "m5.large" : "t3.medium"
  multi_az      = local.is_production ? true : false
}
```

### Resources — count vs for_each
```hcl
# count: simple numeric repetition
resource "aws_instance" "web" {
  count         = var.instance_count
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-web-${count.index + 1}"
  })
}

# for_each: preferred for unique resources — no index shifting
resource "aws_s3_bucket" "data" {
  for_each = toset(["raw", "processed", "archive"])
  bucket   = "${local.name_prefix}-${each.key}-data"

  tags = merge(local.common_tags, {
    Name    = "${local.name_prefix}-${each.key}"
    Purpose = each.key
  })
}

# for_each with map — full control over each resource
resource "aws_iam_user" "team" {
  for_each = {
    alice = "admin"
    bob   = "developer"
    carol = "readonly"
  }

  name = each.key
  tags = { Role = each.value }
}
```

### Dynamic Blocks
```hcl
resource "aws_security_group" "api" {
  name   = "${local.name_prefix}-api-sg"
  vpc_id = module.vpc.vpc_id

  dynamic "ingress" {
    for_each = var.allowed_ports
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      description = "Allow port ${ingress.value}"
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  lifecycle {
    create_before_destroy = true
  }

  tags = local.common_tags
}
```

### Module Design Pattern
```hcl
# modules/rds/variables.tf
variable "identifier"        { type = string }
variable "instance_class"    { type = string }
variable "database_name"     { type = string }
variable "master_username"   { type = string }
variable "master_password"   { type = string; sensitive = true }
variable "allocated_storage" { type = number; default = 20 }
variable "multi_az"          { type = bool;   default = false }
variable "vpc_id"            { type = string }
variable "subnet_ids"        { type = list(string) }
variable "tags"              { type = map(string); default = {} }

# modules/rds/outputs.tf
output "endpoint"    { value = aws_db_instance.this.endpoint }
output "port"        { value = aws_db_instance.this.port }
output "db_name"     { value = aws_db_instance.this.db_name }

# modules/rds/main.tf
resource "aws_db_instance" "this" {
  identifier     = var.identifier
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = var.instance_class

  db_name  = var.database_name
  username = var.master_username
  password = var.master_password

  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.allocated_storage * 3

  multi_az               = var.multi_az
  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  backup_retention_period  = var.multi_az ? 7 : 1
  deletion_protection      = var.multi_az
  skip_final_snapshot      = !var.multi_az
  performance_insights_enabled = true

  tags = var.tags
}

# Calling the module from environment
module "database" {
  source = "../../modules/rds"

  identifier      = "${local.name_prefix}-db"
  instance_class  = local.is_production ? "db.r6g.large" : "db.t3.medium"
  database_name   = "myapp"
  master_username = "admin"
  master_password = var.db_password
  multi_az        = local.is_production
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = module.vpc.private_subnet_ids
  tags            = local.common_tags
}
```

### State Management Commands
```bash
# List all resources in state
terraform state list

# Show details of a specific resource
terraform state show aws_instance.web[0]

# Rename a resource without destroying it
terraform state mv aws_instance.web aws_instance.api

# Remove from state but keep real resource
terraform state rm aws_s3_bucket.old

# Import existing resource into state
terraform import aws_s3_bucket.my_bucket my-existing-bucket-name

# Terraform 1.5+ declarative import block
# import {
#   to = aws_s3_bucket.my_bucket
#   id = "my-existing-bucket-name"
# }

# Sync state with real infrastructure
terraform apply -refresh-only

# Targeted apply — use sparingly
terraform apply -target=module.vpc

# Plan with var file and save output
terraform plan -var-file=terraform.tfvars -out=tfplan

# Apply the saved plan
terraform apply tfplan
```

### Lifecycle Rules
```hcl
resource "aws_db_instance" "prod" {
  # ...

  lifecycle {
    # Never delete this resource via Terraform
    prevent_destroy = true

    # Ignore changes to these fields (e.g. changed outside Terraform)
    ignore_changes = [
      engine_version,
      snapshot_identifier,
    ]

    # Create new before destroying old (zero downtime)
    create_before_destroy = true
  }
}
```

### Data Sources
```hcl
# Reference existing resources not managed by this config
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-22.04-amd64-server-*"]
  }
}

data "aws_vpc" "existing" {
  tags = { Name = "production-vpc" }
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# Use outputs from another state file
data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "my-terraform-state-prod"
    key    = "prod/network/terraform.tfstate"
    region = "us-east-1"
  }
}

# Reference it
resource "aws_instance" "app" {
  subnet_id = data.terraform_remote_state.network.outputs.private_subnet_id
}
```

---

## Best Practices

- Always pin provider and Terraform versions — never use open-ended constraints
- Use for_each over count for resources with unique identities
- Use modules for any pattern used more than once
- Use remote state with locking — never local state for team projects
- Run terraform fmt and terraform validate in CI on every PR
- Use terraform plan -out=tfplan then apply the saved plan in CI pipelines
- Never use -auto-approve without a saved verified plan
- Mark all secret variables as sensitive = true
- Tag every resource with environment, team, and cost-center
- Use lifecycle prevent_destroy = true for production databases and critical resources

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Local state | Lost state, no team sharing | Always use remote backend with locking |
| No version pinning | Breaking changes from provider updates | Pin all provider and Terraform versions |
| count for unique resources | Index shift causes recreation | Use for_each with string keys |
| Secrets in tfvars committed to git | Credentials exposed | Use environment variables or secrets manager |
| No prevent_destroy | Accidental deletion of prod database | Add lifecycle prevent_destroy to critical resources |
| Monolithic config | Slow plans, hard to maintain | Split into focused modules |
| Direct apply in CI | No review of changes | Always plan first, apply saved plan |
| Ignoring drift | Real infra diverges from state | Run terraform apply -refresh-only regularly |

---

## Related Skills

- **aws-expert**: For AWS-specific Terraform resources
- **kubernetes-expert**: For Terraform EKS and Helm provider
- **cicd-expert**: For Terraform in CI/CD pipelines
- **docker-expert**: For ECR and container infrastructure
- **monitoring-expert**: For Terraform observability resources
