import os
import yaml

# Define the repository structure
repo_structure = {
    "feature_store_repo": {
        "pipelines": {
            "customer_pipeline": {
                "customer_pipeline.sas": "",
                "feature_logic.sas": "",
                "config": {
                    "customer_config.yml": yaml.dump({
                        "materialized_table": "customer_feature_table",
                        "source_tables": [
                            {"source": "customer_data", "key_column": "customer_id", 
                             "required_columns": ["purchase_amount", "transaction_count"]},
                            {"source": "transaction_data", "key_column": "customer_id", 
                             "required_columns": ["last_purchase_date"]}
                        ],
                        "features": [
                            {"name": "average_purchase_value", "transformation": "purchase_amount / transaction_count"},
                            {"name": "days_since_last_purchase", "transformation": "DATEDIFF(current_date, last_purchase_date)"}
                        ]
                    }, default_flow_style=False),
                },
                "tests": {
                    "test_customer_pipeline.sas": ""
                }
            },
            "sales_pipeline": {
                "sales_pipeline.sas": "",
                "feature_logic.sas": "",
                "config": {
                    "sales_config.yml": yaml.dump({
                        "materialized_table": "sales_feature_table",
                        "source_tables": [
                            {"source": "sales_data", "key_column": "sale_id", 
                             "required_columns": ["sale_amount", "sale_date"]}
                        ],
                        "features": [
                            {"name": "total_sales", "transformation": "SUM(sale_amount)"},
                            {"name": "sales_frequency", "transformation": "COUNT(sale_id) / DATEDIFF(max(sale_date), min(sale_date))"}
                        ]
                    }, default_flow_style=False),
                },
                "tests": {
                    "test_sales_pipeline.sas": ""
                }
            },
            "shared": {
                "hive_utils.sas": "",
                "logger.sas": "",
                "validator.sas": "",
                "common_features.sas": ""
            }
        },
        "metadata": {
            "feature_definitions.yml": yaml.dump({
                "features": [
                    {"name": "average_purchase_value", "entity": "customer", "type": "FLOAT"},
                    {"name": "days_since_last_purchase", "entity": "customer", "type": "INT"}
                ]
            }, default_flow_style=False),
            "entity_definitions.yml": yaml.dump({
                "entities": [
                    {"name": "customer", "key_column": "customer_id"},
                    {"name": "sales", "key_column": "sale_id"}
                ]
            }, default_flow_style=False),
            "source_systems.yml": yaml.dump({
                "source_systems": {
                    "customer_data": {"system_name": "CRM", "connection": "hive_crm", "table": "customers_raw"},
                    "transaction_data": {"system_name": "SalesDB", "connection": "hive_sales", "table": "transactions_raw"}
                }
            }, default_flow_style=False)
        },
        "features": {
            "customer_features.sas": "",
            "sales_features.sas": "",
            "transactions_features.sas": ""
        },
        "config": {
            "hive_config.sas": "",
            "pipeline_defaults.yml": yaml.dump({
                "defaults": {
                    "partition_column": "event_time",
                    "output_format": "parquet",
                    "enable_logging": True
                }
            }, default_flow_style=False),
            "feature_store_config.yml": ""
        },
        "scripts": {
            "backfill_feature.sas": "",
            "update_feature.sas": "",
            "insert_new_feature.sas": "",
            "manage_partitions.sas": ""
        },
        "tests": {
            "test_pipeline_execution.sas": "",
            "test_feature_output.sas": "",
            "test_hive_operations.sas": ""
        },
        "docs": {
            "feature_catalog.md": "",
            "pipeline_guide.md": "",
            "troubleshooting.md": ""
        },
        "README.md": "Overview of the feature store repository.",
        "LICENSE": "MIT License"
    }
}

# Function to create the repository
def create_repo(structure, root=""):
    for name, content in structure.items():
        path = os.path.join(root, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_repo(content, root=path)
        else:
            with open(path, "w") as f:
                f.write(content)

# Generate the repository
create_repo(repo_structure)

print("Repository created successfully.")
