resource "aws_cloudwatch_event_rule" "this_start" {
  name                = format("%s%s", module.label.id, "-start")
  description         = "Execute sakuracloud server start lambda function mon-fri AM9:30(JST)"
  schedule_expression = "cron(30 0 ? * MON-FRI *)"
}

resource "aws_cloudwatch_event_rule" "this_stop" {
  name                = format("%s%s", module.label.id, "-stop")
  description         = "Execute sakuracloud server stop lambda function mon-fri PM6:30(JST)"
  schedule_expression = "cron(30 9 ? * MON-FRI *)"
}

resource "aws_cloudwatch_event_target" "this_start" {
  rule = aws_cloudwatch_event_rule.this_start.name
  arn  = aws_lambda_function.this.arn

  input = <<INPUT
{"Action": "Start"}
INPUT
}

resource "aws_cloudwatch_event_target" "this_stop" {
  rule = aws_cloudwatch_event_rule.this_stop.name
  arn  = aws_lambda_function.this.arn

  input = <<INPUT
{"Action": "Stop"}
INPUT
}

resource "aws_cloudwatch_log_group" "this" {
  name              = format("%s%s", "/aws/lambda/", aws_lambda_function.this.function_name)
  retention_in_days = 30
}
