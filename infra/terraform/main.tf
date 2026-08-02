terraform {
  required_version = ">= 1.9"
}

locals {
  # Prefer key-based auth if a key path was provided; fall back to password.
  # This is the mechanical half of Decision 3 — flip auth method by
  # setting one variable, nothing else changes.
  ssh_connection = {
    type        = "ssh"
    host        = var.vm_host
    user        = var.vm_user
    password    = var.vm_ssh_private_key_path == null ? var.vm_password : null
    private_key = var.vm_ssh_private_key_path == null ? null : file(var.vm_ssh_private_key_path)
    timeout     = "2m"
  }
}

resource "null_resource" "provision_vm" {
  # Re-runs provisioning if the script itself changes — Terraform tracks
  # this via a trigger hash, since null_resource has no real state of
  # its own to compare against otherwise.
  triggers = {
    script_hash = filesha256("${path.module}/scripts/provision.sh")
  }

  connection {
    type        = local.ssh_connection.type
    host        = local.ssh_connection.host
    user        = local.ssh_connection.user
    password    = local.ssh_connection.password
    private_key = local.ssh_connection.private_key
    timeout     = local.ssh_connection.timeout
  }

  provisioner "file" {
    source      = "${path.module}/scripts/provision.sh"
    destination = "/tmp/provision.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/provision.sh",
      "sudo /tmp/provision.sh ${var.app_directory}",
    ]
  }
}