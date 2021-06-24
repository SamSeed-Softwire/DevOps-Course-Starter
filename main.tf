terraform {
    required_providers {
        azurerm = {
            source = "hashicorp/azurerm"
            version = ">= 2.49"
        }
    }
}
provider "azurerm" {
    features {}
    # Skip provider registration to avoid errors.
    skip_provider_registration = true
}

variable "failover_location" {
  default = "ukwest"
}

data "azurerm_resource_group" "main" {
    name = "SoftwirePilot_SamSeed_ProjectExercise"
}

resource "azurerm_cosmosdb_account" "main" {
    name = "softwirepilot-samseed-projectexercise-cosmos"
    resource_group_name = data.azurerm_resource_group.main.name
    location = data.azurerm_resource_group.main.location
    offer_type = "Standard"
    kind = "MongoDB"
    consistency_policy {
        consistency_level = "Eventual"
    }
    # geo_location {
    #     location = data.azurerm_resource_group.main.location
    #     failover_priority = 0
    # }
    geo_location {
        location = var.failover_location
        failover_priority = 0

    }
    capabilities {
        name = "EnableServerless"
    }
    capabilities {
        name = "EnableMongo"
    }
    lifecycle {
        prevent_destroy = true
    }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
    name                = "softwirepilot-samseed-projectexercise-mongodb"
    resource_group_name = azurerm_cosmosdb_account.main.resource_group_name
    account_name        = azurerm_cosmosdb_account.main.name
    lifecycle {
        prevent_destroy = true
    }
}

resource "azurerm_app_service_plan" "main" {
    name = "terraformed-asp"
    location = data.azurerm_resource_group.main.location
    resource_group_name = data.azurerm_resource_group.main.name
    kind = "Linux"
    reserved = true
    sku {
        tier = "Basic"
        size = "B1"
    }
    lifecycle {
        prevent_destroy = true
    }
}
resource "azurerm_app_service" "main" {
    name = "softwirepilot-samseed-projectexercise-app-service2"
    location = data.azurerm_resource_group.main.location
    resource_group_name = data.azurerm_resource_group.main.name
    app_service_plan_id = azurerm_app_service_plan.main.id
    site_config {
        app_command_line = ""
        linux_fx_version = "DOCKER|samseedsoftwire/todo-app-prod:latest"
    }
    app_settings = {
        "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    }
    lifecycle {
        prevent_destroy = true
    }
}