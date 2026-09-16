# CampaignIQ — Marketing Campaign Optimizer

> End-to-end marketing experimentation and A/B testing analytics platform built with Python, SQL, SQLite, statistical analysis, Streamlit, and Power BI.

---

## 📌 Overview

**CampaignIQ** is an end-to-end marketing experimentation platform designed to evaluate A/B tests using statistical evidence rather than relying only on observed conversion-rate differences.

The project combines:

- Data ingestion and validation
- Exploratory data analysis
- SQL-based analytical modeling
- Two-proportion statistical testing
- Confidence intervals
- Relative lift analysis
- Power and sample-size calculations
- Automated experiment verdicts
- Simulated marketing campaigns
- Streamlit experimentation application
- Power BI executive dashboard
- Independent statistical validation

The platform analyzes real A/B testing datasets and generates a portfolio of **40 simulated marketing campaigns** across multiple channels.

---

# 🎯 Business Problem

Marketing teams frequently run experiments to determine whether a new campaign or treatment improves customer conversion.

A higher treatment conversion rate does not automatically mean the treatment produced a reliable improvement.

For example:

```text
Control Conversion Rate    = 2.00%
Treatment Conversion Rate  = 2.20%
```

The treatment appears better based on the observed rate, but we still need to ask:

- Is the difference statistically significant?
- How large is the effect?
- What is the confidence interval?
- Was the experiment sufficiently powered?
- How many users were required?
- Can the result be considered reliable?

CampaignIQ addresses these questions through an end-to-end experimentation workflow.

---

# 🚀 Key Features

- End-to-end A/B testing workflow
- Data ingestion and validation
- Exploratory data analysis
- Conversion-rate analysis
- Two-proportion z-test
- P-value calculation
- Confidence intervals
- Absolute difference
- Relative lift
- Statistical significance classification
- Power analysis
- Sample-size calculation
- Automated experiment verdict engine
- 40 simulated campaigns
- 400,000 simulated experiment records
- SQLite analytical source of truth
- SQL analytical queries
- Interactive Streamlit application
- Custom CSV experiment upload
- Experiment planner
- Power BI executive dashboard
- Independent production-engine validation

---

# 🏗️ Solution Architecture

```text
                         ┌──────────────────────────┐
                         │        RAW DATA          │
                         │                          │
                         │ Marketing A/B Testing    │
                         │ Cookie Cats              │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │     DATA INGESTION        │
                         │          Python           │
                         │                          │
                         │ Validation               │
                         │ Cleaning                 │
                         │ Transformation           │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │     PROCESSED DATA       │
                         │           CSV            │
                         └────────────┬─────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
                    ▼                                   ▼
          ┌──────────────────────┐             ┌──────────────────────┐
          │    SQLite Database   │             │    EDA Notebooks     │
          │                      │             │                      │
          │ marketing_ab         │             │ Distribution         │
          │ cookie_cats          │             │ Conversion           │
          │ campaigns            │             │ Retention            │
          │ experiment_results   │             │ Statistical Analysis │
          └──────────┬───────────┘             └──────────────────────┘
                     │
                     ▼
          ┌──────────────────────────────┐
          │      STATISTICAL ENGINE      │
          │                              │
          │ Two-Proportion Z-Test        │
          │ Confidence Intervals         │
          │ Relative Lift                │
          │ Power Analysis               │
          │ Sample Size Calculation      │
          │ Verdict Engine               │
          └──────────────┬───────────────┘
                         │
                ┌────────┴────────┐
                │                 │
                ▼                 ▼
      ┌────────────────────┐  ┌──────────────────────┐
      │    Streamlit App   │  │   Power BI Dashboard │
      │                    │  │                      │
      │ Campaign Analysis  │  │ Experiment Overview  │
      │ CSV Upload         │  │ Campaign Performance │
      │ A/B Testing        │  │ Channel Performance  │
      │ Experiment Planner │  │                      │
      └────────────────────┘  └──────────────────────┘
```

---

# 📊 Datasets

## 1. Marketing A/B Testing Dataset

The Marketing A/B Testing dataset contains user-level advertising experiment data.

### Dataset size

```text
588,101 users
```

### Columns

