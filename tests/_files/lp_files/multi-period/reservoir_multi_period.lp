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

c_e_BusBlock_balance(electricity_3)_:
+1 flow(reservoir_electricity_3)
= 0

c_e_BusBlock_balance(electricity_4)_:
+1 flow(reservoir_electricity_4)
= 0

c_e_BusBlock_balance(electricity_5)_:
+1 flow(reservoir_electricity_5)
= 0

c_e_BusBlock_balance(electricity_6)_:
+1 flow(reservoir_electricity_6)
= 0

c_e_BusBlock_balance(electricity_7)_:
+1 flow(reservoir_electricity_7)
= 0

c_e_BusBlock_balance(electricity_8)_:
+1 flow(reservoir_electricity_8)
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

c_e_GenericStorageBlock_losses(reservoir_3)_:
-1 GenericStorageBlock_storage_losses(reservoir_3)
+0.09999999999999998 GenericStorageBlock_storage_content(reservoir_3)
= 0

c_e_GenericStorageBlock_losses(reservoir_4)_:
-1 GenericStorageBlock_storage_losses(reservoir_4)
+0.09999999999999998 GenericStorageBlock_storage_content(reservoir_4)
= 0

c_e_GenericStorageBlock_losses(reservoir_5)_:
-1 GenericStorageBlock_storage_losses(reservoir_5)
+0.09999999999999998 GenericStorageBlock_storage_content(reservoir_5)
= 0

c_e_GenericStorageBlock_losses(reservoir_6)_:
-1 GenericStorageBlock_storage_losses(reservoir_6)
+0.09999999999999998 GenericStorageBlock_storage_content(reservoir_6)
= 0

c_e_GenericStorageBlock_losses(reservoir_7)_:
-1 GenericStorageBlock_storage_losses(reservoir_7)
+0.09999999999999998 GenericStorageBlock_storage_content(reservoir_7)
= 0

c_e_GenericStorageBlock_losses(reservoir_8)_:
-1 GenericStorageBlock_storage_losses(reservoir_8)
+0.09999999999999998 GenericStorageBlock_storage_content(reservoir_8)
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

c_e_GenericStorageBlock_balance(reservoir_3)_:
-1.25 flow(reservoir_electricity_3)
+1 flow((_reservoir_inflow____reservoir_)_reservoir_3)
-1 GenericStorageBlock_storage_losses(reservoir_3)
+1 GenericStorageBlock_storage_content(reservoir_3)
-1 GenericStorageBlock_storage_content(reservoir_4)
= 0

c_e_GenericStorageBlock_balance(reservoir_4)_:
-1.25 flow(reservoir_electricity_4)
+1 flow((_reservoir_inflow____reservoir_)_reservoir_4)
-1 GenericStorageBlock_storage_losses(reservoir_4)
+1 GenericStorageBlock_storage_content(reservoir_4)
-1 GenericStorageBlock_storage_content(reservoir_5)
= 0

c_e_GenericStorageBlock_balance(reservoir_5)_:
-1.25 flow(reservoir_electricity_5)
+1 flow((_reservoir_inflow____reservoir_)_reservoir_5)
-1 GenericStorageBlock_storage_losses(reservoir_5)
+1 GenericStorageBlock_storage_content(reservoir_5)
-1 GenericStorageBlock_storage_content(reservoir_6)
= 0

c_e_GenericStorageBlock_balance(reservoir_6)_:
-1.25 flow(reservoir_electricity_6)
+1 flow((_reservoir_inflow____reservoir_)_reservoir_6)
-1 GenericStorageBlock_storage_losses(reservoir_6)
+1 GenericStorageBlock_storage_content(reservoir_6)
-1 GenericStorageBlock_storage_content(reservoir_7)
= 0

c_e_GenericStorageBlock_balance(reservoir_7)_:
-1.25 flow(reservoir_electricity_7)
+1 flow((_reservoir_inflow____reservoir_)_reservoir_7)
-1 GenericStorageBlock_storage_losses(reservoir_7)
+1 GenericStorageBlock_storage_content(reservoir_7)
-1 GenericStorageBlock_storage_content(reservoir_8)
= 0

c_e_GenericStorageBlock_balance(reservoir_8)_:
-1.25 flow(reservoir_electricity_8)
+1 flow((_reservoir_inflow____reservoir_)_reservoir_8)
-1 GenericStorageBlock_storage_losses(reservoir_8)
+1 GenericStorageBlock_storage_content(reservoir_8)
-1 GenericStorageBlock_storage_content(reservoir_9)
= 0

c_e_GenericStorageBlock_balanced_cstr(reservoir)_:
+1 GenericStorageBlock_storage_content(reservoir_9)
= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= flow(reservoir_electricity_0) <= 50
   0 <= flow(reservoir_electricity_1) <= 50
   0 <= flow(reservoir_electricity_2) <= 50
   0 <= flow(reservoir_electricity_3) <= 50
   0 <= flow(reservoir_electricity_4) <= 50
   0 <= flow(reservoir_electricity_5) <= 50
   0 <= flow(reservoir_electricity_6) <= 50
   0 <= flow(reservoir_electricity_7) <= 50
   0 <= flow(reservoir_electricity_8) <= 50
   0 <= flow((_reservoir_inflow____reservoir_)_reservoir_0) <= 1
   0 <= flow((_reservoir_inflow____reservoir_)_reservoir_1) <= 2
   0 <= flow((_reservoir_inflow____reservoir_)_reservoir_2) <= 6
   0 <= flow((_reservoir_inflow____reservoir_)_reservoir_3) <= 1
   0 <= flow((_reservoir_inflow____reservoir_)_reservoir_4) <= 2
   0 <= flow((_reservoir_inflow____reservoir_)_reservoir_5) <= 6
   0 <= flow((_reservoir_inflow____reservoir_)_reservoir_6) <= 1
   0 <= flow((_reservoir_inflow____reservoir_)_reservoir_7) <= 2
   0 <= flow((_reservoir_inflow____reservoir_)_reservoir_8) <= 6
   -inf <= GenericStorageBlock_storage_losses(reservoir_0) <= +inf
   -inf <= GenericStorageBlock_storage_losses(reservoir_1) <= +inf
   -inf <= GenericStorageBlock_storage_losses(reservoir_2) <= +inf
   -inf <= GenericStorageBlock_storage_losses(reservoir_3) <= +inf
   -inf <= GenericStorageBlock_storage_losses(reservoir_4) <= +inf
   -inf <= GenericStorageBlock_storage_losses(reservoir_5) <= +inf
   -inf <= GenericStorageBlock_storage_losses(reservoir_6) <= +inf
   -inf <= GenericStorageBlock_storage_losses(reservoir_7) <= +inf
   -inf <= GenericStorageBlock_storage_losses(reservoir_8) <= +inf
   0 <= GenericStorageBlock_storage_content(reservoir_1) <= 750.0
   0 <= GenericStorageBlock_storage_content(reservoir_2) <= 750.0
   0 <= GenericStorageBlock_storage_content(reservoir_3) <= 750.0
   0 <= GenericStorageBlock_storage_content(reservoir_4) <= 750.0
   0 <= GenericStorageBlock_storage_content(reservoir_5) <= 750.0
   0 <= GenericStorageBlock_storage_content(reservoir_6) <= 750.0
   0 <= GenericStorageBlock_storage_content(reservoir_7) <= 750.0
   0 <= GenericStorageBlock_storage_content(reservoir_8) <= 750.0
   0 <= GenericStorageBlock_storage_content(reservoir_9) <= 750.0
end
