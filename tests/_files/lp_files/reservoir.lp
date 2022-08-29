\* Source Pyomo model name=Model *\

min
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_Bus_balance(electricity_0)_:
+1 flow(reservoir_electricity_0)
= 0

c_e_Bus_balance(electricity_1)_:
+1 flow(reservoir_electricity_1)
= 0

c_e_Bus_balance(electricity_2)_:
+1 flow(reservoir_electricity_2)
= 0

c_e_GenericStorageBlock_balance_first(reservoir)_:
+1 GenericStorageBlock_storage_content(reservoir_0)
+1.25 flow(reservoir_electricity_0)
-1 flow(reservoir_inflow_reservoir_0)
= 0

c_e_GenericStorageBlock_balance(reservoir_1)_:
-0.90000000000000002 GenericStorageBlock_storage_content(reservoir_0)
+1 GenericStorageBlock_storage_content(reservoir_1)
+1.25 flow(reservoir_electricity_1)
-1 flow(reservoir_inflow_reservoir_1)
= 0

c_e_GenericStorageBlock_balance(reservoir_2)_:
-0.90000000000000002 GenericStorageBlock_storage_content(reservoir_1)
+1 GenericStorageBlock_storage_content(reservoir_2)
+1.25 flow(reservoir_electricity_2)
-1 flow(reservoir_inflow_reservoir_2)
= 0

c_e_GenericStorageBlock_balanced_cstr(reservoir)_:
+1 GenericStorageBlock_storage_content(reservoir_2)
= 0

c_e_ONE_VAR_CONSTANT:
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(reservoir_electricity_0) <= 50
   0 <= flow(reservoir_electricity_1) <= 50
   0 <= flow(reservoir_electricity_2) <= 50
   0 <= flow(reservoir_inflow_reservoir_0) <= 1
   0 <= flow(reservoir_inflow_reservoir_1) <= 2
   0 <= flow(reservoir_inflow_reservoir_2) <= 6
   0 <= GenericStorageBlock_storage_content(reservoir_0) <= 750
   0 <= GenericStorageBlock_storage_content(reservoir_1) <= 750
   0 <= GenericStorageBlock_storage_content(reservoir_2) <= 750
end