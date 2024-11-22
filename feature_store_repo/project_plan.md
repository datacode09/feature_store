### **Code Refactoring Plan (Using Updated Repository Architecture)**

---

### **1. Present State**

#### **Observations from Current Codebase:**
1. **Hardcoded Variables and Paths**:
   - Data paths, file names, and database connections are hardcoded.
2. **Tightly Coupled Logic**:
   - Feature engineering, data validation, logging, and Hive connection logic are embedded directly in the pipeline scripts.
3. **Lack of Centralized Metadata**:
   - No use of centralized metadata files to manage source-target systems, feature definitions, and linkages.
4. **Limited Modularity**:
   - Repeated implementations of Hive connections, validation, and logging utilities.
5. **Minimal Testing**:
   - Testing is ad hoc and directly embedded in the pipeline scripts.

---

### **2. Flaws of the Present State**

1. **High Maintenance Overhead**:
   - Adding or updating features requires changes in multiple places, increasing error risk.
2. **Scalability Issues**:
   - No support for centralized configuration or metadata-driven automation, making it difficult to manage multiple pipelines or datasets.
3. **Redundant Code**:
   - Repeated logic for pre-checks, status tracking, and Hive queries across scripts.
4. **Poor Testing and Debugging**:
   - Lack of structured tests makes it challenging to identify and fix bugs.

---

### **3. Future State**

#### **Vision:**
Refactor the codebase into a modular, scalable, and reusable repository using the updated architecture. Introduce metadata-driven pipelines and reusable utilities to automate feature engineering and streamline pipeline management.

---

### **4. Refactored Repository Architecture**

```plaintext
Refactored_repo/
├── metadata/                                  # Centralized metadata for features
│   ├── source_and_target_systems.yaml         # YAML file documenting source and target systems
│   ├── feature_definitions.yaml               # YAML file documenting all features
│   ├── linkage.yaml                           # YAML file detailing linkage for features
├── config/                                    # Configuration files for global and pipeline-specific variables
│   ├── global_config.sas                      # Defines global paths and variables
│   ├── pipeline_configs/                      # Defines pipeline-specific paths and variables
│   │   ├── customer_universe_pipeline_config.sas
│   │   ├── account_universe_pipeline_config.sas
│   │   ├── opacct_pipeline_config.sas
│   │   ├── financial_pipeline_config.sas
│   │   ├── term_and_revolver_pipeline_config.sas
├── utils/                         # Shared logic for all pipelines
│   ├── database_utils.sas         # Functions for connecting to sources and targets
│   ├── etl_precheck_utils.sas     # Utilities for pre-check before running ETL
│   ├── etl_status_utils.sas       # Utilities for status tracking of ETL jobs
│   ├── logger.sas                 # Functions for centralized logging
│   ├── validator.sas              # Functions for data validation
├── feature_materialization/   
│   ├── common_features.sas              # Common features shared across pipelines
│   ├── customer_universe_features.sas   # Feature logic for the customer_universe pipeline
│   ├── account_universe_features.sas    # Feature logic for the account_universe pipeline
│   ├── opacct_features.sas              # Feature logic for the opacct pipeline
│   ├── financial_features.sas           # Feature logic for the financial pipeline
│   ├── term_and_revolver_features.sas   # Feature logic for the term_and_revolver pipeline
├── pipelines/                      # Modularized pipelines for datasets
│   ├── customer_universe_pipeline/         
│   │   ├── customer_universe_pipeline.sas  # Main pipeline for the customer_universe dataset
│   ├── account_univers_pipeline/            
│   │   ├── account_univers_pipeline.sas     # Main pipeline for the account_universe dataset
│   ├── opacct_pipeline/     
│   │   ├── opacct_pipeline.sas              # Main pipeline for the opacct dataset
│   ├── financial_pipeline/            
│   │   ├── financial_pipeline.sas           # Main pipeline for the financial dataset
│   ├── term_and_revolver_pipeline/     
│   │   ├── term_and_revolver_pipeline.sas   # Main pipeline for the term_and_revolver dataset
├── adhoc_scripts/                 # Standalone scripts for feature management
│   ├── backfill_feature.sas       # Script to backfill specific features
│   ├── insert_new_feature.sas     # Script to insert new feature
│   └── manage_partitions.sas      # Script for partition management
├── tests/                         
│   ├── e2e_tests/
│   │   ├── test_customer_universe_pipeline.sas
│   ├── unit_tests/
├── docs/                         # Documentation
│   ├── feature_guide.md        # Human-readable feature catalog
│   ├── pipeline_guide.md         # Instructions for running pipelines
│   └── troubleshooting.md        # Common issues and solutions
├── README.md                     # Overview of the repository
```

---

### **5. Example Refactored Pipeline: Customer Universe**

#### **Metadata-Driven Pipeline Overview**
The refactored `customer_universe_pipeline` dynamically uses metadata and shared utilities for feature engineering and pipeline orchestration.

---

#### **Example Pipeline Script: `pipelines/customer_universe_pipeline/customer_universe_pipeline.sas`**

