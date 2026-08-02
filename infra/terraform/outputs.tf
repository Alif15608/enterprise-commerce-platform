output "vm_host" {
  description = "Public IP of the provisioned VM"
  value       = var.vm_host
}

output "app_directory" {
  description = "Directory on the VM where the application will be deployed (Phase 17 target)"
  value       = var.app_directory
}