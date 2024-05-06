resource "aws_s3_bucket" "ctw03643-bucket" {
  bucket = "${var.project_name}-${var.identifier}"
}

resource "aws_s3_bucket_object" "ctw03643-files" {
  #for_each = { for file in local.files_to_upload : file => file }

  for_each = fileset("samples/", "*")
  bucket = aws_s3_bucket.ctw03643-bucket.id
  key    = "samples/${each.value}"
  source = "samples/${each.value}"
  etag = filemd5("samples/${each.value}")
}

resource "aws_lambda_function" "ctw03643-lambda" {
  source_code_hash = data.archive_file.python_lambda_package.output_path
  role             = aws_iam_role.lambda_role.arn
  filename      = "code/function.zip"
  function_name = "lambda-${var.project_name}-${var.identifier}"
  handler       = "function-lambda_handler"
  runtime = "python3.12"
}

data "archive_file" "python_lambda_package" {
  type             = "zip"
  source_file      = "code/function.py"
  output_path      = "code/function.zip"
}