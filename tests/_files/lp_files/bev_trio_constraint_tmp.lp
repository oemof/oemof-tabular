\* Source Pyomo model name=Model *\

min 
objective:
+2 InvestmentFlowBlock_invest(el_bus_BEV_inflex_storage_0)
+2 InvestmentFlowBlock_invest(el_bus_BEV_V2G_storage_0)
+2 InvestmentFlowBlock_invest(el_bus_BEV_G2V_storage_0)
+10 flow(el_bus_BEV_V2G_storage_0_0)
+10 flow(el_bus_BEV_V2G_storage_0_1)
+10 flow(el_bus_BEV_V2G_storage_0_2)
+20 flow(el_bus_BEV_inflex_storage_0_0)
+20 flow(el_bus_BEV_inflex_storage_0_1)
+20 flow(el_bus_BEV_inflex_storage_0_2)
+4 flow(el_bus_BEV_G2V_storage_0_0)
+4 flow(el_bus_BEV_G2V_storage_0_1)
+4 flow(el_bus_BEV_G2V_storage_0_2)

s.t.

c_e_BusBlock_balance(BEV_G2V_bus_0_0)_:
+1 flow(BEV_G2V_storage_BEV_G2V_bus_0_0)
-1 flow(BEV_G2V_bus_BEV_G2V_2com_0_0)
= 0

c_e_BusBlock_balance(BEV_G2V_bus_0_1)_:
+1 flow(BEV_G2V_storage_BEV_G2V_bus_0_1)
-1 flow(BEV_G2V_bus_BEV_G2V_2com_0_1)
= 0

c_e_BusBlock_balance(BEV_G2V_bus_0_2)_:
+1 flow(BEV_G2V_storage_BEV_G2V_bus_0_2)
-1 flow(BEV_G2V_bus_BEV_G2V_2com_0_2)
= 0

c_e_BusBlock_balance(BEV_V2G_bus_0_0)_:
+1 flow(BEV_V2G_storage_BEV_V2G_bus_0_0)
-1 flow(BEV_V2G_bus_BEV_V2G_v2g_0_0)
-1 flow(BEV_V2G_bus_BEV_V2G_2com_0_0)
= 0

c_e_BusBlock_balance(BEV_V2G_bus_0_1)_:
+1 flow(BEV_V2G_storage_BEV_V2G_bus_0_1)
-1 flow(BEV_V2G_bus_BEV_V2G_v2g_0_1)
-1 flow(BEV_V2G_bus_BEV_V2G_2com_0_1)
= 0

c_e_BusBlock_balance(BEV_V2G_bus_0_2)_:
+1 flow(BEV_V2G_storage_BEV_V2G_bus_0_2)
-1 flow(BEV_V2G_bus_BEV_V2G_v2g_0_2)
-1 flow(BEV_V2G_bus_BEV_V2G_2com_0_2)
= 0

c_e_BusBlock_balance(BEV_inflex_bus_0_0)_:
+1 flow(BEV_inflex_storage_BEV_inflex_bus_0_0)
-1 flow(BEV_inflex_bus_BEV_inflex_2com_0_0)
= 0

c_e_BusBlock_balance(BEV_inflex_bus_0_1)_:
+1 flow(BEV_inflex_storage_BEV_inflex_bus_0_1)
-1 flow(BEV_inflex_bus_BEV_inflex_2com_0_1)
= 0

c_e_BusBlock_balance(BEV_inflex_bus_0_2)_:
+1 flow(BEV_inflex_storage_BEV_inflex_bus_0_2)
-1 flow(BEV_inflex_bus_BEV_inflex_2com_0_2)
= 0

c_e_BusBlock_balance(el_bus_0_0)_:
-1 flow(el_bus_BEV_V2G_storage_0_0)
-1 flow(el_bus_BEV_inflex_storage_0_0)
-1 flow(el_bus_BEV_G2V_storage_0_0)
+1 flow(BEV_V2G_v2g_el_bus_0_0)
= 0

c_e_BusBlock_balance(el_bus_0_1)_:
-1 flow(el_bus_BEV_V2G_storage_0_1)
-1 flow(el_bus_BEV_inflex_storage_0_1)
-1 flow(el_bus_BEV_G2V_storage_0_1)
+1 flow(BEV_V2G_v2g_el_bus_0_1)
= 0

c_e_BusBlock_balance(el_bus_0_2)_:
-1 flow(el_bus_BEV_V2G_storage_0_2)
-1 flow(el_bus_BEV_inflex_storage_0_2)
-1 flow(el_bus_BEV_G2V_storage_0_2)
+1 flow(BEV_V2G_v2g_el_bus_0_2)
= 0

c_e_BusBlock_balance(pkm_bus_0_0)_:
+1 flow(BEV_V2G_2com_pkm_bus_0_0)
+1 flow(BEV_inflex_2com_pkm_bus_0_0)
+1 flow(BEV_G2V_2com_pkm_bus_0_0)
= 0

