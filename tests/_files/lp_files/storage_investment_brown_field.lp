\* Source Pyomo model name=Model *\

min
objective:
+1300 GenericInvestmentStorageBlock_invest(storage)
+240 InvestmentFlowBlock_invest(electricity_storage)

s.t.

c_e_BusBlock_balance(electricity_0)_:
-1 flow(electricity_storage_0)
+1 flow(storage_electricity_0)
= 0

c_e_BusBlock_balance(electricity_1)_:
-1 flow(electricity_storage_1)
+1 flow(storage_electricity_1)
= 0

c_e_BusBlock_balance(electricity_2)_:
-1 flow(electricity_storage_2)
+1 flow(storage_electricity_2)
= 0

c_u_InvestmentFlowBlock_max(electricity_storage_0)_:
-1 InvestmentFlowBlock_invest(electricity_storage)
+1 flow(electricity_storage_0)
<= 1

c_u_InvestmentFlowBlock_max(electricity_storage_1)_:
-1 InvestmentFlowBlock_invest(electricity_storage)
+1 flow(electricity_storage_1)
<= 1

c_u_InvestmentFlowBlock_max(electricity_storage_2)_:
-1 InvestmentFlowBlock_invest(electricity_storage)
+1 flow(electricity_storage_2)
<= 1

c_u_InvestmentFlowBlock_max(storage_electricity_0)_:
-1 InvestmentFlowBlock_invest(storage_electricity)
+1 flow(storage_electricity_0)
<= 1

c_u_InvestmentFlowBlock_max(storage_electricity_1)_:
-1 InvestmentFlowBlock_invest(storage_electricity)
+1 flow(storage_electricity_1)
<= 1

c_u_InvestmentFlowBlock_max(storage_electricity_2)_:
-1 InvestmentFlowBlock_invest(storage_electricity)
+1 flow(storage_electricity_2)
<= 1

c_u_GenericInvestmentStorageBlock_init_content_limit(storage)_:
+1 GenericInvestmentStorageBlock_init_content(storage)
-1 GenericInvestmentStorageBlock_invest(storage)
<= 2

c_e_GenericInvestmentStorageBlock_balance_first(storage)_:
-1 GenericInvestmentStorageBlock_init_content(storage)
+1 GenericInvestmentStorageBlock_storage_content(storage_0)
-0.90000000000000002 flow(electricity_storage_0)
+1.1111111111111112 flow(storage_electricity_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1)_:
-1 GenericInvestmentStorageBlock_storage_content(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_1)
-0.90000000000000002 flow(electricity_storage_1)
+1.1111111111111112 flow(storage_electricity_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2)_:
-1 GenericInvestmentStorageBlock_storage_content(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_2)
-0.90000000000000002 flow(electricity_storage_2)
+1.1111111111111112 flow(storage_electricity_2)
= 0

c_e_GenericInvestmentStorageBlock_balanced_cstr(storage)_:
-1 GenericInvestmentStorageBlock_init_content(storage)
+1 GenericInvestmentStorageBlock_storage_content(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(storage)_:
-1 InvestmentFlowBlock_invest(electricity_storage)
+1 InvestmentFlowBlock_invest(storage_electricity)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0)_:
-1 GenericInvestmentStorageBlock_invest(storage)
+1 GenericInvestmentStorageBlock_storage_content(storage_0)
<= 2

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_1)_:
-1 GenericInvestmentStorageBlock_invest(storage)
+1 GenericInvestmentStorageBlock_storage_content(storage_1)
<= 2

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_2)_:
-1 GenericInvestmentStorageBlock_invest(storage)
+1 GenericInvestmentStorageBlock_storage_content(storage_2)
<= 2

c_e_ONE_VAR_CONSTANT:
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(electricity_storage_0) <= +inf
   0 <= flow(electricity_storage_1) <= +inf
   0 <= flow(electricity_storage_2) <= +inf
   0 <= flow(storage_electricity_0) <= +inf
   0 <= flow(storage_electricity_1) <= +inf
   0 <= flow(storage_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_invest(electricity_storage) <= 4
   0 <= InvestmentFlowBlock_invest(storage_electricity) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage) <= 8
   0 <= GenericInvestmentStorageBlock_init_content(storage) <= +inf
end
