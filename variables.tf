variable "prefix" {
    description = "The prefix used for all resources in this environment"
}

variable "location" {
    description = "The Azure location where all resources in this deployment should be created"
    default = "uksouth"
}

variable "failover_location" {
    description = "The Azure location which should be used if the main location for the Cosmos account is unavailable."
    default = "ukwest"
}

variable "login_disabled" {
    description = "Flag for whether to require users to log in to Flask."
    default = false
}

variable "role_for_dev_purposes" {
    description = "If logging into Flask is disabled, this variable sets what role a user should be automatically assigned."
    default = "reader"
}

