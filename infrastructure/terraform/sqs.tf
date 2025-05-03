resource "aws_sqs_queue" "guardian_content_dlq" {
  name                      = "guardian_content_dlq"
  message_retention_seconds = 1209600 # 14 days for DLQ
}

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

resource "aws_lambda_event_source_mapping" "publisher_trigger" {
  event_source_arn  = aws_sqs_queue.guardian_content.arn
  function_name     = aws_lambda_function.publisher_lambda.arn
  batch_size        = 10
  enabled           = true
}

output "guardian_content_queue_url" {
  value = aws_sqs_queue.guardian_content.id
}

output "guardian_content_dlq_url" {
  value = aws_sqs_queue.guardian_content_dlq.id
}

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
