resource "azurerm_network_interface" "vm_nic" {
  name                = "virtual_network_nic"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group_name}"

  ip_configuration {
    name                          = "internal"
    subnet_id                     = "${var.subnet_id}"
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = "${var.public_ip_address_id}"
  }
}

resource "azurerm_linux_virtual_machine" "vm" {
  name                = "test-vm"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group_name}"
  size                = "Standard_DS2_v2"
  admin_username      = "azureuser"
  network_interface_ids = [azurerm_network_interface.vm_nic.id]
  admin_ssh_key {
    username   = "azureuser"
    # public_key = file("C:/Users/congt/.ssh/id_rsa.pub")
    public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCshraDMuyydAaaABt005RU2UsMJL6DD+dxCzHhP959uVwlnZiekOuhpj7Sm4djV6CmRzYmphvUTjZZUXVfwLAE/hE8DOI5daMdbGZpK3Kvnd+4vQFQf5rtUEigHWrtadmFhAE6B4RQdlYvYlMNUvGTYLYkzlNr2JCc1FAxNCYOewgrVLDiQv+5INTqW8VLS9M+JtyucOFExcgPFjyNpSW6tWtB7KTThaSVIZfqsfwJe+Nc1oeelgvWGmnmaz/Dp2ngro6Bf4/xxtawhUsqgRXDNvinli3g/lHg3AiTCuDuPyH/2gNJs7PvK07cZyt0VZjc1RUkpekQNkMfSMAu5k8/SaU00iIkfCmNlnRXYvvmsyWAcvBiZyEQZj+c6yeKZFKsY5LUXO+/jiCYyj71tvTyXRH2KfqObq9wgkuRJUNT62TyjFjbIOmTYAOqx/cZ9r9YDegoN/luvchu+uZ9CAJfRsXjgY5vRFy39lSyUeUNv1tBV++dgbRDw3e+xipOoa0= congt@DESKTOP-M2ARS39"
  }
  os_disk {
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  # source_image_reference {
  #   publisher = "Canonical"
  #   offer     = "UbuntuServer"
  #   sku       = "18.04-LTS"
  #   version   = "latest"
  # }
  secure_boot_enabled = true
  source_image_id = "/subscriptions/894dff76-a758-451b-9ab3-9af2045d5e1f/resourceGroups/Udacity/providers/Microsoft.Compute/galleries/mygallery/images/udacityproj/versions/0.0.1"
}
