%include "../customer_pipeline.sas";

/* Validate the generated features */
%log_message(Testing customer pipeline output.);
proc sql;
    select count(*) as row_count
    from hive.customer_feature_table
    where customer_id is null;
quit;

/* Display sample results */
proc print data=hive.customer_feature_table(obs=10);
run;

%log_message(Customer pipeline test completed successfully.);
