---
name: databricks-cloud
summary: Databricks — the unified data analytics platform born from the Apache Spark creators, bridging data engineering, science, and AI on cloud infrastructure.
read_when:
  - Exploring the evolution from batch processing to lakehouse architecture
  - Understanding how Apache Spark's creators monetized their open-source project
  - Researching cloud-native data platforms and their competitive moats
  - Analyzing the data warehousing vs. data lakehouse market shift
  - Studying startup-to-IPO journeys in the enterprise data infrastructure space
---

# Databricks

## 历史时间线
- **2013**: 由Apache Spark创始人Matei Zaharia及UC Berkeley AMPLab团队成员在旧金山创立，初始愿景是让Spark在企业中更易用
- **2014**: 发布首个托管Spark服务，定位为"Spark as a Service"，解决企业自行部署Spark集群的运维痛点
- **2016**: 推出Databricks Delta（后更名为Delta Lake），引入ACID事务到数据湖，解决数据湖的可靠性问题
- **2019**: 发布Delta Lake开源版本，同时推出MLflow实验管理工具，构建完整MLOps生态
- **2021**: 提出"Lakehouse"架构概念，融合数据仓库的结构化查询能力与数据湖的灵活性
- **2022**: 收购8080 Labs（munity.ai），推出DBRX大语言模型训练基础设施
- **2023**: 发布Unity Catalog实现跨工作区统一治理，估值达430亿美元，提交IPO申请
- **2024**: Databricks IQ（AI助手）和Lakeflow产品发布，年经常性收入突破20亿美元

## 商业模式
Databricks采用consumption-based pricing（按消耗付费）的云SaaS模式。客户在AWS/Azure/GCP上运行Databricks工作区，按DBU（Databricks Unit）计费。收入来自两部分：DBU消耗费用（支付给Databricks）和底层云基础设施费用（支付给云厂商）。这种模式与云厂商深度绑定，形成共生关系——云厂商获得IaaS收入，Databricks获得平台收入。企业版还包含高级安全治理、实时协作和专属支持。

## 护城河分析
**技术护城河**: Delta Lake格式已成为行业事实标准，一旦被企业采用，迁移成本极高。Spark生态系统的深度优化让Databricks在大规模数据处理上保持性能优势。
**网络效应**: Notebook协作环境形成团队粘性，数据工程师、科学家和分析师在同一平台上协作，替换意味着整个团队工作流重建。
**生态壁垒**: MLflow、Delta Sharing、Unity Catalog构成完整的data+AI工具链，竞争者很难在单一产品线上同时匹敌。
**云伙伴关系**: 与AWS、Azure、GCP的marketplace集成降低了采购门槛，三大云厂商均将其作为首选数据平台推荐。

## 关键数据
- 估值: ~430亿美元（2023年最后一轮）
- ARR: 超过20亿美元（2024年）
- 客户数: 超过10,000家企业客户
- 员工数: 约5,000人
- 融资总额: 超过35亿美元
- 核心产品: Data Engineering, Data Warehousing, Machine Learning, AI/LLM

## 有趣事实
Databricks的创始人团队几乎就是Apache Spark的原作者。他们最初在伯克利的一个研究项目中创造了Spark，后来意识到企业需要托管服务才能真正释放其价值。有趣的是，他们选择"湖仓一体"这个概念，本质上是在说"为什么要在数据仓库和数据湖之间做选择？"——这直接挑战了Snowflake等纯仓库厂商的定位。