c_e_BusBlock_balance(pkm_bus_0_1)_:
+1 flow(BEV_V2G_2com_pkm_bus_0_1)
+1 flow(BEV_inflex_2com_pkm_bus_0_1)
+1 flow(BEV_G2V_2com_pkm_bus_0_1)
= 200

c_e_BusBlock_balance(pkm_bus_0_2)_:
+1 flow(BEV_V2G_2com_pkm_bus_0_2)
+1 flow(BEV_inflex_2com_pkm_bus_0_2)
+1 flow(BEV_G2V_2com_pkm_bus_0_2)
= 0

c_e_ConverterBlock_relation(BEV_V2G_v2g_BEV_V2G_bus_el_bus_0_0)_:
+0.8333333333333334 flow(BEV_V2G_bus_BEV_V2G_v2g_0_0)
-1 flow(BEV_V2G_v2g_el_bus_0_0)
= 0

c_e_ConverterBlock_relation(BEV_inflex_2com_BEV_inflex_bus_pkm_bus_0_0)_:
+0.6944444444444445 flow(BEV_inflex_bus_BEV_inflex_2com_0_0)
-1 flow(BEV_inflex_2com_pkm_bus_0_0)
= 0

c_e_ConverterBlock_relation(BEV_G2V_2com_BEV_G2V_bus_pkm_bus_0_0)_:
+0.6944444444444445 flow(BEV_G2V_bus_BEV_G2V_2com_0_0)
-1 flow(BEV_G2V_2com_pkm_bus_0_0)
= 0

c_e_ConverterBlock_relation(BEV_V2G_2com_BEV_V2G_bus_pkm_bus_0_0)_:
+0.6944444444444445 flow(BEV_V2G_bus_BEV_V2G_2com_0_0)
-1 flow(BEV_V2G_2com_pkm_bus_0_0)
= 0

c_e_ConverterBlock_relation(BEV_V2G_v2g_BEV_V2G_bus_el_bus_0_1)_:
+0.8333333333333334 flow(BEV_V2G_bus_BEV_V2G_v2g_0_1)
-1 flow(BEV_V2G_v2g_el_bus_0_1)
= 0

c_e_ConverterBlock_relation(BEV_inflex_2com_BEV_inflex_bus_pkm_bus_0_1)_:
+0.6944444444444445 flow(BEV_inflex_bus_BEV_inflex_2com_0_1)
-1 flow(BEV_inflex_2com_pkm_bus_0_1)
= 0

c_e_ConverterBlock_relation(BEV_G2V_2com_BEV_G2V_bus_pkm_bus_0_1)_:
+0.6944444444444445 flow(BEV_G2V_bus_BEV_G2V_2com_0_1)
-1 flow(BEV_G2V_2com_pkm_bus_0_1)
= 0

c_e_ConverterBlock_relation(BEV_V2G_2com_BEV_V2G_bus_pkm_bus_0_1)_:
+0.6944444444444445 flow(BEV_V2G_bus_BEV_V2G_2com_0_1)
-1 flow(BEV_V2G_2com_pkm_bus_0_1)
= 0

c_e_ConverterBlock_relation(BEV_V2G_v2g_BEV_V2G_bus_el_bus_0_2)_:
+0.8333333333333334 flow(BEV_V2G_bus_BEV_V2G_v2g_0_2)
-1 flow(BEV_V2G_v2g_el_bus_0_2)
= 0

c_e_ConverterBlock_relation(BEV_inflex_2com_BEV_inflex_bus_pkm_bus_0_2)_:
+0.6944444444444445 flow(BEV_inflex_bus_BEV_inflex_2com_0_2)
-1 flow(BEV_inflex_2com_pkm_bus_0_2)
= 0

c_e_ConverterBlock_relation(BEV_G2V_2com_BEV_G2V_bus_pkm_bus_0_2)_:
+0.6944444444444445 flow(BEV_G2V_bus_BEV_G2V_2com_0_2)
-1 flow(BEV_G2V_2com_pkm_bus_0_2)
= 0

c_e_ConverterBlock_relation(BEV_V2G_2com_BEV_V2G_bus_pkm_bus_0_2)_:
+0.6944444444444445 flow(BEV_V2G_bus_BEV_V2G_2com_0_2)
-1 flow(BEV_V2G_2com_pkm_bus_0_2)
= 0

c_e_InvestmentFlowBlock_total_rule(el_bus_BEV_inflex_storage_0)_:
-1 InvestmentFlowBlock_invest(el_bus_BEV_inflex_storage_0)
+1 InvestmentFlowBlock_total(el_bus_BEV_inflex_storage_0)
= 0

