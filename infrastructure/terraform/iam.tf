# ==================================
# IAM Role for Fetch Content Lambda
# ==================================

# ========
# DEFINE
# ========

# Fetch content lambda IAM policy doc
resource "aws_iam_policy" "guardian_content_lambda_policy" {
  name        = "guardian_content_lambda_policy"
  description = "Allow access to Secrets Manager and CloudWatch"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "secretsmanager:GetSecretValue"
        ],
        Effect   = "Allow",
        Resource = "*"
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Effect   = "Allow",
        Resource = "*"
      }
    ]
  })
}

# ========
# CREATE
# ========

# Fetch content lambda IAM role
resource "aws_iam_role" "guardian_content_lambda_role" {
  name = "guardian_content_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Principal = {
        Service = "lambda.amazonaws.com"
      },
      Effect    = "Allow",
      Sid       = ""
    }]
  })
}

# ========
# ATTACH
# ========

# Fetch code lambda policy attachment to IAM role
resource "aws_iam_role_policy_attachment" "attach_guardian_content_policy" {
  role       = aws_iam_role.guardian_content_lambda_role.name
  policy_arn = aws_iam_policy.guardian_content_lambda_policy.arn
}

# ==================================
# IAM Role for SQS Publisher Lambda
# ==================================

# ========
# DEFINE
# ========

# SQS publisher lambda IAM policy doc
resource "aws_iam_policy" "publisher_lambda_policy" {
  name        = "publisher_lambda_policy"
  description = "Allow sending messages to SQS and writing logs"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "sqs:SendMessage"
        ],
        Effect   = "Allow",
        Resource = "*"
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Effect   = "Allow",
        Resource = "*"
      }
    ]
  })
}

# ========
# CREATE
# ========

# SQS publisher lambda IAM role
resource "aws_iam_role" "publisher_lambda_role" {
  name = "publisher_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Principal = {
        Service = "lambda.amazonaws.com"
      },
      Effect    = "Allow",
      Sid       = ""
    }]
  })
}

# ========
# ATTACH
# ========

# SQS publisher lambda policy attachment to IAM role
resource "aws_iam_role_policy_attachment" "attach_publisher_policy" {
  role       = aws_iam_role.publisher_lambda_role.name
  policy_arn = aws_iam_policy.publisher_lambda_policy.arn
}
