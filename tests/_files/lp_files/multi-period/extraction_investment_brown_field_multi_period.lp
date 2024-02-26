\* Source Pyomo model name=Model *\

min 
objective:
+393187.4631175658 ONE_VAR_CONSTANT
+550.3538603446715 InvestmentFlowBlock_invest(extraction_electricity_0)
+226.09002140491177 InvestmentFlowBlock_invest(extraction_electricity_1)
+15.604198638169356 InvestmentFlowBlock_invest(extraction_electricity_2)
+0.6 flow(gas_extraction_0_0)
+0.6 flow(gas_extraction_0_1)
+0.6 flow(gas_extraction_0_2)
+0.49220897992509305 flow(gas_extraction_1_3)
+0.49220897992509305 flow(gas_extraction_1_4)
+0.49220897992509305 flow(gas_extraction_1_5)
+0.40378279986483445 flow(gas_extraction_2_6)
+0.40378279986483445 flow(gas_extraction_2_7)
+0.40378279986483445 flow(gas_extraction_2_8)

s.t.

c_e_BusBlock_balance(electricity_0_0)_:
+1 flow(extraction_electricity_0_0)
= 0

c_e_BusBlock_balance(electricity_0_1)_:
+1 flow(extraction_electricity_0_1)
= 0

c_e_BusBlock_balance(electricity_0_2)_:
+1 flow(extraction_electricity_0_2)
= 0

c_e_BusBlock_balance(electricity_1_3)_:
+1 flow(extraction_electricity_1_3)
= 0

c_e_BusBlock_balance(electricity_1_4)_:
+1 flow(extraction_electricity_1_4)
= 0

c_e_BusBlock_balance(electricity_1_5)_:
+1 flow(extraction_electricity_1_5)
= 0

c_e_BusBlock_balance(electricity_2_6)_:
+1 flow(extraction_electricity_2_6)
= 0

c_e_BusBlock_balance(electricity_2_7)_:
+1 flow(extraction_electricity_2_7)
= 0

c_e_BusBlock_balance(electricity_2_8)_:
+1 flow(extraction_electricity_2_8)
= 0

c_e_BusBlock_balance(gas_0_0)_:
+1 flow(gas_extraction_0_0)
= 0

c_e_BusBlock_balance(gas_0_1)_:
+1 flow(gas_extraction_0_1)
= 0

c_e_BusBlock_balance(gas_0_2)_:
+1 flow(gas_extraction_0_2)
= 0

c_e_BusBlock_balance(gas_1_3)_:
+1 flow(gas_extraction_1_3)
= 0

c_e_BusBlock_balance(gas_1_4)_:
+1 flow(gas_extraction_1_4)
= 0

c_e_BusBlock_balance(gas_1_5)_:
+1 flow(gas_extraction_1_5)
= 0

c_e_BusBlock_balance(gas_2_6)_:
+1 flow(gas_extraction_2_6)
= 0

c_e_BusBlock_balance(gas_2_7)_:
+1 flow(gas_extraction_2_7)
= 0

c_e_BusBlock_balance(gas_2_8)_:
+1 flow(gas_extraction_2_8)
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

c_e_BusBlock_balance(heat_1_3)_:
+1 flow(extraction_heat_1_3)
= 0

c_e_BusBlock_balance(heat_1_4)_:
+1 flow(extraction_heat_1_4)
= 0

c_e_BusBlock_balance(heat_1_5)_:
+1 flow(extraction_heat_1_5)
= 0

c_e_BusBlock_balance(heat_2_6)_:
+1 flow(extraction_heat_2_6)
= 0

c_e_BusBlock_balance(heat_2_7)_:
+1 flow(extraction_heat_2_7)
= 0

c_e_BusBlock_balance(heat_2_8)_:
+1 flow(extraction_heat_2_8)
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

