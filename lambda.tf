data "archive_file" "this" {
  type        = "zip"
  source_file = "source/main.py"
  output_path = "source/main.zip"
}

resource "aws_lambda_function" "this" {
  filename         = data.archive_file.this.output_path
  source_code_hash = data.archive_file.this.output_base64sha256
  function_name    = module.label.id
  role             = aws_iam_role.this.arn
  handler          = "main.lambda_handler"
  runtime          = "python3.6"
  description      = module.label.id
  tags             = module.label.tags

  memory_size = 128
  timeout     = 300

  lifecycle {
    ignore_changes = [source_code_hash]
  }
}

resource "aws_lambda_permission" "this_start" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.this_start.arn
}

resource "aws_lambda_permission" "this_stop" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.this_stop.arn
}
