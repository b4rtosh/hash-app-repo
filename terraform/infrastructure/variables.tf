variable "rg-name" {
  default = "crypto-rg"
}

variable "rg-location"{
  default = "polandcentral"
}

variable "client_id" {}
variable "client_secret" {
  sensitive = true
}
variable "tenant_id" {}
variable "subscription_id" {}