c_u_InvestmentFlowBlock_max(extraction_electricity_1_3)_:
+1 flow(extraction_electricity_1_3)
-1 InvestmentFlowBlock_total(extraction_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(extraction_electricity_1_4)_:
+1 flow(extraction_electricity_1_4)
-1 InvestmentFlowBlock_total(extraction_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(extraction_electricity_1_5)_:
+1 flow(extraction_electricity_1_5)
-1 InvestmentFlowBlock_total(extraction_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(extraction_electricity_2_6)_:
+1 flow(extraction_electricity_2_6)
-1 InvestmentFlowBlock_total(extraction_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(extraction_electricity_2_7)_:
+1 flow(extraction_electricity_2_7)
-1 InvestmentFlowBlock_total(extraction_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(extraction_electricity_2_8)_:
+1 flow(extraction_electricity_2_8)
-1 InvestmentFlowBlock_total(extraction_electricity_2)
<= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_0_0)_:
+1 flow(gas_extraction_0_0)
-2.0 flow(extraction_electricity_0_0)
-0.5714285714285713 flow(extraction_heat_0_0)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_0_1)_:
+1 flow(gas_extraction_0_1)
-2.0 flow(extraction_electricity_0_1)
-0.5714285714285713 flow(extraction_heat_0_1)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_0_2)_:
+1 flow(gas_extraction_0_2)
-2.0 flow(extraction_electricity_0_2)
-0.5714285714285713 flow(extraction_heat_0_2)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_1_3)_:
+1 flow(gas_extraction_1_3)
-2.0 flow(extraction_electricity_1_3)
-0.5714285714285713 flow(extraction_heat_1_3)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_1_4)_:
+1 flow(gas_extraction_1_4)
-2.0 flow(extraction_electricity_1_4)
-0.5714285714285713 flow(extraction_heat_1_4)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_1_5)_:
+1 flow(gas_extraction_1_5)
-2.0 flow(extraction_electricity_1_5)
-0.5714285714285713 flow(extraction_heat_1_5)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_2_6)_:
+1 flow(gas_extraction_2_6)
-2.0 flow(extraction_electricity_2_6)
-0.5714285714285713 flow(extraction_heat_2_6)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_2_7)_:
+1 flow(gas_extraction_2_7)
-2.0 flow(extraction_electricity_2_7)
-0.5714285714285713 flow(extraction_heat_2_7)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(extraction_2_8)_:
+1 flow(gas_extraction_2_8)
-2.0 flow(extraction_electricity_2_8)
-0.5714285714285713 flow(extraction_heat_2_8)
= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(extraction_0_0)_:
-1 flow(extraction_electricity_0_0)
+1.142857142857143 flow(extraction_heat_0_0)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(extraction_0_1)_:
-1 flow(extraction_electricity_0_1)
+1.142857142857143 flow(extraction_heat_0_1)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(extraction_0_2)_:
-1 flow(extraction_electricity_0_2)
+1.142857142857143 flow(extraction_heat_0_2)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(extraction_1_3)_:
-1 flow(extraction_electricity_1_3)
+1.142857142857143 flow(extraction_heat_1_3)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(extraction_1_4)_:
-1 flow(extraction_electricity_1_4)
+1.142857142857143 flow(extraction_heat_1_4)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(extraction_1_5)_:
-1 flow(extraction_electricity_1_5)
+1.142857142857143 flow(extraction_heat_1_5)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(extraction_2_6)_:
-1 flow(extraction_electricity_2_6)
+1.142857142857143 flow(extraction_heat_2_6)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(extraction_2_7)_:
-1 flow(extraction_electricity_2_7)
+1.142857142857143 flow(extraction_heat_2_7)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(extraction_2_8)_:
-1 flow(extraction_electricity_2_8)
+1.142857142857143 flow(extraction_heat_2_8)
<= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= InvestmentFlowBlock_invest(extraction_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_invest(extraction_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_invest(extraction_electricity_2) <= +inf
   0 <= flow(gas_extraction_0_0) <= +inf
   0 <= flow(gas_extraction_0_1) <= +inf
   0 <= flow(gas_extraction_0_2) <= +inf
   0 <= flow(gas_extraction_1_3) <= +inf
   0 <= flow(gas_extraction_1_4) <= +inf
   0 <= flow(gas_extraction_1_5) <= +inf
   0 <= flow(gas_extraction_2_6) <= +inf
   0 <= flow(gas_extraction_2_7) <= +inf
   0 <= flow(gas_extraction_2_8) <= +inf
   0 <= flow(extraction_electricity_0_0) <= +inf
   0 <= flow(extraction_electricity_0_1) <= +inf
   0 <= flow(extraction_electricity_0_2) <= +inf
   0 <= flow(extraction_electricity_1_3) <= +inf
   0 <= flow(extraction_electricity_1_4) <= +inf
   0 <= flow(extraction_electricity_1_5) <= +inf
   0 <= flow(extraction_electricity_2_6) <= +inf
   0 <= flow(extraction_electricity_2_7) <= +inf
   0 <= flow(extraction_electricity_2_8) <= +inf
   0 <= flow(extraction_heat_0_0) <= +inf
   0 <= flow(extraction_heat_0_1) <= +inf
   0 <= flow(extraction_heat_0_2) <= +inf
   0 <= flow(extraction_heat_1_3) <= +inf
   0 <= flow(extraction_heat_1_4) <= +inf
   0 <= flow(extraction_heat_1_5) <= +inf
   0 <= flow(extraction_heat_2_6) <= +inf
   0 <= flow(extraction_heat_2_7) <= +inf
   0 <= flow(extraction_heat_2_8) <= +inf
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
