data work.customer_features;
    set work.customer_data;
    /* Calculate average purchase value */
    average_purchase_value = purchase_amount / transaction_count;
    /* Calculate days since last purchase */
    days_since_last_purchase = intck('day', last_purchase_date, today());
run;
