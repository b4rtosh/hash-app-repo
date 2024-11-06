resource "azurerm_resource_group" "rg" {
  name = var.rg-name
  location = var.rg-location
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                = "cryptok8s"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "cryptok8s"

  default_node_pool {
    name            = "default"
    node_count      = "2"
    vm_size         = "Standard_D2_v2"
  }

    identity {
        type = "SystemAssigned"
    }
  tags = {
    environment = "Production"
  }
}
