# provider.tf
provider "docker" {
  host = "unix:///var/run/docker.sock"
}
