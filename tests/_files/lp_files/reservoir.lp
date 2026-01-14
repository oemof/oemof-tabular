\* Source Pyomo model name=Model *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_BusBlock_balance(electricity_0)_:
+1 flow(reservoir_electricity_0)
= 0

c_e_BusBlock_balance(electricity_1)_:
+1 flow(reservoir_electricity_1)
= 0

c_e_BusBlock_balance(electricity_2)_:
+1 flow(reservoir_electricity_2)
= 0

c_e_GenericStorageBlock_losses(reservoir_0)_:
-1 GenericStorageBlock_storage_losses(reservoir_0)
= 0.0

c_e_GenericStorageBlock_losses(reservoir_1)_:
-1 GenericStorageBlock_storage_losses(reservoir_1)
+0.09999999999999998 GenericStorageBlock_storage_content(reservoir_1)
= 0

c_e_GenericStorageBlock_losses(reservoir_2)_:
-1 GenericStorageBlock_storage_losses(reservoir_2)
+0.09999999999999998 GenericStorageBlock_storage_content(reservoir_2)
= 0

c_e_GenericStorageBlock_balance(reservoir_0)_:
-1.25 flow(reservoir_electricity_0)
+1 flow((_reservoir_inflow____reservoir_)_reservoir_0)
-1 GenericStorageBlock_storage_losses(reservoir_0)
-1 GenericStorageBlock_storage_content(reservoir_1)
= 0

c_e_GenericStorageBlock_balance(reservoir_1)_:
-1.25 flow(reservoir_electricity_1)
+1 flow((_reservoir_inflow____reservoir_)_reservoir_1)
-1 GenericStorageBlock_storage_losses(reservoir_1)
+1 GenericStorageBlock_storage_content(reservoir_1)
-1 GenericStorageBlock_storage_content(reservoir_2)
= 0

c_e_GenericStorageBlock_balance(reservoir_2)_:
-1.25 flow(reservoir_electricity_2)
+1 flow((_reservoir_inflow____reservoir_)_reservoir_2)
-1 GenericStorageBlock_storage_losses(reservoir_2)
+1 GenericStorageBlock_storage_content(reservoir_2)
-1 GenericStorageBlock_storage_content(reservoir_3)
= 0

c_e_GenericStorageBlock_balanced_cstr(reservoir)_:
+1 GenericStorageBlock_storage_content(reservoir_3)
= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= flow(reservoir_electricity_0) <= 50
   0 <= flow(reservoir_electricity_1) <= 50
   0 <= flow(reservoir_electricity_2) <= 50
   0 <= flow((_reservoir_inflow____reservoir_)_reservoir_0) <= 1
   0 <= flow((_reservoir_inflow____reservoir_)_reservoir_1) <= 2
   0 <= flow((_reservoir_inflow____reservoir_)_reservoir_2) <= 6
   -inf <= GenericStorageBlock_storage_losses(reservoir_0) <= +inf
   -inf <= GenericStorageBlock_storage_losses(reservoir_1) <= +inf
   -inf <= GenericStorageBlock_storage_losses(reservoir_2) <= +inf
   0 <= GenericStorageBlock_storage_content(reservoir_1) <= 750.0
   0 <= GenericStorageBlock_storage_content(reservoir_2) <= 750.0
   0 <= GenericStorageBlock_storage_content(reservoir_3) <= 750.0
end