c_e_InvestmentFlowBlock_total_rule(el_bus_BEV_V2G_storage_0)_:
-1 InvestmentFlowBlock_invest(el_bus_BEV_V2G_storage_0)
+1 InvestmentFlowBlock_total(el_bus_BEV_V2G_storage_0)
= 0

c_e_InvestmentFlowBlock_total_rule(BEV_G2V_storage_BEV_G2V_bus_0)_:
-1 InvestmentFlowBlock_invest(BEV_G2V_storage_BEV_G2V_bus_0)
+1 InvestmentFlowBlock_total(BEV_G2V_storage_BEV_G2V_bus_0)
= 0

c_e_InvestmentFlowBlock_total_rule(el_bus_BEV_G2V_storage_0)_:
-1 InvestmentFlowBlock_invest(el_bus_BEV_G2V_storage_0)
+1 InvestmentFlowBlock_total(el_bus_BEV_G2V_storage_0)
= 0

c_e_InvestmentFlowBlock_total_rule(BEV_inflex_2com_pkm_bus_0)_:
-1 InvestmentFlowBlock_invest(BEV_inflex_2com_pkm_bus_0)
+1 InvestmentFlowBlock_total(BEV_inflex_2com_pkm_bus_0)
= 0

c_e_InvestmentFlowBlock_total_rule(BEV_V2G_storage_BEV_V2G_bus_0)_:
-1 InvestmentFlowBlock_invest(BEV_V2G_storage_BEV_V2G_bus_0)
+1 InvestmentFlowBlock_total(BEV_V2G_storage_BEV_V2G_bus_0)
= 0

c_e_InvestmentFlowBlock_total_rule(BEV_inflex_storage_BEV_inflex_bus_0)_:
-1 InvestmentFlowBlock_invest(BEV_inflex_storage_BEV_inflex_bus_0)
+1 InvestmentFlowBlock_total(BEV_inflex_storage_BEV_inflex_bus_0)
= 0

c_e_InvestmentFlowBlock_total_rule(BEV_V2G_2com_pkm_bus_0)_:
-1 InvestmentFlowBlock_invest(BEV_V2G_2com_pkm_bus_0)
+1 InvestmentFlowBlock_total(BEV_V2G_2com_pkm_bus_0)
= 0

c_e_InvestmentFlowBlock_total_rule(BEV_V2G_v2g_el_bus_0)_:
-1 InvestmentFlowBlock_invest(BEV_V2G_v2g_el_bus_0)
+1 InvestmentFlowBlock_total(BEV_V2G_v2g_el_bus_0)
= 0

c_e_InvestmentFlowBlock_total_rule(BEV_G2V_2com_pkm_bus_0)_:
-1 InvestmentFlowBlock_invest(BEV_G2V_2com_pkm_bus_0)
+1 InvestmentFlowBlock_total(BEV_G2V_2com_pkm_bus_0)
= 0

c_e_InvestmentFlowBlock_fixed(el_bus_BEV_inflex_storage_0_0)_:
+1 flow(el_bus_BEV_inflex_storage_0_0)
-0.89856 InvestmentFlowBlock_total(el_bus_BEV_inflex_storage_0)
= 0

c_e_InvestmentFlowBlock_fixed(el_bus_BEV_inflex_storage_0_1)_:
+1 flow(el_bus_BEV_inflex_storage_0_1)
= 0

c_e_InvestmentFlowBlock_fixed(el_bus_BEV_inflex_storage_0_2)_:
+1 flow(el_bus_BEV_inflex_storage_0_2)
= 0

c_e_InvestmentFlowBlock_fixed(BEV_inflex_storage_BEV_inflex_bus_0_0)_:
+1 flow(BEV_inflex_storage_BEV_inflex_bus_0_0)
-0.16 InvestmentFlowBlock_total(BEV_inflex_storage_BEV_inflex_bus_0)
= 0

c_e_InvestmentFlowBlock_fixed(BEV_inflex_storage_BEV_inflex_bus_0_1)_:
+1 flow(BEV_inflex_storage_BEV_inflex_bus_0_1)
-0.08 InvestmentFlowBlock_total(BEV_inflex_storage_BEV_inflex_bus_0)
= 0

c_e_InvestmentFlowBlock_fixed(BEV_inflex_storage_BEV_inflex_bus_0_2)_:
+1 flow(BEV_inflex_storage_BEV_inflex_bus_0_2)
-0.16 InvestmentFlowBlock_total(BEV_inflex_storage_BEV_inflex_bus_0)
= 0