```sas
%include "../../utils/logger.sas";
%include "../../utils/database_utils.sas";
%include "../../utils/etl_precheck_utils.sas";
%include "../../utils/etl_status_utils.sas";
%include "../../utils/validator.sas";
%include "../../feature_materialization/customer_universe_features.sas";

/* Load Configurations */
%include "../../config/global_config.sas";
%include "../../config/pipeline_configs/customer_universe_pipeline_config.sas";

%log_message(Starting Customer Universe Pipeline);

/* Step 1: Pre-checks */
%log_message(Running ETL pre-checks);
%etl_precheck();

/* Step 2: Load Data from Source */
%log_message(Loading data from source systems);
%database_load(source_table=customer_data, target_table=work.customer_data);

/* Step 3: Generate Features */
%log_message(Generating features);
%materialize_customer_features(input_table=work.customer_data, output_table=work.customer_features);

/* Step 4: Validate Features */
%log_message(Validating features);
%validate_data(work.customer_features);

/* Step 5: Write to Target System */
%log_message(Writing features to target system);
%database_write(source_table=work.customer_features, target_table=customer_feature_table);

%log_message(Customer Universe Pipeline Completed Successfully);
```

Below are sample **ad hoc scripts** for common scenarios such as backfilling, adding new features, and managing Hive partitions. These scripts are designed to integrate with the proposed repository structure.

---

### **Backfill Script: `adhoc_scripts/backfill_feature.sas`**

**Purpose**: Recompute and backfill specific features for historical data in the `Opacct` dataset.

```sas
%include "../utils/logger.sas";
%include "../utils/database_utils.sas";
%include "../feature_materialization/opacct_features.sas";
%include "../config/global_config.sas";
%include "../config/pipeline_configs/opacct_pipeline_config.sas";

%let feature_list = total_transaction_value, average_monthly_balance;

/* Log start of backfill */
%log_message(Starting backfill for features: &feature_list.);

/* Step 1: Load historical data */
%log_message(Loading historical data from source table.);
%database_load(source_table=opacct_source_table, target_table=work.opacct_historical);

/* Step 2: Recompute features */
%log_message(Recomputing features for historical data.);
%materialize_opacct_features(input_table=work.opacct_historical, output_table=work.opacct_backfilled);

/* Step 3: Write backfilled features to target */
%log_message(Writing backfilled features to target table.);
%database_write(source_table=work.opacct_backfilled, target_table=opacct_feature_table);

/* Log completion */
%log_message(Backfill for features: &feature_list. completed successfully.);
```

---

### **Insert New Feature Script: `adhoc_scripts/insert_new_feature.sas`**

**Purpose**: Add a new feature to the existing pipeline and materialize it for historical data.

```sas
%include "../utils/logger.sas";
%include "../utils/database_utils.sas";
%include "../config/global_config.sas";
%include "../config/pipeline_configs/opacct_pipeline_config.sas";

%let new_feature_name = days_since_last_activity;

/* Log start of feature addition */
%log_message(Adding new feature: &new_feature_name.);

/* Step 1: Load historical data */
%log_message(Loading historical data from source table.);
%database_load(source_table=opacct_source_table, target_table=work.opacct_historical);

/* Step 2: Compute the new feature */
data work.opacct_new_feature;
    set work.opacct_historical;
    /* Example: Calculate days since the last activity */
    days_since_last_activity = intck('day', last_transaction_date, today());
run;

/* Step 3: Merge with existing features */
%log_message(Merging new feature with existing feature set.);
proc sql;
    create table work.opacct_updated as
    select a.*, b.days_since_last_activity
    from work.opacct_features a
    left join work.opacct_new_feature b
    on a.account_id = b.account_id;
quit;

/* Step 4: Write updated features to target */
%log_message(Writing updated feature set to target table.);
%database_write(source_table=work.opacct_updated, target_table=opacct_feature_table);

/* Log completion */
%log_message(New feature: &new_feature_name. added successfully.);
```

---

### **Manage Partitions Script: `adhoc_scripts/manage_partitions.sas`**

**Purpose**: Add, drop, or update partitions for a Hive table used in the `Opacct` pipeline.

```sas
%include "../utils/logger.sas";
%include "../utils/database_utils.sas";
%include "../config/global_config.sas";

%let action = add; /* Options: add, drop, update */
%let partition_date = '2024-01-01';
%let target_table = opacct_feature_table;

/* Log start of partition management */
%log_message(Starting partition management for table: &target_table., action: &action.);

/* Perform action */
%if &action = add %then %do;
    proc sql;
        alter table &target_table add partition (load_date = &partition_date.);
    quit;
    %log_message(Partition &partition_date. added to table: &target_table.);
%end;

%else %if &action = drop %then %do;
    proc sql;
        alter table &target_table drop partition (load_date = &partition_date.);
    quit;
    %log_message(Partition &partition_date. dropped from table: &target_table.);
%end;

%else %if &action = update %then %do;
    proc sql;
        alter table &target_table drop partition (load_date = &partition_date.);
        alter table &target_table add partition (load_date = &partition_date.);
    quit;
    %log_message(Partition &partition_date. updated in table: &target_table.);
%end;

%else %do;
    %log_message(Invalid action specified for partition management.);
%end;

/* Log completion */
%log_message(Partition management for table: &target_table., action: &action., completed successfully.);
```

