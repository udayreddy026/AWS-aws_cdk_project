from constructs import Construct
import aws_cdk as CDK
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)


class AwsCdkDemoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # queue = sqs.Queue(
        #     self, "Demo-Queue-20221214",
        #     visibility_timeout=Duration.seconds(300),
        # )

        # topic = sns.Topic(
        #     self, "Demo-Topic-20221214"
        # )

        # topic.add_subscription(subs.SqsSubscription(queue))

        # Creating Lambda Layer
        boto3_layer = _lambda.LayerVersion(self, "Boto3",
                                           code=_lambda.Code.from_asset(
                                               'layers/boto3'),
                                           compatible_runtimes=[
                                               _lambda.Runtime.PYTHON_3_8, _lambda.Runtime.PYTHON_3_9],
                                           compatible_architectures=[
                                               _lambda.Architecture.X86_64],
                                           description="Boto3 Common Lambda Layer.",
                                           )

        aws_xray_layer = _lambda.LayerVersion(self, "aws_xray",
                                              code=_lambda.Code.from_asset(
                                                  'layers/aws_xray'),
                                              compatible_runtimes=[
                                                  _lambda.Runtime.PYTHON_3_8, _lambda.Runtime.PYTHON_3_9],
                                              compatible_architectures=[
                                                  _lambda.Architecture.X86_64],
                                              description="AWS XRAY Lambda Layer.",
                                              )

        requests = _lambda.LayerVersion(self, "requests",
                                        code=_lambda.Code.from_asset(
                                            'layers/requests'),
                                        compatible_runtimes=[
                                            _lambda.Runtime.PYTHON_3_7, _lambda.Runtime.PYTHON_3_8, _lambda.Runtime.PYTHON_3_9],
                                        compatible_architectures=[
                                            _lambda.Architecture.ARM_64],
                                        description="Requests Lambda Layer.",
                                        )

        # Defines an AWS Lambda resource
        my_lambda = _lambda.Function(
            self, 'DemoLambda',
            function_name="Demo_lambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('src'),
            handler='hello.handler',
            tracing=_lambda.Tracing.ACTIVE,
            layers=[boto3_layer, aws_xray_layer, requests],
            description="Demo Lambda Function.",
            timeout=CDK.Duration.minutes(7)
        )

        # Creating API Endpoint
        apigw.LambdaRestApi(self, "/demo", handler=my_lambda)
