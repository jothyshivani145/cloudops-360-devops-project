terraform {
  required_version = ">= 1.5.0"

  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.9"
    }
  }
}

resource "local_file" "cloudops_config" {
  file_permission = "0644"
  filename        = "${path.module}/cloudops-config.txt"

  content = <<EOT
Project: ${var.project_name}
Environment: ${var.environment}
Application: Flask IT Support Ticket Management
Database: PostgreSQL
Container Platform: Docker Compose
Infrastructure Tool: Terraform
EOT
}
