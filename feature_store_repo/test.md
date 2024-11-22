Refactored_repo/
├── metadata/                                  # Centralized metadata for features
│   ├── source_and_target_systems.yaml         # YAML file documenting source and target systems
│   ├── feature_definitions.yaml               # YAML file documenting all features
│   ├── linkage.yaml                           # YAML file detailed linkage for features
├── config/                                    # for defining paths, varibales etc etc 
│   ├── global_config.sas                      # for defining global paths, varibales etc etc
│   ├── pipeline_configs/                      # for defining pipeline-specific paths, varibales etc etc
│   │   ├── customer_universe_pipeline_config.sas
│   │   ├── account_universe_pipeline_config.sas
│   │   ├── opacct_pipeline_config.sas
│   │   ├── financial_pipeline_config.sas
│   │   ├── term_and_revolver_pipeline_config.sas
├── utils/                         # Shared logic for all pipelines
│   ├── database_utils.sas         # functions for connecting to sources and targets, DDLs, loading utilties
│   ├── etl_precheck_utils.sas     # utils for pre-check before running etl
│   ├── etl_status_utils.sas       # utils for status-tracking of a running etl
│   ├── logger.sas                 # functions for Centralized logging
│   ├── validator.sas              # functions for Data validation utilities 
├── feature_materialization/   
│   └── common_features.sas              # Common features for all pipelines                  
│   ├── customer_universe_features.sas   # materialize features from metadata for customer_universe dataset
│   ├── account_universe_features.sas    # materialize features from metadata for account_universe dataset
│   ├── opacct_features.sas              # materialize features from metadata for opacct dataset
│   ├── financial_features.sas           # materialize features from metadata for financial dataset
│   ├── term_and_revolver_features.sas   # materialize features from metadata for term_and_revolver dataset
├── pipelines/                     
│   ├── customer_universe_pipeline/         # Pipeline for customer-related table
│   │   ├── customer_universe_pipeline.sas  # Main pipeline for customer table
│   ├── account_univers_pipeline/            # Pipeline for sales-related table
│   │   ├── account_univers_pipeline.sas     # Main pipeline for sales table
│   ├── opacct_pipeline/     # Pipeline for transaction-related table
│   │   ├── opacct_pipeline.sas
│   ├── financial_pipeline/            # Pipeline for sales-related table
│   │   ├── financial_pipeline.sas     # Main pipeline for sales table
│   ├── term_and_revolver_pipeline/     # Pipeline for transaction-related table
│   │   ├── term_and_revolver_pipeline.sas
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