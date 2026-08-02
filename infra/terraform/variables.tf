variable "vm_host" {
  description = "Public IP address of the Mir Cloud Ubuntu VM"
  type        = string
}

variable "vm_user" {
  description = "SSH username for the VM"
  type        = string
  default     = "ubuntu"
}

variable "vm_password" {
  description = "SSH password for the VM. Prefer vm_ssh_private_key_path once key auth is set up."
  type        = string
  sensitive   = true
  default     = null
}

variable "vm_ssh_private_key_path" {
  description = "Path to an SSH private key, if using key-based auth instead of password."
  type        = string
  default     = null
}

variable "app_directory" {
  description = "Directory on the VM where the deployed application will live"
  type        = string
  default     = "/opt/enterprise-commerce-platform"
}