| Column | Description |
|---|---|
| `user_id` | Unique user identifier |
| `test_group` | Control or treatment group |
| `converted` | Whether the user converted |
| `total_ads` | Number of advertisements shown |
| `most_ads_day` | Day with the highest ad exposure |
| `most_ads_hour` | Hour with the highest ad exposure |

---

## 2. Cookie Cats Dataset

The Cookie Cats dataset is used as an independent validation dataset for the statistical testing engine.

### Dataset size

```text
90,189 users
```

### Columns

| Column | Description |
|---|---|
| `userid` | Unique user identifier |
| `version` | Experiment variant |
| `sum_gamerounds` | Number of game rounds |
| `retention_1` | Day-1 retention |
| `retention_7` | Day-7 retention |

---

## 3. Simulated Campaign Dataset

CampaignIQ generates simulated experiments to demonstrate campaign-level experimentation across multiple marketing channels.

### Campaigns

```text
40 campaigns
```

### Users per campaign

```text
5,000 Control
5,000 Treatment
```

### Total simulated records

```text
400,000
```

### Marketing channels

```text
Email
Social Media
Search
Display
Push Notification
SMS
In-App
Website
Referral
Loyalty
```

---

# 🧪 Statistical Methodology

CampaignIQ uses statistical testing to determine whether observed differences between experiment groups are supported by sufficient evidence.

---

## 1. Conversion Rate

```text
Conversion Rate = Conversions / Total Users
```

---

## 2. Absolute Difference

```text
Absolute Difference =
Treatment Rate - Control Rate
```

---

## 3. Relative Lift

```text
Relative Lift =
(Treatment Rate - Control Rate) / Control Rate
```

Example:

```text
Control  = 2.00%
Treatment = 2.40%

Relative Lift =
(2.40% - 2.00%) / 2.00%

= +20%
```

---

# 📐 Hypothesis Testing

CampaignIQ uses a **two-proportion z-test** for binary conversion and retention metrics.

### Null Hypothesis

```text
H₀:
Treatment conversion rate = Control conversion rate
```

### Alternative Hypothesis

```text
H₁:
Treatment conversion rate ≠ Control conversion rate
```

### Default significance level

```text
α = 0.05
```

The statistical engine reports:

- Z-statistic
- P-value
- Statistical significance
- Treatment rate
- Control rate
- Absolute difference
- Relative lift
- Confidence interval

---

# 📊 Confidence Intervals

CampaignIQ calculates a 95% confidence interval for the difference between treatment and control proportions.

The output includes:

```text
CI Lower Bound
CI Upper Bound
```

Confidence intervals provide additional context about uncertainty around the observed treatment effect.

---

# ⚡ Power & Sample Size Analysis

Statistical significance alone is not enough.

An experiment may fail to detect an effect because the sample size is insufficient.

CampaignIQ therefore performs power analysis using:

```text
Alpha       = 0.05
Power       = 0.80
Relative MDE = 20%
```

The power calculator determines:

```text
Required sample size per group
Required total sample size
```

The platform compares the required sample size with the actual experiment size.

---

# 🧠 Automated Verdict Engine

The verdict engine evaluates:

```text
P-value
+
Observed Treatment Effect
+
Confidence Interval
+
Actual Sample Size
+
Required Sample Size
```

The system can classify results as:

```text
Statistically Significant Positive
Statistically Significant Negative
Not Statistically Significant
Underpowered
```

A non-significant result is **not automatically treated as proof that treatment and control are identical**.

---

# 📈 Marketing A/B Testing Results

The Marketing A/B Testing dataset produced:

```text
Control Conversion Rate
1.7854%

Treatment Conversion Rate
2.5547%

Absolute Difference
+0.7692 percentage points

Relative Lift
+43.09%

P-value
1.705281e-13

95% Confidence Interval
[+0.5951 pp, +0.9434 pp]
```

The observed difference was statistically significant under the configured 5% significance level.

---

# 🍪 Statistical Validation — Cookie Cats

The production statistical engine was independently validated against the Cookie Cats experiment.

## Day-1 Retention

```text
Control Rate:
44.8188%

Treatment Rate:
44.2283%

P-value:
0.0744096553

95% Confidence Interval:
[-1.2392%, +0.0582%]
```

Production validation:

```text
PASS
```

---

## Day-7 Retention

```text
Control Rate:
19.0201%

Treatment Rate:
18.2000%

P-value:
0.0015542500

95% Confidence Interval:
[-1.3282%, -0.3121%]
```

