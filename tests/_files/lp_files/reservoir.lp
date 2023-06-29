\* Source Pyomo model name=Model *\

min 
objective:
+0 ONE_VAR_CONSTANT

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

c_e_GenericStorageBlock_balanced_cstr(reservoir)_:
+1 GenericStorageBlock_storage_content(reservoir_3)
= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= flow(reservoir_electricity_0_0) <= 50
   0 <= flow(reservoir_electricity_0_1) <= 50
   0 <= flow(reservoir_electricity_0_2) <= 50
   0 <= GenericStorageBlock_storage_content(reservoir_1) <= 750.0
   0 <= GenericStorageBlock_storage_content(reservoir_2) <= 750.0
   0 <= GenericStorageBlock_storage_content(reservoir_3) <= 750.0
end
