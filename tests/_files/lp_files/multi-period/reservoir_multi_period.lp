\* Source Pyomo model name=Model *\

min 
objective:
+0.0 ONE_VAR_CONSTANT

s.t.

c_e_BusBlock_balance(electricity_0_0)_:
+1 flow(reservoir_electricity_0_0)
= 0

c_e_BusBlock_balance(electricity_0_1)_:
+1 flow(reservoir_electricity_0_1)
= 0

c_e_BusBlock_balance(electricity_0_2)_:
+1 flow(reservoir_electricity_0_2)
= 0

c_e_BusBlock_balance(electricity_1_3)_:
+1 flow(reservoir_electricity_1_3)
= 0

c_e_BusBlock_balance(electricity_1_4)_:
+1 flow(reservoir_electricity_1_4)
= 0

c_e_BusBlock_balance(electricity_1_5)_:
+1 flow(reservoir_electricity_1_5)
= 0

c_e_BusBlock_balance(electricity_2_6)_:
+1 flow(reservoir_electricity_2_6)
= 0

c_e_BusBlock_balance(electricity_2_7)_:
+1 flow(reservoir_electricity_2_7)
= 0

c_e_BusBlock_balance(electricity_2_8)_:
+1 flow(reservoir_electricity_2_8)
= 0

c_e_GenericStorageBlock_balance(reservoir_0_0)_:
+1.25 flow(reservoir_electricity_0_0)
+1 GenericStorageBlock_storage_content(reservoir_1)
-1 flow(reservoir_inflow_reservoir_0_0)
= 0.0

c_e_GenericStorageBlock_balance(reservoir_0_1)_:
+1.25 flow(reservoir_electricity_0_1)
-0.9 GenericStorageBlock_storage_content(reservoir_1)
+1 GenericStorageBlock_storage_content(reservoir_2)
-1 flow(reservoir_inflow_reservoir_0_1)
= 0

c_e_GenericStorageBlock_balance(reservoir_0_2)_:
+1.25 flow(reservoir_electricity_0_2)
-0.9 GenericStorageBlock_storage_content(reservoir_2)
+1 GenericStorageBlock_storage_content(reservoir_3)
-1 flow(reservoir_inflow_reservoir_0_2)
= 0

c_e_GenericStorageBlock_balance(reservoir_1_3)_:
+1.25 flow(reservoir_electricity_1_3)
-0.9 GenericStorageBlock_storage_content(reservoir_3)
+1 GenericStorageBlock_storage_content(reservoir_4)
-1 flow(reservoir_inflow_reservoir_1_3)
= 0

c_e_GenericStorageBlock_balance(reservoir_1_4)_:
+1.25 flow(reservoir_electricity_1_4)
-0.9 GenericStorageBlock_storage_content(reservoir_4)
+1 GenericStorageBlock_storage_content(reservoir_5)
-1 flow(reservoir_inflow_reservoir_1_4)
= 0

c_e_GenericStorageBlock_balance(reservoir_1_5)_:
+1.25 flow(reservoir_electricity_1_5)
-0.9 GenericStorageBlock_storage_content(reservoir_5)
+1 GenericStorageBlock_storage_content(reservoir_6)
-1 flow(reservoir_inflow_reservoir_1_5)
= 0

c_e_GenericStorageBlock_balance(reservoir_2_6)_:
+1.25 flow(reservoir_electricity_2_6)
-0.9 GenericStorageBlock_storage_content(reservoir_6)
+1 GenericStorageBlock_storage_content(reservoir_7)
-1 flow(reservoir_inflow_reservoir_2_6)
= 0

c_e_GenericStorageBlock_balance(reservoir_2_7)_:
+1.25 flow(reservoir_electricity_2_7)
-0.9 GenericStorageBlock_storage_content(reservoir_7)
+1 GenericStorageBlock_storage_content(reservoir_8)
-1 flow(reservoir_inflow_reservoir_2_7)
= 0

c_e_GenericStorageBlock_balance(reservoir_2_8)_:
+1.25 flow(reservoir_electricity_2_8)
-0.9 GenericStorageBlock_storage_content(reservoir_8)
+1 GenericStorageBlock_storage_content(reservoir_9)
-1 flow(reservoir_inflow_reservoir_2_8)
= 0

c_e_GenericStorageBlock_balanced_cstr(reservoir)_:
+1 GenericStorageBlock_storage_content(reservoir_9)
= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= flow(reservoir_electricity_0_0) <= 50
   0 <= flow(reservoir_electricity_0_1) <= 50
   0 <= flow(reservoir_electricity_0_2) <= 50
   0 <= flow(reservoir_electricity_1_3) <= 50
   0 <= flow(reservoir_electricity_1_4) <= 50
   0 <= flow(reservoir_electricity_1_5) <= 50
   0 <= flow(reservoir_electricity_2_6) <= 50
   0 <= flow(reservoir_electricity_2_7) <= 50
   0 <= flow(reservoir_electricity_2_8) <= 50
   0 <= GenericStorageBlock_storage_content(reservoir_1) <= 750.0
   0 <= flow(reservoir_inflow_reservoir_0_0) <= 1
   0 <= GenericStorageBlock_storage_content(reservoir_2) <= 750.0
   0 <= flow(reservoir_inflow_reservoir_0_1) <= 2
   0 <= GenericStorageBlock_storage_content(reservoir_3) <= 750.0
   0 <= flow(reservoir_inflow_reservoir_0_2) <= 6
   0 <= GenericStorageBlock_storage_content(reservoir_4) <= 750.0
   0 <= flow(reservoir_inflow_reservoir_1_3) <= 1
   0 <= GenericStorageBlock_storage_content(reservoir_5) <= 750.0
   0 <= flow(reservoir_inflow_reservoir_1_4) <= 2
   0 <= GenericStorageBlock_storage_content(reservoir_6) <= 750.0
   0 <= flow(reservoir_inflow_reservoir_1_5) <= 6
   0 <= GenericStorageBlock_storage_content(reservoir_7) <= 750.0
   0 <= flow(reservoir_inflow_reservoir_2_6) <= 1
   0 <= GenericStorageBlock_storage_content(reservoir_8) <= 750.0
   0 <= flow(reservoir_inflow_reservoir_2_7) <= 2
   0 <= GenericStorageBlock_storage_content(reservoir_9) <= 750.0
   0 <= flow(reservoir_inflow_reservoir_2_8) <= 6
end
