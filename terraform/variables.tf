# variables.tf
variable "db_user" {
  description = "Database username"
  default     = "your_user"
}

variable "db_password" {
  description = "Database password"
  default     = "your_password"
}

variable "db_name" {
  description = "Database name"
  default     = "your_db"
}
