\* Source Pyomo model name=Model *\

min 
objective:
+5 flow(storage_electricity_0_0)
+5 flow(storage_electricity_0_1)
+5 flow(storage_electricity_0_2)
+10 GenericInvestmentStorageBlock_invest(storage_0)

s.t.

c_e_BusBlock_balance(electricity_0_0)_:
+1 flow(storage_electricity_0_0)
-1 flow(electricity_storage_0_0)
= 0

c_e_BusBlock_balance(electricity_0_1)_:
+1 flow(storage_electricity_0_1)
-1 flow(electricity_storage_0_1)
= 0

c_e_BusBlock_balance(electricity_0_2)_:
+1 flow(storage_electricity_0_2)
-1 flow(electricity_storage_0_2)
= 0

c_u_InvestmentFlowBlock_max(electricity_storage_0_0)_:
+1 flow(electricity_storage_0_0)
-1 InvestmentFlowBlock_total(electricity_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_0_1)_:
+1 flow(electricity_storage_0_1)
-1 InvestmentFlowBlock_total(electricity_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_0_2)_:
+1 flow(electricity_storage_0_2)
-1 InvestmentFlowBlock_total(electricity_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_0_0)_:
+1 flow(storage_electricity_0_0)
-1 InvestmentFlowBlock_total(storage_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_0_1)_:
+1 flow(storage_electricity_0_1)
-1 InvestmentFlowBlock_total(storage_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_0_2)_:
+1 flow(storage_electricity_0_2)
-1 InvestmentFlowBlock_total(storage_electricity_0)
<= 0

c_e_GenericInvestmentStorageBlock_init_content_fix(storage)_:
-0.5 GenericInvestmentStorageBlock_invest(storage_0)
+1 GenericInvestmentStorageBlock_init_content(storage)
= 0

c_e_GenericInvestmentStorageBlock_balance_first(storage)_:
+1 flow(storage_electricity_0_0)
-1 flow(electricity_storage_0_0)
-1 GenericInvestmentStorageBlock_init_content(storage)
+1 GenericInvestmentStorageBlock_storage_content(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0_1)_:
+1 flow(storage_electricity_0_1)
-1 flow(electricity_storage_0_1)
-1 GenericInvestmentStorageBlock_storage_content(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0_2)_:
+1 flow(storage_electricity_0_2)
-1 flow(electricity_storage_0_2)
-1 GenericInvestmentStorageBlock_storage_content(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_balanced_cstr(storage)_:
-1 GenericInvestmentStorageBlock_init_content(storage)
+1 GenericInvestmentStorageBlock_storage_content(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(storage)_:
-1 InvestmentFlowBlock_invest(electricity_storage)
+1 InvestmentFlowBlock_invest(storage_electricity)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_0)_:
+1 InvestmentFlowBlock_total(storage_electricity_0)
-0.125 GenericInvestmentStorageBlock_total(storage_0)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_0)_:
-0.75 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_1)_:
-0.5 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_2)_:
-0.25 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_2)
<= 0

bounds
   0 <= flow(storage_electricity_0_0) <= +inf
   0 <= flow(storage_electricity_0_1) <= +inf
   0 <= flow(storage_electricity_0_2) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_0) <= +inf
   0 <= flow(electricity_storage_0_0) <= +inf
   0 <= flow(electricity_storage_0_1) <= +inf
   0 <= flow(electricity_storage_0_2) <= +inf
   0 <= InvestmentFlowBlock_invest(electricity_storage_0) <= +inf
   0 <= InvestmentFlowBlock_total(storage_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_electricity_0) <= +inf
   0 <= GenericInvestmentStorageBlock_init_content(storage) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_2) <= +inf
end