### **6. Benefits of Refactoring**

| Aspect             | Before Refactoring                | After Refactoring                     |
|--------------------|------------------------------------|---------------------------------------|
| **Modularity**     | Tightly coupled logic             | Decoupled pipelines and feature logic |
| **Reusability**    | Redundant code                    | Shared utilities and metadata-driven  |
| **Scalability**    | Difficult to add new pipelines    | Simple to extend with new pipelines   |
| **Testing**        | Minimal or ad-hoc                 | Structured unit and integration tests |
| **Maintainability**| High effort for debugging         | Centralized and modular structure     |

---


### **7. POC Overview**

#### **Objective**:  
Refactor the `Opacct Pipeline` as a proof-of-concept (POC) for the new repository architecture. This POC will demonstrate the benefits of modularity, metadata-driven configurations, and shared utilities, serving as a template for other pipelines.

---

#### **Project Scope**

##### **In-Scope**:
- Refactor the `Opacct Pipeline` to:
  - Modularize feature engineering logic.
  - Utilize centralized metadata for source systems, features, and linkages.
  - Integrate shared utilities for database connections, logging, and validation.
- Implement unit and E2E tests for the pipeline.
- Document pipeline setup and execution.

##### **Out-of-Scope**:
- Refactoring pipelines other than `Opacct`.
- Introducing new business logic or features unless necessary for metadata integration.



#### **Deliverables**

1. **Refactored `Opacct Pipeline`**:
   - Modularized pipeline script using metadata and shared utilities.
2. **Centralized Metadata**:
   - `source_and_target_systems.yaml`, `feature_definitions.yaml`, and `linkage.yaml`.
3. **Shared Utilities**:
   - Include `database_utils.sas`, `logger.sas`, and `validator.sas`.
4. **Testing Framework**:
   - Unit tests for feature logic and E2E tests for the pipeline.
5. **Documentation**:
   - Pipeline execution guide and feature catalog.



#### **Milestones and Timeline**

| **Milestone**                        | **Tasks**                                                                                          | **Duration** |
|--------------------------------------|---------------------------------------------------------------------------------------------------|--------------|
| **1. Repository Restructure**        | Create directory structure for `Opacct Pipeline`.                                                 | 1 week       |
|                                      | Move existing `Opacct` scripts into the new structure.                                            |              |
| **2. Centralize Metadata**           | Create and populate metadata files specific to the `Opacct Pipeline`.                             | 1 week       |
| **3. Implement Shared Utilities**    | Develop or refine `database_utils.sas`, `logger.sas`, and `validator.sas`.                        | 2 weeks      |
| **4. Refactor `Opacct Pipeline`**    | Extract feature engineering logic into `opacct_features.sas`.                                     | 2 weeks      |
|                                      | Integrate metadata and utilities into `opacct_pipeline.sas`.                                      |              |
| **5. Introduce Testing Framework**   | Write unit tests for `opacct_features.sas`.                                                       | 1 week       |
|                                      | Develop E2E tests for `opacct_pipeline.sas`.                                                      |              |
| **6. Documentation and Handoff**     | Document pipeline execution and feature definitions.                                              | 1 week       |
| **Total Duration**                   |                                                                                                   | **8 weeks**  |

---

#### **Project Risks**

| **Risk**                                | **Impact**                                                                                       | **Mitigation Strategy**                                                                                     |
|-----------------------------------------|--------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| **Incomplete Metadata**                 | Missing or inaccurate metadata could delay pipeline refactoring.                                | Validate metadata with stakeholders before refactoring.                                                     |
| **Technical Challenges in Refactoring** | Legacy code issues may increase effort required for modularization.                             | Allocate additional time for debugging and testing refactored logic.                                        |
| **Testing Gaps**                        | Lack of test cases in legacy code could cause defects in refactored pipeline.                   | Create comprehensive test cases based on current logic and output expectations.                             |
| **Team Familiarity with New Approach**  | Limited experience with metadata-driven pipelines may slow progress.                            | Provide training sessions on the refactored architecture and metadata integration.                          |

---

#### **Success Metrics**

1. **Modularity**:
   - 100% of the `Opacct Pipeline` logic modularized and reusable.
2. **Metadata Utilization**:
   - Pipeline dynamically uses centralized metadata for sources, features, and linkages.
3. **Testing Coverage**:
   - 80% unit test coverage for feature engineering logic.
   - Successful execution of E2E tests for the pipeline.
4. **Time Efficiency**:
   - Reduce time required to add or update features by 50%.
5. **Stakeholder Feedback**:
   - Positive feedback on the POC’s scalability and maintainability.

