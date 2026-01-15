\* Source Pyomo model name=Model *\

min 
objective:
+450000 ONE_VAR_CONSTANT
+650.0 InvestmentFlowBlock_invest(extraction_electricity_0)
+359.92657536218167 InvestmentFlowBlock_invest(extraction_electricity_1)
+32.99787833947502 InvestmentFlowBlock_invest(extraction_electricity_2)
+0.6 flow(gas_extraction_0)
+0.6 flow(gas_extraction_1)
+0.6 flow(gas_extraction_2)
+0.49220897992509305 flow(gas_extraction_3)
+0.49220897992509305 flow(gas_extraction_4)
+0.49220897992509305 flow(gas_extraction_5)
+0.40378279986483445 flow(gas_extraction_6)
+0.40378279986483445 flow(gas_extraction_7)
+0.40378279986483445 flow(gas_extraction_8)

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

c_e_BusBlock_balance(electricity_3)_:
+1 flow(extraction_electricity_3)
= 0

c_e_BusBlock_balance(electricity_4)_:
+1 flow(extraction_electricity_4)
= 0

c_e_BusBlock_balance(electricity_5)_:
+1 flow(extraction_electricity_5)
= 0

c_e_BusBlock_balance(electricity_6)_:
+1 flow(extraction_electricity_6)
= 0

c_e_BusBlock_balance(electricity_7)_:
+1 flow(extraction_electricity_7)
= 0

c_e_BusBlock_balance(electricity_8)_:
+1 flow(extraction_electricity_8)
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

c_e_BusBlock_balance(gas_3)_:
+1 flow(gas_extraction_3)
= 0

c_e_BusBlock_balance(gas_4)_:
+1 flow(gas_extraction_4)
= 0

c_e_BusBlock_balance(gas_5)_:
+1 flow(gas_extraction_5)
= 0

c_e_BusBlock_balance(gas_6)_:
+1 flow(gas_extraction_6)
= 0

c_e_BusBlock_balance(gas_7)_:
+1 flow(gas_extraction_7)
= 0

c_e_BusBlock_balance(gas_8)_:
+1 flow(gas_extraction_8)
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

c_e_BusBlock_balance(heat_3)_:
+1 flow(extraction_heat_3)
= 0

c_e_BusBlock_balance(heat_4)_:
+1 flow(extraction_heat_4)
= 0

c_e_BusBlock_balance(heat_5)_:
+1 flow(extraction_heat_5)
= 0

c_e_BusBlock_balance(heat_6)_:
+1 flow(extraction_heat_6)
= 0

c_e_BusBlock_balance(heat_7)_:
+1 flow(extraction_heat_7)
= 0

c_e_BusBlock_balance(heat_8)_:
+1 flow(extraction_heat_8)
= 0

c_e_InvestmentFlowBlock_total_rule(extraction_electricity_0)_:
-1 InvestmentFlowBlock_invest(extraction_electricity_0)
+1 InvestmentFlowBlock_total(extraction_electricity_0)
= 1000

c_e_InvestmentFlowBlock_total_rule(extraction_electricity_1)_:
-1 InvestmentFlowBlock_invest(extraction_electricity_1)
-1 InvestmentFlowBlock_total(extraction_electricity_0)
+1 InvestmentFlowBlock_total(extraction_electricity_1)
+1 InvestmentFlowBlock_old(extraction_electricity_1)
= 0