c_u_InvestmentFlowBlock_max(el_bus_BEV_V2G_storage_0_0)_:
+1 flow(el_bus_BEV_V2G_storage_0_0)
-1 InvestmentFlowBlock_total(el_bus_BEV_V2G_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(el_bus_BEV_V2G_storage_0_1)_:
+1 flow(el_bus_BEV_V2G_storage_0_1)
-1 InvestmentFlowBlock_total(el_bus_BEV_V2G_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(el_bus_BEV_V2G_storage_0_2)_:
+1 flow(el_bus_BEV_V2G_storage_0_2)
-1 InvestmentFlowBlock_total(el_bus_BEV_V2G_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_G2V_storage_BEV_G2V_bus_0_0)_:
+1 flow(BEV_G2V_storage_BEV_G2V_bus_0_0)
-1 InvestmentFlowBlock_total(BEV_G2V_storage_BEV_G2V_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_G2V_storage_BEV_G2V_bus_0_1)_:
+1 flow(BEV_G2V_storage_BEV_G2V_bus_0_1)
-1 InvestmentFlowBlock_total(BEV_G2V_storage_BEV_G2V_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_G2V_storage_BEV_G2V_bus_0_2)_:
+1 flow(BEV_G2V_storage_BEV_G2V_bus_0_2)
-1 InvestmentFlowBlock_total(BEV_G2V_storage_BEV_G2V_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(el_bus_BEV_G2V_storage_0_0)_:
+1 flow(el_bus_BEV_G2V_storage_0_0)
-1 InvestmentFlowBlock_total(el_bus_BEV_G2V_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(el_bus_BEV_G2V_storage_0_1)_:
+1 flow(el_bus_BEV_G2V_storage_0_1)
-1 InvestmentFlowBlock_total(el_bus_BEV_G2V_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(el_bus_BEV_G2V_storage_0_2)_:
+1 flow(el_bus_BEV_G2V_storage_0_2)
-1 InvestmentFlowBlock_total(el_bus_BEV_G2V_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_inflex_2com_pkm_bus_0_0)_:
+1 flow(BEV_inflex_2com_pkm_bus_0_0)
-1 InvestmentFlowBlock_total(BEV_inflex_2com_pkm_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_inflex_2com_pkm_bus_0_1)_:
+1 flow(BEV_inflex_2com_pkm_bus_0_1)
-1 InvestmentFlowBlock_total(BEV_inflex_2com_pkm_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_inflex_2com_pkm_bus_0_2)_:
+1 flow(BEV_inflex_2com_pkm_bus_0_2)
-1 InvestmentFlowBlock_total(BEV_inflex_2com_pkm_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_storage_BEV_V2G_bus_0_0)_:
+1 flow(BEV_V2G_storage_BEV_V2G_bus_0_0)
-1 InvestmentFlowBlock_total(BEV_V2G_storage_BEV_V2G_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_storage_BEV_V2G_bus_0_1)_:
+1 flow(BEV_V2G_storage_BEV_V2G_bus_0_1)
-1 InvestmentFlowBlock_total(BEV_V2G_storage_BEV_V2G_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_storage_BEV_V2G_bus_0_2)_:
+1 flow(BEV_V2G_storage_BEV_V2G_bus_0_2)
-1 InvestmentFlowBlock_total(BEV_V2G_storage_BEV_V2G_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_2com_pkm_bus_0_0)_:
+1 flow(BEV_V2G_2com_pkm_bus_0_0)
-1 InvestmentFlowBlock_total(BEV_V2G_2com_pkm_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_2com_pkm_bus_0_1)_:
+1 flow(BEV_V2G_2com_pkm_bus_0_1)
-1 InvestmentFlowBlock_total(BEV_V2G_2com_pkm_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_2com_pkm_bus_0_2)_:
+1 flow(BEV_V2G_2com_pkm_bus_0_2)
-1 InvestmentFlowBlock_total(BEV_V2G_2com_pkm_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_v2g_el_bus_0_0)_:
+1 flow(BEV_V2G_v2g_el_bus_0_0)
-1 InvestmentFlowBlock_total(BEV_V2G_v2g_el_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_v2g_el_bus_0_1)_:
+1 flow(BEV_V2G_v2g_el_bus_0_1)
-1 InvestmentFlowBlock_total(BEV_V2G_v2g_el_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_v2g_el_bus_0_2)_:
+1 flow(BEV_V2G_v2g_el_bus_0_2)
-1 InvestmentFlowBlock_total(BEV_V2G_v2g_el_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_G2V_2com_pkm_bus_0_0)_:
+1 flow(BEV_G2V_2com_pkm_bus_0_0)
-1 InvestmentFlowBlock_total(BEV_G2V_2com_pkm_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_G2V_2com_pkm_bus_0_1)_:
+1 flow(BEV_G2V_2com_pkm_bus_0_1)
-1 InvestmentFlowBlock_total(BEV_G2V_2com_pkm_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_G2V_2com_pkm_bus_0_2)_:
+1 flow(BEV_G2V_2com_pkm_bus_0_2)
-1 InvestmentFlowBlock_total(BEV_G2V_2com_pkm_bus_0)
<= 0

c_e_InvestmentFlowBlock_mob_share_BEV_V2G_0_:
-0.3 InvestmentFlowBlock_invest(el_bus_BEV_inflex_storage_0)
+0.7 InvestmentFlowBlock_invest(el_bus_BEV_V2G_storage_0)
-0.3 InvestmentFlowBlock_invest(el_bus_BEV_G2V_storage_0)
= 0

c_e_InvestmentFlowBlock_mob_share_BEV_inflex_0_:
+0.8 InvestmentFlowBlock_invest(el_bus_BEV_inflex_storage_0)
-0.2 InvestmentFlowBlock_invest(el_bus_BEV_V2G_storage_0)
-0.2 InvestmentFlowBlock_invest(el_bus_BEV_G2V_storage_0)
= 0

c_e_InvestmentFlowBlock_mob_share_BEV_G2V_0_:
-0.5 InvestmentFlowBlock_invest(el_bus_BEV_inflex_storage_0)
-0.5 InvestmentFlowBlock_invest(el_bus_BEV_V2G_storage_0)
+0.5 InvestmentFlowBlock_invest(el_bus_BEV_G2V_storage_0)
= 0

c_e_InvestmentFlowBlock__BEV_V2G_equal_invest_0_(0)__:
+1 InvestmentFlowBlock_invest(BEV_V2G_storage_BEV_V2G_bus_0)
-1 InvestmentFlowBlock_invest(BEV_V2G_v2g_el_bus_0)
= 0

c_e_InvestmentFlowBlock__BEV_V2G_equal_invest_1_(0)__:
-1 InvestmentFlowBlock_invest(el_bus_BEV_V2G_storage_0)
+1 InvestmentFlowBlock_invest(BEV_V2G_v2g_el_bus_0)
= 0

c_e_InvestmentFlowBlock__BEV_V2G_equal_invest_2_(0)__:
+1 InvestmentFlowBlock_invest(el_bus_BEV_V2G_storage_0)
-1 InvestmentFlowBlock_invest(BEV_V2G_2com_pkm_bus_0)
= 0

c_e_InvestmentFlowBlock__BEV_inflex_equal_invest_0_(0)__:
+1 InvestmentFlowBlock_invest(BEV_inflex_2com_pkm_bus_0)
-1 InvestmentFlowBlock_invest(BEV_inflex_storage_BEV_inflex_bus_0)
= 0

c_e_InvestmentFlowBlock__BEV_inflex_equal_invest_1_(0)__:
-1 InvestmentFlowBlock_invest(el_bus_BEV_inflex_storage_0)
+1 InvestmentFlowBlock_invest(BEV_inflex_storage_BEV_inflex_bus_0)
= 0

c_e_InvestmentFlowBlock__BEV_G2V_equal_invest_0_(0)__:
+1 InvestmentFlowBlock_invest(el_bus_BEV_G2V_storage_0)
-1 InvestmentFlowBlock_invest(BEV_G2V_2com_pkm_bus_0)
= 0

c_e_InvestmentFlowBlock__BEV_G2V_equal_invest_1_(0)__:
-1 InvestmentFlowBlock_invest(BEV_G2V_storage_BEV_G2V_bus_0)
+1 InvestmentFlowBlock_invest(BEV_G2V_2com_pkm_bus_0)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(BEV_inflex_storage_0)_:
+1 GenericInvestmentStorageBlock_total(BEV_inflex_storage_0)
-1 GenericInvestmentStorageBlock_invest(BEV_inflex_storage_0)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(BEV_G2V_storage_0)_:
+1 GenericInvestmentStorageBlock_total(BEV_G2V_storage_0)
-1 GenericInvestmentStorageBlock_invest(BEV_G2V_storage_0)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(BEV_V2G_storage_0)_:
+1 GenericInvestmentStorageBlock_total(BEV_V2G_storage_0)
-1 GenericInvestmentStorageBlock_invest(BEV_V2G_storage_0)
= 0

c_e_GenericInvestmentStorageBlock_init_content_fix(BEV_inflex_storage)_:
+1 GenericInvestmentStorageBlock_init_content(BEV_inflex_storage)
= 0

c_e_GenericInvestmentStorageBlock_init_content_fix(BEV_G2V_storage)_:
+1 GenericInvestmentStorageBlock_init_content(BEV_G2V_storage)
= 0

c_e_GenericInvestmentStorageBlock_init_content_fix(BEV_V2G_storage)_:
+1 GenericInvestmentStorageBlock_init_content(BEV_V2G_storage)
= 0

c_e_GenericInvestmentStorageBlock_balance_first(BEV_inflex_storage)_:
-0.6944444444444445 flow(el_bus_BEV_inflex_storage_0_0)
+1.2 flow(BEV_inflex_storage_BEV_inflex_bus_0_0)
-1 GenericInvestmentStorageBlock_init_content(BEV_inflex_storage)
+1 GenericInvestmentStorageBlock_storage_content(BEV_inflex_storage_0)
= 0

c_e_GenericInvestmentStorageBlock_balance_first(BEV_G2V_storage)_:
-0.6944444444444445 flow(el_bus_BEV_G2V_storage_0_0)
+1.2 flow(BEV_G2V_storage_BEV_G2V_bus_0_0)
-1 GenericInvestmentStorageBlock_init_content(BEV_G2V_storage)
+1 GenericInvestmentStorageBlock_storage_content(BEV_G2V_storage_0)
= 0

c_e_GenericInvestmentStorageBlock_balance_first(BEV_V2G_storage)_:
-0.6944444444444445 flow(el_bus_BEV_V2G_storage_0_0)
+1.2 flow(BEV_V2G_storage_BEV_V2G_bus_0_0)
-1 GenericInvestmentStorageBlock_init_content(BEV_V2G_storage)
+1 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(BEV_inflex_storage_0_1)_:
-0.6944444444444445 flow(el_bus_BEV_inflex_storage_0_1)
+1.2 flow(BEV_inflex_storage_BEV_inflex_bus_0_1)
-1 GenericInvestmentStorageBlock_storage_content(BEV_inflex_storage_0)
+1 GenericInvestmentStorageBlock_storage_content(BEV_inflex_storage_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(BEV_inflex_storage_0_2)_:
-0.6944444444444445 flow(el_bus_BEV_inflex_storage_0_2)
+1.2 flow(BEV_inflex_storage_BEV_inflex_bus_0_2)
-1 GenericInvestmentStorageBlock_storage_content(BEV_inflex_storage_1)
+1 GenericInvestmentStorageBlock_storage_content(BEV_inflex_storage_2)
= 0

c_e_GenericInvestmentStorageBlock_balance(BEV_G2V_storage_0_1)_:
-0.6944444444444445 flow(el_bus_BEV_G2V_storage_0_1)
+1.2 flow(BEV_G2V_storage_BEV_G2V_bus_0_1)
-1 GenericInvestmentStorageBlock_storage_content(BEV_G2V_storage_0)
+1 GenericInvestmentStorageBlock_storage_content(BEV_G2V_storage_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(BEV_G2V_storage_0_2)_:
-0.6944444444444445 flow(el_bus_BEV_G2V_storage_0_2)
+1.2 flow(BEV_G2V_storage_BEV_G2V_bus_0_2)
-1 GenericInvestmentStorageBlock_storage_content(BEV_G2V_storage_1)
+1 GenericInvestmentStorageBlock_storage_content(BEV_G2V_storage_2)
= 0

c_e_GenericInvestmentStorageBlock_balance(BEV_V2G_storage_0_1)_:
-0.6944444444444445 flow(el_bus_BEV_V2G_storage_0_1)
+1.2 flow(BEV_V2G_storage_BEV_V2G_bus_0_1)
-1 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_0)
+1 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(BEV_V2G_storage_0_2)_:
-0.6944444444444445 flow(el_bus_BEV_V2G_storage_0_2)
+1.2 flow(BEV_V2G_storage_BEV_V2G_bus_0_2)
-1 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_1)
+1 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_2)
= 0

c_e_GenericInvestmentStorageBlock_balanced_cstr(BEV_inflex_storage)_:
-1 GenericInvestmentStorageBlock_init_content(BEV_inflex_storage)
+1 GenericInvestmentStorageBlock_storage_content(BEV_inflex_storage_2)
= 0

c_e_GenericInvestmentStorageBlock_balanced_cstr(BEV_G2V_storage)_:
-1 GenericInvestmentStorageBlock_init_content(BEV_G2V_storage)
+1 GenericInvestmentStorageBlock_storage_content(BEV_G2V_storage_2)
= 0

c_e_GenericInvestmentStorageBlock_balanced_cstr(BEV_V2G_storage)_:
-1 GenericInvestmentStorageBlock_init_content(BEV_V2G_storage)
+1 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_2)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(BEV_inflex_storage_0)_:
-1 InvestmentFlowBlock_total(el_bus_BEV_inflex_storage_0)
+1 InvestmentFlowBlock_total(BEV_inflex_storage_BEV_inflex_bus_0)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(BEV_G2V_storage_0)_:
+1 InvestmentFlowBlock_total(BEV_G2V_storage_BEV_G2V_bus_0)
-1 InvestmentFlowBlock_total(el_bus_BEV_G2V_storage_0)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(BEV_V2G_storage_0)_:
-1 InvestmentFlowBlock_total(el_bus_BEV_V2G_storage_0)
+1 InvestmentFlowBlock_total(BEV_V2G_storage_BEV_V2G_bus_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(BEV_inflex_storage_0)_:
+1 InvestmentFlowBlock_total(el_bus_BEV_inflex_storage_0)
-0.3333333333333333 GenericInvestmentStorageBlock_total(BEV_inflex_storage_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(BEV_G2V_storage_0)_:
+1 InvestmentFlowBlock_total(el_bus_BEV_G2V_storage_0)
-0.3333333333333333 GenericInvestmentStorageBlock_total(BEV_G2V_storage_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(BEV_V2G_storage_0)_:
+1 InvestmentFlowBlock_total(el_bus_BEV_V2G_storage_0)
-0.3333333333333333 GenericInvestmentStorageBlock_total(BEV_V2G_storage_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(BEV_inflex_storage_0)_:
+1 InvestmentFlowBlock_total(BEV_inflex_storage_BEV_inflex_bus_0)
-0.3333333333333333 GenericInvestmentStorageBlock_total(BEV_inflex_storage_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(BEV_G2V_storage_0)_:
+1 InvestmentFlowBlock_total(BEV_G2V_storage_BEV_G2V_bus_0)
-0.3333333333333333 GenericInvestmentStorageBlock_total(BEV_G2V_storage_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(BEV_V2G_storage_0)_:
+1 InvestmentFlowBlock_total(BEV_V2G_storage_BEV_V2G_bus_0)
-0.3333333333333333 GenericInvestmentStorageBlock_total(BEV_V2G_storage_0)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(BEV_inflex_storage_0_0)_:
-1 GenericInvestmentStorageBlock_total(BEV_inflex_storage_0)
+1 GenericInvestmentStorageBlock_storage_content(BEV_inflex_storage_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(BEV_inflex_storage_0_1)_:
-1 GenericInvestmentStorageBlock_total(BEV_inflex_storage_0)
+1 GenericInvestmentStorageBlock_storage_content(BEV_inflex_storage_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(BEV_inflex_storage_0_2)_:
-1 GenericInvestmentStorageBlock_total(BEV_inflex_storage_0)
+1 GenericInvestmentStorageBlock_storage_content(BEV_inflex_storage_2)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(BEV_G2V_storage_0_0)_:
-1 GenericInvestmentStorageBlock_total(BEV_G2V_storage_0)
+1 GenericInvestmentStorageBlock_storage_content(BEV_G2V_storage_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(BEV_G2V_storage_0_1)_:
-1 GenericInvestmentStorageBlock_total(BEV_G2V_storage_0)
+1 GenericInvestmentStorageBlock_storage_content(BEV_G2V_storage_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(BEV_G2V_storage_0_2)_:
-1 GenericInvestmentStorageBlock_total(BEV_G2V_storage_0)
+1 GenericInvestmentStorageBlock_storage_content(BEV_G2V_storage_2)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(BEV_V2G_storage_0_0)_:
-1 GenericInvestmentStorageBlock_total(BEV_V2G_storage_0)
+1 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(BEV_V2G_storage_0_1)_:
-1 GenericInvestmentStorageBlock_total(BEV_V2G_storage_0)
+1 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(BEV_V2G_storage_0_2)_:
-1 GenericInvestmentStorageBlock_total(BEV_V2G_storage_0)
+1 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_2)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(el_bus_BEV_inflex_storage_0) <= +inf
   0 <= InvestmentFlowBlock_invest(el_bus_BEV_V2G_storage_0) <= +inf
   0 <= InvestmentFlowBlock_invest(BEV_G2V_storage_BEV_G2V_bus_0) <= +inf
   0 <= InvestmentFlowBlock_invest(el_bus_BEV_G2V_storage_0) <= +inf
   0 <= InvestmentFlowBlock_invest(BEV_inflex_2com_pkm_bus_0) <= +inf
   0 <= InvestmentFlowBlock_invest(BEV_V2G_storage_BEV_V2G_bus_0) <= +inf
   0 <= InvestmentFlowBlock_invest(BEV_inflex_storage_BEV_inflex_bus_0) <= +inf
   0 <= InvestmentFlowBlock_invest(BEV_V2G_2com_pkm_bus_0) <= +inf
   0 <= InvestmentFlowBlock_invest(BEV_V2G_v2g_el_bus_0) <= +inf
   0 <= InvestmentFlowBlock_invest(BEV_G2V_2com_pkm_bus_0) <= +inf
   0 <= flow(el_bus_BEV_V2G_storage_0_0) <= +inf
   0 <= flow(el_bus_BEV_V2G_storage_0_1) <= +inf
   0 <= flow(el_bus_BEV_V2G_storage_0_2) <= +inf
   0 <= flow(el_bus_BEV_inflex_storage_0_0) <= +inf
   0 <= flow(el_bus_BEV_inflex_storage_0_1) <= +inf
   0 <= flow(el_bus_BEV_inflex_storage_0_2) <= +inf
   0 <= flow(el_bus_BEV_G2V_storage_0_0) <= +inf
   0 <= flow(el_bus_BEV_G2V_storage_0_1) <= +inf
   0 <= flow(el_bus_BEV_G2V_storage_0_2) <= +inf
   0 <= flow(BEV_V2G_storage_BEV_V2G_bus_0_0) <= +inf
   0 <= flow(BEV_V2G_storage_BEV_V2G_bus_0_1) <= +inf
   0 <= flow(BEV_V2G_storage_BEV_V2G_bus_0_2) <= +inf
   0 <= flow(BEV_V2G_bus_BEV_V2G_v2g_0_0) <= +inf
   0 <= flow(BEV_V2G_bus_BEV_V2G_v2g_0_1) <= +inf
   0 <= flow(BEV_V2G_bus_BEV_V2G_v2g_0_2) <= +inf
   0 <= flow(BEV_V2G_bus_BEV_V2G_2com_0_0) <= +inf
   0 <= flow(BEV_V2G_bus_BEV_V2G_2com_0_1) <= +inf
   0 <= flow(BEV_V2G_bus_BEV_V2G_2com_0_2) <= +inf
   0 <= flow(BEV_V2G_v2g_el_bus_0_0) <= +inf
   0 <= flow(BEV_V2G_v2g_el_bus_0_1) <= +inf
   0 <= flow(BEV_V2G_v2g_el_bus_0_2) <= +inf
   0 <= flow(BEV_V2G_2com_pkm_bus_0_0) <= +inf
   0 <= flow(BEV_V2G_2com_pkm_bus_0_1) <= +inf
   0 <= flow(BEV_V2G_2com_pkm_bus_0_2) <= +inf
   0 <= flow(BEV_inflex_storage_BEV_inflex_bus_0_0) <= +inf
   0 <= flow(BEV_inflex_storage_BEV_inflex_bus_0_1) <= +inf
   0 <= flow(BEV_inflex_storage_BEV_inflex_bus_0_2) <= +inf
   0 <= flow(BEV_inflex_bus_BEV_inflex_2com_0_0) <= +inf
   0 <= flow(BEV_inflex_bus_BEV_inflex_2com_0_1) <= +inf
   0 <= flow(BEV_inflex_bus_BEV_inflex_2com_0_2) <= +inf
   0 <= flow(BEV_inflex_2com_pkm_bus_0_0) <= +inf
   0 <= flow(BEV_inflex_2com_pkm_bus_0_1) <= +inf
   0 <= flow(BEV_inflex_2com_pkm_bus_0_2) <= +inf
   0 <= flow(BEV_G2V_storage_BEV_G2V_bus_0_0) <= +inf
   0 <= flow(BEV_G2V_storage_BEV_G2V_bus_0_1) <= +inf
   0 <= flow(BEV_G2V_storage_BEV_G2V_bus_0_2) <= +inf
   0 <= flow(BEV_G2V_bus_BEV_G2V_2com_0_0) <= +inf
   0 <= flow(BEV_G2V_bus_BEV_G2V_2com_0_1) <= +inf
   0 <= flow(BEV_G2V_bus_BEV_G2V_2com_0_2) <= +inf
   0 <= flow(BEV_G2V_2com_pkm_bus_0_0) <= +inf
   0 <= flow(BEV_G2V_2com_pkm_bus_0_1) <= +inf
   0 <= flow(BEV_G2V_2com_pkm_bus_0_2) <= +inf
   0 <= InvestmentFlowBlock_total(el_bus_BEV_inflex_storage_0) <= +inf
   0 <= InvestmentFlowBlock_total(el_bus_BEV_V2G_storage_0) <= +inf
   0 <= InvestmentFlowBlock_total(BEV_G2V_storage_BEV_G2V_bus_0) <= +inf
   0 <= InvestmentFlowBlock_total(el_bus_BEV_G2V_storage_0) <= +inf
   0 <= InvestmentFlowBlock_total(BEV_inflex_2com_pkm_bus_0) <= +inf
   0 <= InvestmentFlowBlock_total(BEV_V2G_storage_BEV_V2G_bus_0) <= +inf
   0 <= InvestmentFlowBlock_total(BEV_inflex_storage_BEV_inflex_bus_0) <= +inf
   0 <= InvestmentFlowBlock_total(BEV_V2G_2com_pkm_bus_0) <= +inf
   0 <= InvestmentFlowBlock_total(BEV_V2G_v2g_el_bus_0) <= +inf
   0 <= InvestmentFlowBlock_total(BEV_G2V_2com_pkm_bus_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(BEV_inflex_storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(BEV_G2V_storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(BEV_V2G_storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(BEV_inflex_storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(BEV_G2V_storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(BEV_V2G_storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_init_content(BEV_inflex_storage) <= +inf
   0 <= GenericInvestmentStorageBlock_init_content(BEV_G2V_storage) <= +inf
   0 <= GenericInvestmentStorageBlock_init_content(BEV_V2G_storage) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(BEV_inflex_storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(BEV_inflex_storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(BEV_inflex_storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(BEV_G2V_storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(BEV_G2V_storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(BEV_G2V_storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_2) <= +inf
end
