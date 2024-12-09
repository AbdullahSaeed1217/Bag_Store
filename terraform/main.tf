# main.tf

# Create a Docker network
resource "docker_network" "app_network" {
  name = "app_network"
}

# PostgreSQL Container
resource "docker_container" "db" {
  name  = "bagstore_db"
  image = "postgres:14"
  env   = [
    "POSTGRES_USER=your_user",
    "POSTGRES_PASSWORD=your_password",
    "POSTGRES_DB=your_db"
  ]
  ports {
    internal = 5432
    external = 5432
  }
  networks_advanced {
    name = docker_network.app_network.name
  }
  volumes {
    container_path = "/var/lib/postgresql/data"
    host_path      = "${path.module}/postgres_data"
  }
}

# Django Container
resource "docker_container" "django" {
  name  = "bagstore_django"
  image = "django-app:latest"
  build {
    context    = "${path.module}/.."
    dockerfile = "${path.module}/../Dockerfile"
  }
  ports {
    internal = 3000
    external = 3000
  }
  depends_on = [docker_container.db]
  networks_advanced {
    name = docker_network.app_network.name
  }
}

# NGINX Container
resource "docker_container" "nginx" {
  name  = "bagstore_nginx"
  image = "nginx:latest"
  ports {
    internal = 80
    external = 80
  }
  volumes {
    container_path = "/etc/nginx/conf.d/default.conf"
    host_path      = "${path.module}/../nginx/nginx.conf"
  }
  depends_on = [docker_container.django]
  networks_advanced {
    name = docker_network.app_network.name
  }
}
