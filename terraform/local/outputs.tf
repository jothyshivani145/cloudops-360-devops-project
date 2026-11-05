output "generated_file" {
  description = "Location of the generated configuration"
  value       = local_file.cloudops_config.filename
}

output "project_name" {
  description = "Name of the project"
  value       = var.project_name
}
