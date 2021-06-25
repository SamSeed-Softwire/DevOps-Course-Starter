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

data "azurerm_resource_group" "main" {
    name = "SoftwirePilot_SamSeed_ProjectExercise"
}

resource "azurerm_cosmosdb_account" "main" {
    name = "${var.prefix}-softwirepilot-samseed-projectexercise-cosmos"
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
    name                = "${var.prefix}-softwirepilot-samseed-projectexercise-mongodb"
    resource_group_name = azurerm_cosmosdb_account.main.resource_group_name
    account_name        = azurerm_cosmosdb_account.main.name
    lifecycle {
        prevent_destroy = true
    }
}

resource "azurerm_app_service_plan" "main" {
    name = "${var.prefix}-terraformed-asp"
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
    name = "${var.prefix}-softwirepilot-samseed-projectexercise-app-service2"
    location = data.azurerm_resource_group.main.location
    resource_group_name = data.azurerm_resource_group.main.name
    app_service_plan_id = azurerm_app_service_plan.main.id
    site_config {
        app_command_line = ""
        linux_fx_version = "DOCKER|samseedsoftwire/todo-app-prod:latest"
    }
    app_settings = {
        "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
        "COSMOS_USERNAME" = azurerm_cosmosdb_account.main.name
        "COSMOS_PASSWORD" = azurerm_cosmosdb_account.main.primary_key
        "COSMOS_HOST" = "${azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com"
        "COSMOS_PORT" = 10255
        "COSMOS_TODO_APP_DATABASE" = azurerm_cosmosdb_mongo_database.main.name
    }
    lifecycle {
        prevent_destroy = true
    }
}