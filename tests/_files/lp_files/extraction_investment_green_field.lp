\* Source Pyomo model name=Model *\

min
objective:
+50 InvestmentFlowBlock_invest(extraction_electricity)
+0.59999999999999998 flow(gas_extraction_0)
+0.59999999999999998 flow(gas_extraction_1)
+0.59999999999999998 flow(gas_extraction_2)

s.t.

c_e_BusBlock_balance(electricity_0)_:
+1 flow(extraction_electricity_0)
= 0

c_e_BusBlock_balance(electricity_1)_:
+1 flow(extraction_electricity_1)
= 0

c_e_BusBlock_balance(electricity_2)_:
+1 flow(extraction_electricity_2)
= 0

c_e_BusBlock_balance(gas_0)_:
+1 flow(gas_extraction_0)
= 0

c_e_BusBlock_balance(gas_1)_:
+1 flow(gas_extraction_1)
= 0

c_e_BusBlock_balance(gas_2)_:
+1 flow(gas_extraction_2)
= 0

c_e_BusBlock_balance(heat_0)_:
+1 flow(extraction_heat_0)
= 0

c_e_BusBlock_balance(heat_1)_:
+1 flow(extraction_heat_1)
= 0

c_e_BusBlock_balance(heat_2)_:
+1 flow(extraction_heat_2)
= 0

c_u_InvestmentFlowBlock_max(extraction_electricity_0)_:
-1 InvestmentFlowBlock_invest(extraction_electricity)
+1 flow(extraction_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(extraction_electricity_1)_:
-1 InvestmentFlowBlock_invest(extraction_electricity)
+1 flow(extraction_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(extraction_electricity_2)_:
-1 InvestmentFlowBlock_invest(extraction_electricity)
+1 flow(extraction_electricity_2)
<= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_0)_:
-2 flow(extraction_electricity_0)
-0.57142857142857129 flow(extraction_heat_0)
+1 flow(gas_extraction_0)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_1)_:
-2 flow(extraction_electricity_1)
-0.57142857142857129 flow(extraction_heat_1)
+1 flow(gas_extraction_1)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_2)_:
-2 flow(extraction_electricity_2)
-0.57142857142857129 flow(extraction_heat_2)
+1 flow(gas_extraction_2)
= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(extraction_0)_:
-1 flow(extraction_electricity_0)
+1.142857142857143 flow(extraction_heat_0)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(extraction_1)_:
-1 flow(extraction_electricity_1)
+1.142857142857143 flow(extraction_heat_1)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(extraction_2)_:
-1 flow(extraction_electricity_2)
+1.142857142857143 flow(extraction_heat_2)
<= 0

c_e_ONE_VAR_CONSTANT:
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(extraction_electricity_0) <= +inf
   0 <= flow(extraction_electricity_1) <= +inf
   0 <= flow(extraction_electricity_2) <= +inf
   0 <= flow(extraction_heat_0) <= +inf
   0 <= flow(extraction_heat_1) <= +inf
   0 <= flow(extraction_heat_2) <= +inf
   0 <= flow(gas_extraction_0) <= +inf
   0 <= flow(gas_extraction_1) <= +inf
   0 <= flow(gas_extraction_2) <= +inf
   0 <= InvestmentFlowBlock_invest(extraction_electricity) <= +inf
end
