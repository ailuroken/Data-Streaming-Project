variable "code_bucket_prefix" {
  type    = string
  default = "guardian-content-code"
}

variable "publisher_code_bucket_prefix" {
  type    = string
  default = "publisher-code"
}

variable "lambda_fetch_content" {
  type    = string
  default = "content_lambda"
}

variable "lambda_publisher" {
  type    = string
  default = "publisher_lambda"
}

variable "python_runtime" {
  type    = string
  default = "python3.12"
}
