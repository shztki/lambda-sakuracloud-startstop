variable "label" {
  default = {
    namespace = "shztki"
    stage     = "dev"
    name      = "sakuracloud-startstop"
  }
}

variable "sacloud_access_token" {}
variable "sacloud_access_token_secret" {}
variable "slack_webhook_url" {}