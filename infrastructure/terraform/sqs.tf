# ======================
# SQS Publisher
# ======================

# ========
# DEFINE
# ========

# IAM policy document granting required SQS actions
data "aws_iam_policy_document" "sqs_access" {
  statement {
    actions = [
      "sqs:SendMessage",
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
      "sqs:GetQueueUrl"
    ]
    resources = [
      aws_sqs_queue.guardian_content.arn,
      aws_sqs_queue.guardian_content_dlq.arn
    ]
  }
}

# IAM policy allowing Lambda to receive and delete SQS messages
resource "aws_iam_policy" "lambda_sqs_policy" {
  name        = "LambdaSQSSendReceivePolicy"
  description = "Policy to allow Lambda to receive and delete messages from SQS"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:sqs:eu-west-2:109264794038:guardian_content"
      }
    ]
  })
}

# ========
# CREATE
# ========

# Dead Letter Queue for SQS
resource "aws_sqs_queue" "guardian_content_dlq" {
  name                      = "guardian_content_dlq"
  message_retention_seconds = 1209600 # 14 days for DLQ
}

# Main SQS Queue used by publisher Lambda
resource "aws_sqs_queue" "guardian_content" {
  name                      = "guardian_content"
  message_retention_seconds = 259200  # 3 days
  visibility_timeout_seconds = 30     # default processing window
  receive_wait_time_seconds  = 5

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.guardian_content_dlq.arn
    maxReceiveCount     = 5
  })

  tags = {
    Environment = "dev"
    Project     = "GuardianStream"
  }
}

# Mapping between SQS queue and publisher Lambda function
resource "aws_lambda_event_source_mapping" "publisher_trigger" {
  event_source_arn  = aws_sqs_queue.guardian_content.arn
  function_name     = aws_lambda_function.publisher_lambda.arn
  batch_size        = 10
  enabled           = true
}

# Output the URLs of both queues
output "guardian_content_queue_url" {
  value = aws_sqs_queue.guardian_content.id
}

output "guardian_content_dlq_url" {
  value = aws_sqs_queue.guardian_content_dlq.id
}

# ========
# ATTACH
# ========

# Attach the SQS policy to the Lambda's execution role
resource "aws_iam_role_policy_attachment" "lambda_sqs_policy_attachment" {
  policy_arn = aws_iam_policy.lambda_sqs_policy.arn
  role       = aws_iam_role.publisher_lambda_role.name
}
