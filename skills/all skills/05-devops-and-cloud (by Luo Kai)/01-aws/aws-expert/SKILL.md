---
author: luo-kai
name: aws-expert
description: Expert-level AWS cloud development. Use when working with EC2, S3, Lambda, RDS, DynamoDB, ECS, API Gateway, CloudFront, SQS, SNS, IAM, CDK, or CloudFormation. Also use when the user mentions 'Lambda', 'S3 bucket', 'IAM role', 'CDK', 'CloudFormation', 'DynamoDB', 'ECS', 'VPC', 'API Gateway', 'cost optimization', or any AWS service name.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# AWS Expert

You are an expert AWS cloud architect and developer with hands-on experience across the full AWS service catalog and production deployments at scale.

## Before Starting

1. **Service in question** — specific AWS service or general architecture?
2. **Architecture pattern** — serverless, containers (ECS/EKS), EC2, or hybrid?
3. **Scale** — requests/day, data volume, concurrent users?
4. **IaC tool** — CDK, CloudFormation, Terraform, SAM?
5. **Existing infrastructure** — greenfield or existing AWS account?

---

## Core Expertise Areas

- **Compute**: EC2 (instance types, ASG, AMI, placement groups), Lambda (cold starts, layers, SnapStart), ECS/Fargate, App Runner
- **Storage**: S3 (storage classes, lifecycle, presigned URLs, multipart upload, event notifications), EBS, EFS
- **Database**: RDS Aurora (Multi-AZ, read replicas, Aurora Serverless v2), DynamoDB (single-table design, GSIs, streams), ElastiCache
- **Networking**: VPC (subnets, NACLs, SGs, flow logs), ALB/NLB, API Gateway, CloudFront, Route53, PrivateLink, Transit Gateway
- **Messaging**: SQS (standard vs FIFO, DLQ, visibility timeout), SNS (fan-out), EventBridge (rules, pipes, schedules), Kinesis
- **Security**: IAM (least privilege, roles, SCPs), KMS, Secrets Manager, WAF, GuardDuty, Security Hub, CloudTrail
- **IaC**: CDK (TypeScript/Python), CloudFormation, SAM, AWS Powertools
- **Cost optimization**: Savings Plans, Reserved Instances, Spot, Compute Optimizer, Cost Explorer

---

## Key Patterns & Code

### AWS CDK — Full Stack API
```typescript
import * as cdk from "aws-cdk-lib";
import {
  aws_lambda as lambda,
  aws_dynamodb as ddb,
  aws_apigateway as apigw,
  aws_sqs as sqs,
  aws_lambda_event_sources as sources,
  aws_iam as iam,
} from "aws-cdk-lib";
import { Construct } from "constructs";

export class ApiStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // DynamoDB table with best practices
    const table = new ddb.Table(this, "UsersTable", {
      tableName: `users-${props?.env?.account}-${props?.env?.region}`,
      partitionKey: { name: "pk", type: ddb.AttributeType.STRING },
      sortKey:      { name: "sk", type: ddb.AttributeType.STRING },
      billingMode:  ddb.BillingMode.PAY_PER_REQUEST,
      encryption:   ddb.TableEncryption.AWS_MANAGED,
      pointInTimeRecovery: true,
      removalPolicy: cdk.RemovalPolicy.RETAIN,
      stream: ddb.StreamViewType.NEW_AND_OLD_IMAGES,
    });

    // GSI for querying by email
    table.addGlobalSecondaryIndex({
      indexName: "email-index",
      partitionKey: { name: "email", type: ddb.AttributeType.STRING },
      projectionType: ddb.ProjectionType.ALL,
    });

    // Dead letter queue
    const dlq = new sqs.Queue(this, "DLQ", {
      retentionPeriod: cdk.Duration.days(14),
      encryption: sqs.QueueEncryption.KMS_MANAGED,
    });

    // Lambda function with best practices
    const apiHandler = new lambda.Function(this, "ApiHandler", {
      functionName: "users-api-handler",
      runtime: lambda.Runtime.NODEJS_20_X,
      handler: "index.handler",
      code: lambda.Code.fromAsset("lambda"),
      timeout: cdk.Duration.seconds(30),
      memorySize: 1024,
      environment: {
        TABLE_NAME: table.tableName,
        REGION: this.region,
        NODE_OPTIONS: "--enable-source-maps",
      },
      tracing: lambda.Tracing.ACTIVE,
      insightsVersion: lambda.LambdaInsightsVersion.VERSION_1_0_229_0,
      deadLetterQueue: dlq,
      retryAttempts: 2,
    });

    // Least privilege
    table.grantReadWriteData(apiHandler);

    // API Gateway with usage plan
    const api = new apigw.RestApi(this, "UsersApi", {
      restApiName: "Users API",
      description: "Users management API",
      deployOptions: {
        stageName: "prod",
        loggingLevel: apigw.MethodLoggingLevel.INFO,
        dataTraceEnabled: true,
        metricsEnabled: true,
        throttlingBurstLimit: 500,
        throttlingRateLimit: 1000,
      },
      defaultCorsPreflightOptions: {
        allowOrigins: apigw.Cors.ALL_ORIGINS,
        allowMethods: apigw.Cors.ALL_METHODS,
      },
    });

    const users = api.root.addResource("users");
    users.addMethod("GET",  new apigw.LambdaIntegration(apiHandler));
    users.addMethod("POST", new apigw.LambdaIntegration(apiHandler));

    const user = users.addResource("{id}");
    user.addMethod("GET",    new apigw.LambdaIntegration(apiHandler));
    user.addMethod("PUT",    new apigw.LambdaIntegration(apiHandler));
    user.addMethod("DELETE", new apigw.LambdaIntegration(apiHandler));

    // Outputs
    new cdk.CfnOutput(this, "ApiUrl", { value: api.url });
    new cdk.CfnOutput(this, "TableName", { value: table.tableName });
  }
}
```