Production validation:

```text
PASS
```

### Validation conclusion

```text
Day-1 Production Validation: PASS
Day-7 Production Validation: PASS
Production Engine Validation: PASS
```

The notebook calculations and production statistical engine produced matching results.

---

# 🗄️ SQLite Analytical Layer

SQLite acts as the analytical source of truth for the application and experiment results.

## Database

```text
db/marketing_campaign_optimizer.db
```

## Tables

```text
marketing_ab
cookie_cats
campaigns
experiment_results
```

---

## `experiment_results`

The experiment results table stores statistical outputs including:

```text
result_id
campaign_id
metric_name
control_rate
treatment_rate
absolute_difference
relative_lift
p_value
alpha
ci_low
ci_high
sample_size
required_sample_size
statistically_significant
decision
created_at
```

This creates a shared analytical layer for the Streamlit application and Power BI reporting.

---

# 🧮 Simulated Experiment Portfolio

The project generates:

```text
40 campaigns
400,000 experiment records
```

Each campaign contains:

```text
5,000 Control Users
5,000 Treatment Users
```

The simulated campaigns span:

```text
Email
Social Media
Search
Display
Push Notification
SMS
In-App
Website
Referral
Loyalty
```

---

# 🖥️ Streamlit Application

CampaignIQ includes an interactive Streamlit application.

## Features

### Existing Campaign Analysis

Users can select an existing campaign and view:

```text
Control Conversion
Treatment Conversion
Absolute Difference
Relative Lift
P-value
Confidence Interval
Statistical Significance
Sample Adequacy
Experiment Interpretation
```

### CSV Upload

Users can upload their own experiment data.

Required columns:

```text
user_id
test_group
converted
```

Example:

```csv
user_id,test_group,converted
1,control,0
2,control,1
3,control,0
4,control,0
5,control,1
6,treatment,1
7,treatment,1
8,treatment,0
9,treatment,1
10,treatment,1
```

The application automatically analyzes the uploaded experiment.

---

# 📊 Power BI Dashboard

The project contains a three-page Power BI dashboard.

---

## Page 1 — Experiment Overview

Provides a portfolio-level view of the experimentation program.

### KPIs

```text
Total Campaigns
40

Total Experiment Results
40

Significant Results
10

Underpowered Experiments
40
```

### Visualizations

- Campaign relative lift
- Statistical significance distribution
- Sample adequacy distribution
- Channel-level relative lift
- Experiment evidence table
- Campaign filtering

---

## Page 2 — Campaign Performance

Provides detailed campaign-level analysis.

Users can select a campaign and analyze:

```text
Control Conversion
Treatment Conversion
Relative Lift
P-value
Confidence Interval
Statistical Significance
Sample Adequacy
```

The page allows campaign-level investigation rather than only portfolio-level reporting.

---

## Page 3 — Channel Performance

Provides channel-level experimentation analysis.

### Channels

```text
Email
Social Media
Search
Display
Push Notification
SMS
In-App
Website
Referral
Loyalty
```

The page includes:

- Observed relative lift by channel
- Campaign count by channel
- Channel experiment summary
- Channel filtering

---

# 📁 Project Structure

```text
marketing_campaign_optimizer/
│
├── data/
│   ├── raw/
│   │   ├── cookie_cats.csv
│   │   └── marketing_AB.csv
│   │
│   └── processed/
│       ├── cookie_cats_processed.csv
│       ├── marketing_ab_processed.csv
│       └── simulated_campaigns.csv
│
├── db/
│   └── marketing_campaign_optimizer.db
│
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_eda_analysis.ipynb
│   └── 03_validation_report.ipynb
│
├── scripts/
│   ├── campaign_simulator.py
│   ├── significance_test.py
│   ├── power_calculator.py
│   ├── verdict_engine.py
│   ├── load_database.py
│   └── generate_experiment_results.py
│
├── sql/
│   ├── schema.sql
│   └── queries.sql
│
├── app/
│   └── app.py
│
├── dashboard/
│   └── campaign_optimizer_dashboard.pbix
│
├── reports/
│   ├── Final_Report.pdf
│   └── Presentation.pptx
│
├── requirements.txt
└── README.md
```

---

