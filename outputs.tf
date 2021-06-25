output "webapp_url" {
    description = "The URL of the app."
    value = "https://${azurerm_app_service.main.default_site_hostname}"
}

output "deployment_webhook_url" {
    description = "The Azure App Service webhook that, when called using a POST request, causes the app to pull a fresh Docker image and redploy."
    value = "https://${azurerm_app_service.main.site_credential[0].username}:${azurerm_app_service.main.site_credential[0].password}@${azurerm_app_service.main.name}.scm.azurewebsites.net/docker/hook"
}