resource "aws_iam_policy" "this" {
  name        = module.label.id
  description = module.label.id
  policy      = data.aws_iam_policy_document.policy.json
}

data "aws_iam_policy_document" "policy" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:DescribeLogGroups",
      "logs:DescribeLogStreams",
    ]

    effect    = "Allow"
    resources = ["arn:aws:logs:*:*:*"]
  }
}

resource "aws_iam_role" "this" {
  name               = module.label.id
  description        = module.label.id
  assume_role_policy = data.aws_iam_policy_document.role.json
}

data "aws_iam_policy_document" "role" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "this" {
  role       = aws_iam_role.this.name
  policy_arn = aws_iam_policy.this.arn
}
