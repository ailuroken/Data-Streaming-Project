# ==========================================
# Fetch Content Lambda
# ==========================================

# ========
# DEFINE
# ========

# Fetch content lambda code
data "archive_file" "fetch_content_lambda" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${path.module}/../../src/guardian_content.py"
  output_path      = "${path.module}/../../packages/guardian_content/guardian_content.zip"
}

# Fetch content layer dependency
data "archive_file" "requests_layer" {
  type             = "zip"
  output_file_mode = "0666"
  source_dir       = "${path.module}/../../layer/python"
  output_path      = "${path.module}/../../packages/guardian_content/requests_layer.zip"
}

# ========
# CREATE
# ========

# Fetch content layer dependencies
resource "aws_lambda_layer_version" "requests_layer" {
  layer_name          = "requests"
  compatible_runtimes = [var.python_runtime]
  s3_bucket           = aws_s3_bucket.code_bucket.bucket
  s3_key              = aws_s3_object.requests_layer.key
}

resource "aws_lambda_function" "fetch_content_lambda" {
  function_name = var.lambda_fetch_content
  s3_bucket     = aws_s3_bucket.code_bucket.bucket
  s3_key        = aws_s3_object.guardian_content_lambda_code.key
  role          = aws_iam_role.guardian_content_lambda_role.arn
  handler       = "guardian_content.lambda_handler"
  runtime       = var.python_runtime
  layers        = [aws_lambda_layer_version.requests_layer.arn]
}

# ==========================================
# SQS Publisher Lambda
# ==========================================

# ========
# DEFINE
# ========

# SQS Publisher lambda code
data "archive_file" "publisher_lambda_code" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${path.module}/../../src/sqs_publisher.py"
  output_path      = "${path.module}/../../packages/sqs_publisher/sqs_publisher.zip"
}

# ========
# CREATE
# ========

resource "aws_lambda_function" "publisher_lambda" {
  function_name = var.lambda_publisher
  s3_bucket     = aws_s3_bucket.publisher_code_bucket.bucket
  s3_key        = aws_s3_object.publisher_lambda_code.key
  role          = aws_iam_role.publisher_lambda_role.arn
  handler       = "sqs_publisher.lambda_handler"
  runtime       = var.python_runtime
}