### Lambda Handler — Best Practices
```typescript
import { APIGatewayProxyHandler } from "aws-lambda";
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, GetCommand, PutCommand } from "@aws-sdk/lib-dynamodb";
import { Logger } from "@aws-lambda-powertools/logger";
import { Tracer } from "@aws-lambda-powertools/tracer";
import { Metrics, MetricUnits } from "@aws-lambda-powertools/metrics";

// Initialize outside handler — reused across warm invocations
const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);
const logger = new Logger({ serviceName: "users-api" });
const tracer = new Tracer({ serviceName: "users-api" });
const metrics = new Metrics({ namespace: "UsersApi", serviceName: "users-api" });

export const handler: APIGatewayProxyHandler = async (event, context) => {
  logger.addContext(context);
  logger.info("Request received", { path: event.path, method: event.httpMethod });

  try {
    const { httpMethod, pathParameters } = event;

    if (httpMethod === "GET" && pathParameters?.id) {
      const result = await docClient.send(new GetCommand({
        TableName: process.env.TABLE_NAME!,
        Key: {
          pk: `USER#${pathParameters.id}`,
          sk: "PROFILE",
        },
      }));

      if (!result.Item) {
        return {
          statusCode: 404,
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ error: "User not found" }),
        };
      }

      metrics.addMetric("UserFetched", MetricUnits.Count, 1);

      return {
        statusCode: 200,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(result.Item),
      };
    }

    return {
      statusCode: 405,
      body: JSON.stringify({ error: "Method not allowed" }),
    };

  } catch (error) {
    logger.error("Handler error", { error });
    metrics.addMetric("Errors", MetricUnits.Count, 1);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Internal server error" }),
    };
  } finally {
    metrics.publishStoredMetrics();
  }
};
```

### DynamoDB Single-Table Design
```typescript
import { DynamoDBDocumentClient, QueryCommand, TransactWriteCommand } from "@aws-sdk/lib-dynamodb";

// Access patterns drive the entire schema design
//
// Entity     PK              SK                GSI1PK          GSI1SK
// User       USER#<id>       PROFILE           EMAIL#<email>   USER#<id>
// Order      USER#<userId>   ORDER#<orderId>   ORDER#<id>      USER#<userId>
// Product    PRODUCT#<id>    METADATA          -               -

const docClient = DynamoDBDocumentClient.from(new DynamoDBClient({}));
const TABLE = process.env.TABLE_NAME!;

// Get user + all their orders in a single query
async function getUserWithOrders(userId: string) {
  const result = await docClient.send(new QueryCommand({
    TableName: TABLE,
    KeyConditionExpression: "pk = :pk",
    ExpressionAttributeValues: { ":pk": `USER#${userId}` },
  }));

  const items = result.Items ?? [];
  const profile = items.find(i => i.sk === "PROFILE");
  const orders  = items.filter(i => i.sk.startsWith("ORDER#"));
  return { profile, orders };
}

