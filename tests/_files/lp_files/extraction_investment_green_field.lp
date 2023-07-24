\* Source Pyomo model name=Model *\

min 
objective:
+50 InvestmentFlowBlock_invest(extraction_electricity_0)
+0.6 flow(gas_extraction_0_0)
+0.6 flow(gas_extraction_0_1)
+0.6 flow(gas_extraction_0_2)

s.t.

c_e_BusBlock_balance(gas_0_0)_:
+1 flow(gas_extraction_0_0)
= 0

c_e_BusBlock_balance(gas_0_1)_:
+1 flow(gas_extraction_0_1)
= 0

c_e_BusBlock_balance(gas_0_2)_:
+1 flow(gas_extraction_0_2)
= 0

c_e_BusBlock_balance(heat_0_0)_:
+1 flow(extraction_heat_0_0)
= 0

c_e_BusBlock_balance(heat_0_1)_:
+1 flow(extraction_heat_0_1)
= 0

c_e_BusBlock_balance(heat_0_2)_:
+1 flow(extraction_heat_0_2)
= 0

c_e_BusBlock_balance(electricity_0_0)_:
+1 flow(extraction_electricity_0_0)
= 0

c_e_BusBlock_balance(electricity_0_1)_:
+1 flow(extraction_electricity_0_1)
= 0

c_e_BusBlock_balance(electricity_0_2)_:
+1 flow(extraction_electricity_0_2)
= 0

c_e_InvestmentFlowBlock_total_rule(extraction_electricity_0)_:
-1 InvestmentFlowBlock_invest(extraction_electricity_0)
+1 InvestmentFlowBlock_total(extraction_electricity_0)
= 0

c_u_InvestmentFlowBlock_max(extraction_electricity_0_0)_:
+1 flow(extraction_electricity_0_0)
-1 InvestmentFlowBlock_total(extraction_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(extraction_electricity_0_1)_:
+1 flow(extraction_electricity_0_1)
-1 InvestmentFlowBlock_total(extraction_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(extraction_electricity_0_2)_:
+1 flow(extraction_electricity_0_2)
-1 InvestmentFlowBlock_total(extraction_electricity_0)
<= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_0_0)_:
+1 flow(gas_extraction_0_0)
-0.5714285714285713 flow(extraction_heat_0_0)
-2.0 flow(extraction_electricity_0_0)
= 0.0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_0_1)_:
+1 flow(gas_extraction_0_1)
-0.5714285714285713 flow(extraction_heat_0_1)
-2.0 flow(extraction_electricity_0_1)
= 0.0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_0_2)_:
+1 flow(gas_extraction_0_2)
-0.5714285714285713 flow(extraction_heat_0_2)
-2.0 flow(extraction_electricity_0_2)
= 0.0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(extraction_0_0)_:
+1.142857142857143 flow(extraction_heat_0_0)
-1 flow(extraction_electricity_0_0)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(extraction_0_1)_:
+1.142857142857143 flow(extraction_heat_0_1)
-1 flow(extraction_electricity_0_1)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(extraction_0_2)_:
+1.142857142857143 flow(extraction_heat_0_2)
-1 flow(extraction_electricity_0_2)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(extraction_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_total(extraction_electricity_0) <= +inf
   0 <= flow(gas_extraction_0_0) <= +inf
   0 <= flow(gas_extraction_0_1) <= +inf
   0 <= flow(gas_extraction_0_2) <= +inf
   0 <= flow(extraction_heat_0_0) <= +inf
   0 <= flow(extraction_heat_0_1) <= +inf
   0 <= flow(extraction_heat_0_2) <= +inf
   0 <= flow(extraction_electricity_0_0) <= +inf
   0 <= flow(extraction_electricity_0_1) <= +inf
   0 <= flow(extraction_electricity_0_2) <= +inf
end
