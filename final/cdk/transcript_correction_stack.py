from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_lambda_python_alpha as lambda_python,  # AWS CDKのPython Lambdaレイヤー用（別途alphaモジュール必要）
)
from constructs import Construct
import os

class TranscriptCorrectionStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Lambda Layer（依存関係 FastAPIなど）
        lambda_layer = _lambda.LayerVersion(
            self, "LambdaLayer",
            code=_lambda.Code.from_asset(os.path.join("..", "lambda_layer", "python")),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9, _lambda.Runtime.PYTHON_3_10],
            description="Layer for FastAPI dependencies",
        )

        # Lambda関数
        lambda_function = _lambda.Function(
            self, "TranscriptCorrectionFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="main.handler",  # main.py の最後にある handler = Mangum(app)
            code=_lambda.Code.from_asset(os.path.join("..", "lambda")),
            layers=[lambda_layer],
            memory_size=1024,
            timeout=cdk.Duration.seconds(30),
            environment={
                "AWS_REGION": self.region,
            },
        )

        # API Gateway REST API + Lambdaプロキシ統合
        api = apigw.LambdaRestApi(
            self, "TranscriptCorrectionApi",
            handler=lambda_function,
            proxy=True,
            rest_api_name="TranscriptCorrectionService",
            description="API Gateway for transcript correction Lambda",
        )