// Query by email using GSI
async function getUserByEmail(email: string) {
  const result = await docClient.send(new QueryCommand({
    TableName: TABLE,
    IndexName: "email-index",
    KeyConditionExpression: "email = :email",
    ExpressionAttributeValues: { ":email": email },
    Limit: 1,
  }));
  return result.Items?.[0] ?? null;
}

// Atomic transaction — create order + decrement stock
async function createOrder(userId: string, productId: string, quantity: number) {
  const orderId = crypto.randomUUID();
  await docClient.send(new TransactWriteCommand({
    TransactItems: [
      {
        Put: {
          TableName: TABLE,
          Item: {
            pk: `USER#${userId}`,
            sk: `ORDER#${orderId}`,
            orderId,
            productId,
            quantity,
            status: "pending",
            createdAt: new Date().toISOString(),
          },
          ConditionExpression: "attribute_not_exists(pk)",
        },
      },
      {
        Update: {
          TableName: TABLE,
          Key: { pk: `PRODUCT#${productId}`, sk: "METADATA" },
          UpdateExpression: "SET stock = stock - :qty",
          ConditionExpression: "stock >= :qty",
          ExpressionAttributeValues: { ":qty": quantity },
        },
      },
    ],
  }));
  return orderId;
}
```

### S3 Patterns
```typescript
import {
  S3Client,
  PutObjectCommand,
  GetObjectCommand,
  DeleteObjectCommand,
  ListObjectsV2Command,
} from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const s3 = new S3Client({ region: process.env.AWS_REGION });
const BUCKET = process.env.BUCKET_NAME!;

// Generate presigned upload URL (user uploads directly to S3)
async function getUploadUrl(userId: string, filename: string, contentType: string) {
  const key = `uploads/${userId}/${Date.now()}-${filename}`;
  const url = await getSignedUrl(
    s3,
    new PutObjectCommand({
      Bucket: BUCKET,
      Key: key,
      ContentType: contentType,
      Metadata: { uploadedBy: userId },
    }),
    { expiresIn: 900 } // 15 minutes
  );
  return { url, key };
}

// Generate presigned download URL
async function getDownloadUrl(key: string) {
  return getSignedUrl(
    s3,
    new GetObjectCommand({ Bucket: BUCKET, Key: key }),
    { expiresIn: 3600 } // 1 hour
  );
}

// Stream large file download
async function streamFile(key: string) {
  const response = await s3.send(
    new GetObjectCommand({ Bucket: BUCKET, Key: key })
  );
  return response.Body; // ReadableStream
}
```

### SQS + Lambda Event Processing
```typescript
import { SQSHandler, SQSRecord } from "aws-lambda";
import { SQSClient, DeleteMessageBatchCommand } from "@aws-sdk/client-sqs";

export const handler: SQSHandler = async (event) => {
  const results = await Promise.allSettled(
    event.Records.map(record => processRecord(record))
  );

  // Report partial batch failures
  // Lambda will retry only failed messages
  const failures = results
    .map((result, index) => ({ result, record: event.Records[index] }))
    .filter(({ result }) => result.status === "rejected")
    .map(({ record }) => ({ itemIdentifier: record.messageId }));

  return { batchItemFailures: failures };
};

async function processRecord(record: SQSRecord) {
  const body = JSON.parse(record.body);
  // process message...
  console.log("Processing:", body);
}
```

### IAM Least Privilege Policy
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DynamoDBAccess",
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem",
        "dynamodb:Query",
        "dynamodb:BatchGetItem",
        "dynamodb:BatchWriteItem"
      ],
      "Resource": [
        "arn:aws:dynamodb:us-east-1:123456789012:table/MyTable",
        "arn:aws:dynamodb:us-east-1:123456789012:table/MyTable/index/*"
      ]
    },
    {
      "Sid": "S3BucketAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/uploads/*"
    },
    {
      "Sid": "SecretsManagerAccess",
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": "arn:aws:secretsmanager:us-east-1:123456789012:secret:MyApp/*"
    }
  ]
}
```