# 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Programming | Python |
| Data Analysis | Pandas, NumPy |
| Statistics | SciPy, Statsmodels |
| Machine Learning Utilities | Scikit-learn |
| Visualization | Matplotlib, Seaborn, Plotly |
| Database | SQLite |
| Query Language | SQL |
| Application | Streamlit |
| Business Intelligence | Power BI |
| BI Calculations | DAX |
| Notebook Environment | Jupyter Notebook |
| IDE | VS Code |
| Version Control | Git / GitHub |
| Operating System | Windows 11 |

---

# ⚙️ Installation

## Prerequisites

Install:

```text
Python 3.14+
VS Code
Git
PowerShell
```

---

## 1. Clone the repository

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd marketing_campaign_optimizer
```

---

## 2. Create a virtual environment

```powershell
python -m venv .venv
```

---

## 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 4. Install dependencies

```powershell
pip install -r requirements.txt
```

---

# ▶️ Running the Project

## Step 1 — Data Ingestion

Start Jupyter:

```powershell
jupyter notebook
```

Open:

```text
notebooks/01_data_ingestion.ipynb
```

Run all cells.

This performs:

- Schema validation
- Missing-value validation
- Duplicate validation
- Value validation
- Data cleaning
- Column standardization
- Processed-data generation

---

## Step 2 — Exploratory Data Analysis

Open:

```text
notebooks/02_eda_analysis.ipynb
```

Run all cells.

The notebook analyzes:

- Group sizes
- Conversion rates
- Retention rates
- Distribution of ad exposure
- Game-round distributions
- Conversion by day
- Conversion by exposure
- Statistical differences
- Confidence intervals

---

## Step 3 — Generate Simulated Campaigns

From PowerShell:

```powershell
python scripts\campaign_simulator.py
```

This generates:

```text
data\processed\simulated_campaigns.csv
```

with:

```text
40 campaigns
400,000 records
```

---

## Step 4 — Build SQLite Database

Run:

```powershell
python scripts\load_database.py
```

This loads:

```text
Marketing A/B Testing
Cookie Cats
Simulated Campaigns
```

into:

```text
db\marketing_campaign_optimizer.db
```

---

## Step 5 — Generate Experiment Results

Run:

```powershell
python scripts\generate_experiment_results.py
```

This calculates experiment-level statistics and stores them in:

```text
experiment_results
```

---

## Step 6 — Validate the Statistical Engine

Open:

```text
notebooks/03_validation_report.ipynb
```

Run all cells.

Expected:

```text
Production Engine Validation: PASS
```

---

## Step 7 — Launch Streamlit

From PowerShell:

```powershell
streamlit run app\app.py
```

The application will open in your browser.

---

# 📋 Example Experiment Result

Example campaign output:

```text
Campaign:
Campaign 1

Control Conversion:
2.32%

Treatment Conversion:
2.40%

Absolute Difference:
+0.08 percentage points

Relative Lift:
+3.45%

P-value:
0.792161

95% CI:
[-0.52 pp, +0.68 pp]

Statistical Significance:
Not Significant

Sample Status:
Underpowered
```

This demonstrates why CampaignIQ evaluates more than the observed conversion-rate difference.

---

# 🔬 Experimentation Principles

## 1. Observed Lift ≠ Statistical Significance

A treatment can have a higher conversion rate without providing sufficient statistical evidence that the difference is real.

---

## 2. Statistical Significance ≠ Practical Significance

A statistically significant difference should still be evaluated in the context of the actual effect size and business objective.

---

## 3. Non-Significance Does Not Prove Equality

Failing to reject the null hypothesis does not prove that the treatment and control groups are identical.

---

## 4. Sample Size Matters

An experiment with insufficient observations may not have enough power to detect the intended minimum detectable effect.

---

## 5. Confidence Intervals Add Context

Confidence intervals provide information about uncertainty surrounding the observed treatment effect.

---

# 📈 Project Results Summary

```text
Marketing A/B Testing Users
588,101

Cookie Cats Users
90,189

Simulated Campaigns
40

Simulated Experiment Records
400,000

Experiment Results
40

Statistically Significant Results
10

