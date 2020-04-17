terraform {
  required_version = "~> 0.12"
  backend "remote" {}
}

module "label" {
  source      = "git::https://github.com/cloudposse/terraform-null-label.git?ref=master"
  namespace   = var.label["namespace"]
  stage       = var.label["stage"]
  name        = var.label["name"]
  attributes  = [var.label["namespace"], var.label["stage"], var.label["name"]]
  delimiter   = "_"
  label_order = ["namespace", "stage", "name"]
}

module "kms_key" {
  source                  = "git::https://github.com/cloudposse/terraform-aws-kms-key.git?ref=master"
  namespace               = var.label["namespace"]
  stage                   = var.label["stage"]
  name                    = var.label["name"]
  description             = format("%s%s", "KMS key for ", var.label["namespace"])
  deletion_window_in_days = 10
  enable_key_rotation     = true
  alias                   = format("%s%s", "alias/", module.label.id)
}