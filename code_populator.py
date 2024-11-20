# Define sample code for all files in the repository
full_sample_code = {
    "pipelines/customer_pipeline/customer_pipeline.sas": """
%include "../shared/hive_utils.sas";
%include "../shared/logger.sas";
%include "../shared/validator.sas";
%include "feature_logic.sas";

%hive_connect(config_path="../config/hive_config.sas");

/* Load customer and transaction data */
proc sql;
    create table work.customer_data as
    select customer_id, purchase_amount, transaction_count
    from hive_crm.customers_raw;

    create table work.transaction_data as
    select customer_id, last_purchase_date
    from hive_sales.transactions_raw;
quit;

/* Generate features */
%include "feature_logic.sas";

proc sql;
    insert overwrite table hive.customer_feature_table
    select customer_id, average_purchase_value, days_since_last_purchase
    from work.customer_features;
quit;

%hive_disconnect();
""",
    "pipelines/customer_pipeline/feature_logic.sas": """
data work.customer_features;
    set work.customer_data;
    average_purchase_value = purchase_amount / transaction_count;
    days_since_last_purchase = intck('day', last_purchase_date, today());
run;
""",
    "pipelines/customer_pipeline/tests/test_customer_pipeline.sas": """
%include "../customer_pipeline.sas";

data test_results;
    set hive.customer_feature_table;
    where customer_id is not null;
run;

proc print data=test_results(obs=10);
run;
""",
    "pipelines/sales_pipeline/sales_pipeline.sas": """
%include "../shared/hive_utils.sas";
%include "../shared/logger.sas";
%include "../shared/validator.sas";
%include "feature_logic.sas";

%hive_connect(config_path="../config/hive_config.sas");

/* Load sales data */
proc sql;
    create table work.sales_data as
    select sale_id, sale_amount, sale_date
    from hive_sales.sales_raw;
quit;

/* Generate features */
%include "feature_logic.sas";

proc sql;
    insert overwrite table hive.sales_feature_table
    select sale_id, total_sales, sales_frequency
    from work.sales_features;
quit;

%hive_disconnect();
""",
    "pipelines/sales_pipeline/feature_logic.sas": """
data work.sales_features;
    set work.sales_data;
    total_sales = sum(sale_amount);
    sales_frequency = count(sale_id) / intck('day', min(sale_date), max(sale_date));
run;
""",
    "pipelines/sales_pipeline/tests/test_sales_pipeline.sas": """
%include "../sales_pipeline.sas";

data test_results;
    set hive.sales_feature_table;
    where sale_id is not null;
run;

proc print data=test_results(obs=10);
run;
""",
    "pipelines/shared/hive_utils.sas": """
%macro hive_connect(config_path);
    %include "&config_path";
    libname hive hadoop server="&hive_server" schema="&hive_schema";
%mend hive_connect;

%macro hive_disconnect();
    libname hive clear;
%mend hive_disconnect;
""",
    "pipelines/shared/logger.sas": """
%macro log_message(message);
    %put NOTE: &message;
%mend log_message;
""",
    "pipelines/shared/validator.sas": """
%macro validate_data(data);
    proc sql;
        select count(*) as missing_values
        from &data
        where customer_id is null;
    quit;
%mend validate_data;
""",
    "features/customer_features.sas": """
%macro average_purchase_value(purchase_amount, transaction_count);
    purchase_amount / transaction_count;
%mend average_purchase_value;

%macro days_since_last_purchase(last_purchase_date);
    intck('day', last_purchase_date, today());
%mend days_since_last_purchase;
""",
    "features/sales_features.sas": """
%macro total_sales(sale_amount);
    sum(sale_amount);
%mend total_sales;

%macro sales_frequency(sale_id, sale_date);
    count(sale_id) / intck('day', min(sale_date), max(sale_date));
%mend sales_frequency;
""",
    "scripts/backfill_feature.sas": """
%include "../pipelines/shared/hive_utils.sas";
%include "../features/customer_features.sas";

%hive_connect(config_path="../config/hive_config.sas");

proc sql;
    insert into hive.customer_feature_table
    select customer_id, 
           %average_purchase_value(purchase_amount, transaction_count) as average_purchase_value,
           %days_since_last_purchase(last_purchase_date) as days_since_last_purchase
    from hive_crm.customers_raw;
quit;

%hive_disconnect();
""",
    "scripts/update_feature.sas": """
%include "../features/customer_features.sas";

data updated_features;
    set hive.customer_feature_table;
    average_purchase_value = %average_purchase_value(purchase_amount, transaction_count);
run;
""",
    "scripts/insert_new_feature.sas": """
%include "../features/customer_features.sas";

data new_features;
    set hive.customer_feature_table;
    new_feature = some_new_logic_here;
run;
""",
}

# Populate the repository with sample code
populate_files_with_sample_code("feature_store_repo", full_sample_code)

print("Full sample code added to all repository files.")
