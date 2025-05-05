
# ====================
# CREATE S3 BUCKETS
# ====================

resource "aws_s3_bucket" "code_bucket" {
  # S3 bucket for the fetch guardian content code. 
  bucket_prefix = "ds-${var.code_bucket_prefix}"
  tags = {
    Name = "CodeBucket"
  }
}

resource "aws_s3_bucket" "publisher_code_bucket" {
  # S3 bucket for the SQS publisher code. 
  bucket_prefix = "ds-${var.publisher_code_bucket_prefix}"
  tags = {
    Name = "PublisherBucket"
  }
}

# ==========================================
# Fetch Content Lambda
# ==========================================

# ========
# CREATE
# ========

# Fetch content lambda code
resource "aws_s3_object" "guardian_content_lambda_code" {
  bucket = aws_s3_bucket.code_bucket.bucket
  key    = "packages/guardian_content/guardian_content.zip"
  source = data.archive_file.fetch_content_lambda.output_path
}

# Fetch content requests layer
resource "aws_s3_object" "requests_layer" {
  bucket = aws_s3_bucket.code_bucket.bucket
  key    = "requests_layer.zip"
  source = data.archive_file.requests_layer.output_path
  etag   = filemd5(data.archive_file.requests_layer.output_path)
}

# ==========================================
# SQS Publisher Lambda
# ==========================================

# ========
# CREATE
# ========

# SQS publisher lambda code
resource "aws_s3_object" "publisher_lambda_code" {
  bucket = aws_s3_bucket.publisher_code_bucket.bucket
  key    = "publisher_lambda/publisher_lambda.zip"
  source = data.archive_file.publisher_lambda_code.output_path
}
