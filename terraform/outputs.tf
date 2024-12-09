# outputs.tf
output "django_container_ip" {
  value = docker_container.django.ip_address
}

output "nginx_container_ip" {
  value = docker_container.nginx.ip_address
}
