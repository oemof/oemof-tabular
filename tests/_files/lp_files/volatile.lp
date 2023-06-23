\* Source Pyomo model name=Model *\

min
objective:
+150 InvestmentFlowBlock_invest(wind_electricity)

s.t.

c_e_BusBlock_balance(electricity_0)_:
+1 flow(wind_electricity_0)
= 0

c_e_BusBlock_balance(electricity_1)_:
+1 flow(wind_electricity_1)
= 0

c_e_BusBlock_balance(electricity_2)_:
+1 flow(wind_electricity_2)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_0)_:
-0.25 InvestmentFlowBlock_invest(wind_electricity)
+1 flow(wind_electricity_0)
= 2.5

c_e_InvestmentFlowBlock_fixed(wind_electricity_1)_:
-0.1 InvestmentFlowBlock_invest(wind_electricity)
+1 flow(wind_electricity_1)
= 1.0

c_e_InvestmentFlowBlock_fixed(wind_electricity_2)_:
-0.3 InvestmentFlowBlock_invest(wind_electricity)
+1 flow(wind_electricity_2)
= 3.0

bounds
   0 <= flow(wind_electricity_0) <= +inf
   0 <= flow(wind_electricity_1) <= +inf
   0 <= flow(wind_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_invest(wind_electricity) <= 90
end