c_e_InvestmentFlowBlock_total_rule(extraction_electricity_2)_:
-1 InvestmentFlowBlock_invest(extraction_electricity_2)
-1 InvestmentFlowBlock_total(extraction_electricity_1)
+1 InvestmentFlowBlock_total(extraction_electricity_2)
+1 InvestmentFlowBlock_old(extraction_electricity_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(extraction_electricity_0)_:
+1 InvestmentFlowBlock_old_end(extraction_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(extraction_electricity_1)_:
+1 InvestmentFlowBlock_old_end(extraction_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(extraction_electricity_2)_:
-1 InvestmentFlowBlock_invest(extraction_electricity_0)
+1 InvestmentFlowBlock_old_end(extraction_electricity_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(extraction_electricity_0)_:
+1 InvestmentFlowBlock_old_exo(extraction_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(extraction_electricity_1)_:
+1 InvestmentFlowBlock_old_exo(extraction_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(extraction_electricity_2)_:
+1 InvestmentFlowBlock_old_exo(extraction_electricity_2)
= 1000

c_e_InvestmentFlowBlock_old_rule(extraction_electricity_0)_:
+1 InvestmentFlowBlock_old(extraction_electricity_0)
-1 InvestmentFlowBlock_old_end(extraction_electricity_0)
-1 InvestmentFlowBlock_old_exo(extraction_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule(extraction_electricity_1)_:
+1 InvestmentFlowBlock_old(extraction_electricity_1)
-1 InvestmentFlowBlock_old_end(extraction_electricity_1)
-1 InvestmentFlowBlock_old_exo(extraction_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule(extraction_electricity_2)_:
+1 InvestmentFlowBlock_old(extraction_electricity_2)
-1 InvestmentFlowBlock_old_end(extraction_electricity_2)
-1 InvestmentFlowBlock_old_exo(extraction_electricity_2)
= 0

c_u_InvestmentFlowBlock_max(extraction_electricity_0_0)_:
+1 flow(extraction_electricity_0)
-1 InvestmentFlowBlock_total(extraction_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(extraction_electricity_0_1)_:
+1 flow(extraction_electricity_1)
-1 InvestmentFlowBlock_total(extraction_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(extraction_electricity_0_2)_:
+1 flow(extraction_electricity_2)
-1 InvestmentFlowBlock_total(extraction_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(extraction_electricity_1_3)_:
+1 flow(extraction_electricity_3)
-1 InvestmentFlowBlock_total(extraction_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(extraction_electricity_1_4)_:
+1 flow(extraction_electricity_4)
-1 InvestmentFlowBlock_total(extraction_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(extraction_electricity_1_5)_:
+1 flow(extraction_electricity_5)
-1 InvestmentFlowBlock_total(extraction_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(extraction_electricity_2_6)_:
+1 flow(extraction_electricity_6)
-1 InvestmentFlowBlock_total(extraction_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(extraction_electricity_2_7)_:
+1 flow(extraction_electricity_7)
-1 InvestmentFlowBlock_total(extraction_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(extraction_electricity_2_8)_:
+1 flow(extraction_electricity_8)
-1 InvestmentFlowBlock_total(extraction_electricity_2)
<= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_0)_:
+1 flow(gas_extraction_0)
-2.0 flow(extraction_electricity_0)
-0.5714285714285713 flow(extraction_heat_0)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_1)_:
+1 flow(gas_extraction_1)
-2.0 flow(extraction_electricity_1)
-0.5714285714285713 flow(extraction_heat_1)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_2)_:
+1 flow(gas_extraction_2)
-2.0 flow(extraction_electricity_2)
-0.5714285714285713 flow(extraction_heat_2)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_3)_:
+1 flow(gas_extraction_3)
-2.0 flow(extraction_electricity_3)
-0.5714285714285713 flow(extraction_heat_3)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_4)_:
+1 flow(gas_extraction_4)
-2.0 flow(extraction_electricity_4)
-0.5714285714285713 flow(extraction_heat_4)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_5)_:
+1 flow(gas_extraction_5)
-2.0 flow(extraction_electricity_5)
-0.5714285714285713 flow(extraction_heat_5)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_6)_:
+1 flow(gas_extraction_6)
-2.0 flow(extraction_electricity_6)
-0.5714285714285713 flow(extraction_heat_6)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_7)_:
+1 flow(gas_extraction_7)
-2.0 flow(extraction_electricity_7)
-0.5714285714285713 flow(extraction_heat_7)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_8)_:
+1 flow(gas_extraction_8)
-2.0 flow(extraction_electricity_8)
-0.5714285714285713 flow(extraction_heat_8)
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

c_u_ExtractionTurbineCHPBlock_out_flow_relation(extraction_3)_:
-1 flow(extraction_electricity_3)
+1.142857142857143 flow(extraction_heat_3)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(extraction_4)_:
-1 flow(extraction_electricity_4)
+1.142857142857143 flow(extraction_heat_4)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(extraction_5)_:
-1 flow(extraction_electricity_5)
+1.142857142857143 flow(extraction_heat_5)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(extraction_6)_:
-1 flow(extraction_electricity_6)
+1.142857142857143 flow(extraction_heat_6)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(extraction_7)_:
-1 flow(extraction_electricity_7)
+1.142857142857143 flow(extraction_heat_7)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(extraction_8)_:
-1 flow(extraction_electricity_8)
+1.142857142857143 flow(extraction_heat_8)
<= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= InvestmentFlowBlock_invest(extraction_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_invest(extraction_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_invest(extraction_electricity_2) <= +inf
   0 <= flow(gas_extraction_0) <= +inf
   0 <= flow(gas_extraction_1) <= +inf
   0 <= flow(gas_extraction_2) <= +inf
   0 <= flow(gas_extraction_3) <= +inf
   0 <= flow(gas_extraction_4) <= +inf
   0 <= flow(gas_extraction_5) <= +inf
   0 <= flow(gas_extraction_6) <= +inf
   0 <= flow(gas_extraction_7) <= +inf
   0 <= flow(gas_extraction_8) <= +inf
   0 <= flow(extraction_electricity_0) <= +inf
   0 <= flow(extraction_electricity_1) <= +inf
   0 <= flow(extraction_electricity_2) <= +inf
   0 <= flow(extraction_electricity_3) <= +inf
   0 <= flow(extraction_electricity_4) <= +inf
   0 <= flow(extraction_electricity_5) <= +inf
   0 <= flow(extraction_electricity_6) <= +inf
   0 <= flow(extraction_electricity_7) <= +inf
   0 <= flow(extraction_electricity_8) <= +inf
   0 <= flow(extraction_heat_0) <= +inf
   0 <= flow(extraction_heat_1) <= +inf
   0 <= flow(extraction_heat_2) <= +inf
   0 <= flow(extraction_heat_3) <= +inf
   0 <= flow(extraction_heat_4) <= +inf
   0 <= flow(extraction_heat_5) <= +inf
   0 <= flow(extraction_heat_6) <= +inf
   0 <= flow(extraction_heat_7) <= +inf
   0 <= flow(extraction_heat_8) <= +inf
   0 <= InvestmentFlowBlock_total(extraction_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_total(extraction_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_total(extraction_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old(extraction_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_old(extraction_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old(extraction_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(extraction_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(extraction_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(extraction_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(extraction_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(extraction_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(extraction_electricity_2) <= +inf
end
