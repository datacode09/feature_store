%include "../shared/hive_utils.sas";
%include "../shared/logger.sas";
%include "../shared/validator.sas";
%include "feature_logic.sas";

%hive_connect(config_path="../config/hive_config.sas");

/* Step 1: Load data from Hive source tables */
%log_message(Loading customer data from source systems.);
proc sql;
    create table work.customer_data as
    select customer_id, purchase_amount, transaction_count
    from hive_crm.customers_raw;

    create table work.transaction_data as
    select customer_id, last_purchase_date
    from hive_sales.transactions_raw;
quit;

/* Step 2: Generate customer features */
%log_message(Generating customer features.);
%include "feature_logic.sas";

/* Step 3: Insert features into the materialized table */
%log_message(Inserting features into Hive materialized table.);
proc sql;
    insert overwrite table hive.customer_feature_table
    select customer_id, average_purchase_value, days_since_last_purchase
    from work.customer_features;
quit;

%hive_disconnect();
%log_message(Customer pipeline execution completed successfully.);