Underpowered Experiments
40
```

---

# 💡 Key Analytical Insights

### Marketing A/B Testing

The treatment group showed:

```text
+43.09% relative lift
```

with a statistically significant difference under the configured 5% significance level.

---

### Cookie Cats

Day-1 retention:

```text
p = 0.0744096553
```

Day-7 retention:

```text
p = 0.0015542500
```

The production statistical engine reproduced both results successfully.

---

### Simulated Campaign Portfolio

The 40 simulated campaigns demonstrate how an experimentation system can evaluate campaign results at scale while tracking both:

```text
Experiment performance
+
Sample adequacy
```

---

# 🧩 Design Decisions

## SQLite as Source of Truth

SQLite was selected as the analytical source of truth so that:

- SQL queries
- Streamlit
- Statistical scripts
- Experiment results

can work from a consistent analytical layer.

---

## Separate Statistical Modules

Statistical functionality is separated into reusable modules:

```text
significance_test.py
power_calculator.py
verdict_engine.py
```

This makes the statistical engine easier to test, maintain, and reuse.

---

## Independent Validation

The production statistical engine is validated against the Cookie Cats experiment rather than relying only on internally generated simulated data.

This helps validate:

- Treatment/control ordering
- P-value calculation
- Confidence intervals
- Statistical decisions

---

# 🚀 Future Enhancements

Potential future improvements include:

- Bayesian A/B testing
- Sequential testing
- CUPED variance reduction
- Multi-armed bandits
- Automated experiment monitoring
- Automated data refresh
- Revenue-based experimentation metrics
- Customer segmentation
- Experiment history tracking
- Cloud database integration
- Cloud deployment
- Automated reporting
- Multiple-testing correction workflows
- Experiment anomaly detection

---

# 📸 Dashboard Screenshots

Add screenshots to a `docs/` folder:

```text
docs/
├── experiment_overview.png
├── campaign_performance.png
├── channel_performance.png
└── streamlit_app.png
```

Then add them to this README:

```markdown
## Experiment Overview

![Experiment Overview](docs/experiment_overview.png)

## Campaign Performance

![Campaign Performance](docs/campaign_performance.png)

## Channel Performance

![Channel Performance](docs/channel_performance.png)

## Streamlit Application

![CampaignIQ Streamlit Application](docs/streamlit_app.png)
```

---

# 🎥 Demo

Add your Streamlit or dashboard demo link here:

```markdown
[Watch CampaignIQ Demo](YOUR_DEMO_LINK)
```

---

# 📚 Project Deliverables

```text
✓ Data ingestion pipeline
✓ Data validation
✓ EDA notebooks
✓ Statistical testing engine
✓ Confidence interval calculation
✓ Power/sample-size calculator
✓ Automated verdict engine
✓ Campaign simulator
✓ SQLite analytical database
✓ SQL analytical queries
✓ Streamlit application
✓ CSV upload functionality
✓ Power BI dashboard
✓ Statistical validation notebook
✓ Final project report
✓ Project presentation
```

---

# 👤 Author

## Thanuj Vummidi

Aspiring Data Analyst / Data Engineer

### Technical Interests

```text
Python
SQL
Data Analytics
Data Engineering
A/B Testing
Statistical Analysis
Power BI
Microsoft Fabric
Cloud Data Engineering
```

---

# ⭐ Project Summary

CampaignIQ demonstrates an end-to-end experimentation workflow:

```text
RAW DATA
   ↓
DATA CLEANING
   ↓
EDA
   ↓
SQL DATABASE
   ↓
STATISTICAL TESTING
   ↓
POWER ANALYSIS
   ↓
CONFIDENCE INTERVALS
   ↓
VERDICT ENGINE
   ↓
STREAMLIT APPLICATION
   ↓
POWER BI DASHBOARD
```

The project demonstrates how raw marketing experiment data can be transformed into a complete analytics solution combining:

**Data Engineering + Statistical Analysis + Business Intelligence + Application Development.**

---

## Final Workflow

```text
Data
  ↓
Validate
  ↓
Clean
  ↓
Analyze
  ↓
Store in SQLite
  ↓
Run A/B Tests
  ↓
Calculate Power
  ↓
Generate Experiment Results
  ↓
Validate Statistical Engine
  ↓
Streamlit
  ↓
Power BI
```

CampaignIQ is designed to demonstrate practical experimentation analytics rather than simply reporting which campaign has the highest conversion rate.

The platform combines:

```text
Observed Effect
+
Statistical Evidence
+
Confidence Intervals
+
Power Analysis
+
Sample Adequacy
```

to provide a comprehensive view of marketing experiment results.
