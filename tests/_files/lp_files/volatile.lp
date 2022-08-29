\* Source Pyomo model name=Model *\

min
objective:
+150 InvestmentFlow_invest(wind_electricity)

s.t.

c_e_Bus_balance(electricity_0)_:
+1 flow(wind_electricity_0)
= 0

c_e_Bus_balance(electricity_1)_:
+1 flow(wind_electricity_1)
= 0

c_e_Bus_balance(electricity_2)_:
+1 flow(wind_electricity_2)
= 0

c_e_InvestmentFlow_fixed(wind_electricity_0)_:
-0.25 InvestmentFlow_invest(wind_electricity)
+1 flow(wind_electricity_0)
= 2.5

c_e_InvestmentFlow_fixed(wind_electricity_1)_:
-0.10000000000000001 InvestmentFlow_invest(wind_electricity)
+1 flow(wind_electricity_1)
= 1

c_e_InvestmentFlow_fixed(wind_electricity_2)_:
-0.29999999999999999 InvestmentFlow_invest(wind_electricity)
+1 flow(wind_electricity_2)
= 3

c_e_ONE_VAR_CONSTANT:
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(wind_electricity_0) <= +inf
   0 <= flow(wind_electricity_1) <= +inf
   0 <= flow(wind_electricity_2) <= +inf
   0 <= InvestmentFlow_invest(wind_electricity) <= 90
end