### VPC Design — Production Pattern
```
┌─────────────────────────────────────────────────────┐
│  VPC: 10.0.0.0/16                                   │
│                                                     │
│  ┌──────────────────┐  ┌──────────────────┐         │
│  │ Public Subnet AZ1│  │ Public Subnet AZ2│         │
│  │   10.0.1.0/24    │  │   10.0.2.0/24    │         │
│  │  [ALB] [NAT GW]  │  │  [ALB] [NAT GW]  │         │
│  └────────┬─────────┘  └────────┬─────────┘         │
│           │                     │                   │
│  ┌────────▼─────────┐  ┌────────▼─────────┐         │
│  │ Private Subnet AZ1│  │ Private Subnet AZ2│        │
│  │   10.0.11.0/24   │  │   10.0.12.0/24   │         │
│  │  [ECS Tasks]     │  │  [ECS Tasks]     │         │
│  │  [Lambda in VPC] │  │  [Lambda in VPC] │         │
│  └────────┬─────────┘  └────────┬─────────┘         │
│           │                     │                   │
│  ┌────────▼─────────┐  ┌────────▼─────────┐         │
│  │ Database Subnet  │  │ Database Subnet  │         │
│  │  AZ1 10.0.21.0/24│  │  AZ2 10.0.22.0/24│         │
│  │  [RDS Primary]   │  │  [RDS Standby]   │         │
│  │  [ElastiCache]   │  │  [ElastiCache]   │         │
│  └──────────────────┘  └──────────────────┘         │
└─────────────────────────────────────────────────────┘
```

### Cost Optimization Checklist
```
Compute:
  ✓ Use Savings Plans for steady-state Lambda/Fargate (up to 17% savings)
  ✓ Reserved Instances for RDS (up to 60% savings)
  ✓ Spot Instances for batch/fault-tolerant workloads (up to 90% savings)
  ✓ Right-size Lambda memory (use AWS Compute Optimizer)
  ✓ Use ARM64 (Graviton) for Lambda/ECS (20% cheaper, 20% faster)

Storage:
  ✓ S3 Intelligent-Tiering for unpredictable access patterns
  ✓ S3 lifecycle policies: Standard → Standard-IA → Glacier
  ✓ Delete incomplete multipart uploads (lifecycle rule)
  ✓ EBS gp3 over gp2 (same performance, 20% cheaper)

Database:
  ✓ Aurora Serverless v2 for variable workloads
  ✓ DynamoDB on-demand for spiky traffic
  ✓ ElastiCache to reduce RDS read load
  ✓ Enable RDS storage autoscaling (avoid over-provisioning)

Networking:
  ✓ VPC endpoints for S3/DynamoDB (avoid NAT Gateway costs)
  ✓ CloudFront in front of ALB (reduce origin requests)
  ✓ Same-AZ traffic where possible (avoid cross-AZ data transfer)
```

---

## Best Practices

- Use IAM roles for all services — never embed access keys in code or environment variables
- Enable MFA on root account and all IAM users — enforce with SCP
- Tag ALL resources: `Environment`, `Team`, `CostCenter`, `Project`
- Enable CloudTrail, Config, and GuardDuty in every region from day one
- Use VPC endpoints for S3 and DynamoDB — keeps traffic off public internet and saves NAT costs
- Use AWS Organizations + SCPs for multi-account governance
- Set billing alerts at 50%, 80%, 100% of monthly budget
- Use AWS Lambda Powertools for structured logging, tracing, and metrics
- Use CDK for IaC — type safety, higher-level abstractions, easier to maintain than raw CloudFormation

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Using root account | Massive security risk | Use IAM Identity Center + MFA |
| Over-permissive IAM | Large blast radius on breach | Principle of least privilege always |
| Hardcoded credentials | Secret exposure in code/git | Use IAM roles + Secrets Manager |
| No VPC for compute | Services exposed to internet | Always deploy compute inside VPC |
| Lambda in VPC without endpoints | Slow cold starts, NAT costs | Add VPC endpoints for AWS services |
| Missing billing alerts | Unexpected huge bill | Set budget alerts on day one |
| Single region deployment | Regional outage = total downtime | Multi-region for critical workloads |
| No resource tagging | Cannot track costs per team/project | Enforce tags with SCP and Config rules |

---

## Related Skills

- **terraform-expert**: For multi-cloud IaC with Terraform
- **kubernetes-expert**: For EKS on AWS
- **cicd-expert**: For GitHub Actions deploying to AWS
- **serverless-expert**: For advanced Lambda patterns
- **docker-expert**: For ECS and ECR container deployments
- **monitoring-expert**: For CloudWatch, X-Ray, and AWS observability
