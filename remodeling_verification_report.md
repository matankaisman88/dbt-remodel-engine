# Remodeling Verification Report

Phase A headless engine run against copied corpora under `tests/fixtures/`.

> **Fixture provenance:** Ingested from ETL-Migration-Studio via
> `scripts/ingest_fixtures_from_studio.py`.
> **Studio root:** `C:\ETL-Migration-Studio`
> - `daily_etl_main_active_diagnosis` (`daily_etl_main_active_diagnosis`): 13 models from `.remodel_engine_exports\daily_etl_main_active_diagnosis`
> - `informatica_stress_corpus_aggregator_multi_groupby` (`informatica_stress_corpus_aggregator_multi_groupby`): 1 models from `.remodel_engine_exports\informatica_stress_corpus_aggregator_multi_groupby`
> - `informatica_stress_corpus_colliding_names_stress` (`informatica_stress_corpus_colliding_names_stress`): 1 models from `.remodel_engine_exports\informatica_stress_corpus_colliding_names_stress`
> - `informatica_stress_corpus_deep_lookup_chain` (`informatica_stress_corpus_deep_lookup_chain`): 1 models from `.remodel_engine_exports\informatica_stress_corpus_deep_lookup_chain`
> - `informatica_stress_corpus_dunder_schema_names_3merge` (`informatica_stress_corpus_dunder_schema_names_3merge`): 1 models from `.remodel_engine_exports\informatica_stress_corpus_dunder_schema_names_3merge`
> - `informatica_stress_corpus_filter_router_union_faninout` (`informatica_stress_corpus_filter_router_union_faninout`): 1 models from `.remodel_engine_exports\informatica_stress_corpus_filter_router_union_faninout`
> - `informatica_stress_corpus_informatica_scd_type2` (`informatica_stress_corpus_informatica_scd_type2`): 1 models from `.remodel_engine_exports\informatica_stress_corpus_informatica_scd_type2`
> - `informatica_stress_corpus_long_linear_10stage` (`informatica_stress_corpus_long_linear_10stage`): 1 models from `.remodel_engine_exports\informatica_stress_corpus_long_linear_10stage`
> - `informatica_stress_corpus_lookup_composite_condition` (`informatica_stress_corpus_lookup_composite_condition`): 1 models from `.remodel_engine_exports\informatica_stress_corpus_lookup_composite_condition`
> - `informatica_stress_corpus_multi_target_nonsequential_load_order` (`informatica_stress_corpus_multi_target_nonsequential_load_order`): 3 models from `.remodel_engine_exports\informatica_stress_corpus_multi_target_nonsequential_load_order`
> - `informatica_stress_corpus_nested_conditional_expression` (`informatica_stress_corpus_nested_conditional_expression`): 1 models from `.remodel_engine_exports\informatica_stress_corpus_nested_conditional_expression`
> - `informatica_stress_corpus_nested_mapplet_pipeline` (`informatica_stress_corpus_nested_mapplet_pipeline`): 1 models from `.remodel_engine_exports\informatica_stress_corpus_nested_mapplet_pipeline`
> - `informatica_stress_corpus_rank_sorter_aggregator_chain` (`informatica_stress_corpus_rank_sorter_aggregator_chain`): 1 models from `.remodel_engine_exports\informatica_stress_corpus_rank_sorter_aggregator_chain`
> - `informatica_stress_corpus_reused_mapplet_twice` (`informatica_stress_corpus_reused_mapplet_twice`): 2 models from `.remodel_engine_exports\informatica_stress_corpus_reused_mapplet_twice`
> - `informatica_stress_corpus_sequence_generator_reused` (`informatica_stress_corpus_sequence_generator_reused`): 2 models from `.remodel_engine_exports\informatica_stress_corpus_sequence_generator_reused`
> - `informatica_stress_corpus_sequence_update_strategy` (`informatica_stress_corpus_sequence_update_strategy`): 1 models from `.remodel_engine_exports\informatica_stress_corpus_sequence_update_strategy`
> - `informatica_stress_corpus_sorter_multi_key` (`informatica_stress_corpus_sorter_multi_key`): 1 models from `.remodel_engine_exports\informatica_stress_corpus_sorter_multi_key`
> - `informatica_stress_corpus_star_join_4satellite` (`informatica_stress_corpus_star_join_4satellite`): 1 models from `.remodel_engine_exports\informatica_stress_corpus_star_join_4satellite`
> - `informatica_stress_corpus_three_sq_two_joiner_chain` (`informatica_stress_corpus_three_sq_two_joiner_chain`): 1 models from `.remodel_engine_exports\informatica_stress_corpus_three_sq_two_joiner_chain`
> - `informatica_stress_corpus_two_mapplets_chained` (`informatica_stress_corpus_two_mapplets_chained`): 1 models from `.remodel_engine_exports\informatica_stress_corpus_two_mapplets_chained`
> - `informatica_stress_corpus_underscore_schema_multi_target` (`informatica_stress_corpus_underscore_schema_multi_target`): 2 models from `.remodel_engine_exports\informatica_stress_corpus_underscore_schema_multi_target`
> - `informatica_stress_corpus_union_heterogeneous_4way` (`informatica_stress_corpus_union_heterogeneous_4way`): 1 models from `.remodel_engine_exports\informatica_stress_corpus_union_heterogeneous_4way`
> - `informatica_stress_corpus_wide_router_fanout` (`informatica_stress_corpus_wide_router_fanout`): 6 models from `.remodel_engine_exports\informatica_stress_corpus_wide_router_fanout`
> - `informatica_xml_aggregator_pipeline` (`informatica_xml_aggregator_pipeline`): 3 models from `.remodel_engine_exports\informatica_xml_aggregator_pipeline`
> - `informatica_xml_mapplet_pipeline` (`informatica_xml_mapplet_pipeline`): 1 models from `.remodel_engine_exports\informatica_xml_mapplet_pipeline`
> - `informatica_xml_minimal_source_sq_exp_target` (`informatica_xml_minimal_source_sq_exp_target`): 1 models from `.remodel_engine_exports\informatica_xml_minimal_source_sq_exp_target`
> - `informatica_xml_minimal_with_missing_transformation` (`informatica_xml_minimal_with_missing_transformation`): 1 models from `.remodel_engine_exports\informatica_xml_minimal_with_missing_transformation`
> - `informatica_xml_minimal_with_unsupported` (`informatica_xml_minimal_with_unsupported`): 1 models from `.remodel_engine_exports\informatica_xml_minimal_with_unsupported`
> - `informatica_xml_multi_input_union` (`informatica_xml_multi_input_union`): 1 models from `.remodel_engine_exports\informatica_xml_multi_input_union`
> - `informatica_xml_multi_target_pipeline` (`informatica_xml_multi_target_pipeline`): 2 models from `.remodel_engine_exports\informatica_xml_multi_target_pipeline`
> - `informatica_xml_real_world_complex_pipeline` (`informatica_xml_real_world_complex_pipeline`): 5 models from `.remodel_engine_exports\informatica_xml_real_world_complex_pipeline`
> - `informatica_xml_sq_user_defined_join_two_tables` (`informatica_xml_sq_user_defined_join_two_tables`): 1 models from `.remodel_engine_exports\informatica_xml_sq_user_defined_join_two_tables`
> - `informatica_xml_transform_pipeline` (`informatica_xml_transform_pipeline`): 3 models from `.remodel_engine_exports\informatica_xml_transform_pipeline`
> - `informatica_xml_update_strategy_pipeline` (`informatica_xml_update_strategy_pipeline`): 1 models from `.remodel_engine_exports\informatica_xml_update_strategy_pipeline`
> - `orchestration_infa_synthetic_nonconforming_names` (`orchestration_infa_synthetic_nonconforming_names`): 1 models from `.remodel_engine_exports\orchestration_infa_synthetic_nonconforming_names`
> - `orchestration_infa_synthetic_standalone_worklet_root` (`orchestration_infa_synthetic_standalone_worklet_root`): 1 models from `.remodel_engine_exports\orchestration_infa_synthetic_standalone_worklet_root`
> - `orchestration_infa_wf_enterprise_daily_run` (`orchestration_infa_wf_enterprise_daily_run`): 4 models from `.remodel_engine_exports\orchestration_infa_wf_enterprise_daily_run`
> - `orchestration_infa_wf_enterprise_master_repository` (`orchestration_infa_wf_enterprise_master_repository`): 51 models from `.remodel_engine_exports\orchestration_infa_wf_enterprise_master_repository`
> - `orchestration_infa_wf_with_nested_worklet` (`orchestration_infa_wf_with_nested_worklet`): 3 models from `.remodel_engine_exports\orchestration_infa_wf_with_nested_worklet`
> - `orchestration_infa_wrapped_wf_m_aggregator` (`orchestration_infa_wrapped_wf_m_aggregator`): 3 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_aggregator`
> - `orchestration_infa_wrapped_wf_m_aggregator_multi_groupby` (`orchestration_infa_wrapped_wf_m_aggregator_multi_groupby`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_aggregator_multi_groupby`
> - `orchestration_infa_wrapped_wf_m_colliding_names_stress` (`orchestration_infa_wrapped_wf_m_colliding_names_stress`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_colliding_names_stress`
> - `orchestration_infa_wrapped_wf_m_deep_lookup_chain` (`orchestration_infa_wrapped_wf_m_deep_lookup_chain`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_deep_lookup_chain`
> - `orchestration_infa_wrapped_wf_m_dunder_schema_names_3merge` (`orchestration_infa_wrapped_wf_m_dunder_schema_names_3merge`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_dunder_schema_names_3merge`
> - `orchestration_infa_wrapped_wf_m_filter_router_union_faninout` (`orchestration_infa_wrapped_wf_m_filter_router_union_faninout`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_filter_router_union_faninout`
> - `orchestration_infa_wrapped_wf_m_informatica_scd_type2` (`orchestration_infa_wrapped_wf_m_informatica_scd_type2`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_informatica_scd_type2`
> - `orchestration_infa_wrapped_wf_m_long_linear_10stage` (`orchestration_infa_wrapped_wf_m_long_linear_10stage`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_long_linear_10stage`
> - `orchestration_infa_wrapped_wf_m_lookup_composite_condition` (`orchestration_infa_wrapped_wf_m_lookup_composite_condition`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_lookup_composite_condition`
> - `orchestration_infa_wrapped_wf_m_mapplet` (`orchestration_infa_wrapped_wf_m_mapplet`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_mapplet`
> - `orchestration_infa_wrapped_wf_m_minimal` (`orchestration_infa_wrapped_wf_m_minimal`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_minimal`
> - `orchestration_infa_wrapped_wf_m_missing_transformation` (`orchestration_infa_wrapped_wf_m_missing_transformation`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_missing_transformation`
> - `orchestration_infa_wrapped_wf_m_multi_target` (`orchestration_infa_wrapped_wf_m_multi_target`): 2 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_multi_target`
> - `orchestration_infa_wrapped_wf_m_multi_target_nonsequential_load_order` (`orchestration_infa_wrapped_wf_m_multi_target_nonsequential_load_order`): 3 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_multi_target_nonsequential_load_order`
> - `orchestration_infa_wrapped_wf_m_multi_union` (`orchestration_infa_wrapped_wf_m_multi_union`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_multi_union`
> - `orchestration_infa_wrapped_wf_m_nested_conditional_expression` (`orchestration_infa_wrapped_wf_m_nested_conditional_expression`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_nested_conditional_expression`
> - `orchestration_infa_wrapped_wf_m_nested_mapplet_pipeline` (`orchestration_infa_wrapped_wf_m_nested_mapplet_pipeline`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_nested_mapplet_pipeline`
> - `orchestration_infa_wrapped_wf_m_rank_sorter_aggregator_chain` (`orchestration_infa_wrapped_wf_m_rank_sorter_aggregator_chain`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_rank_sorter_aggregator_chain`
> - `orchestration_infa_wrapped_wf_m_reused_mapplet_twice` (`orchestration_infa_wrapped_wf_m_reused_mapplet_twice`): 2 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_reused_mapplet_twice`
> - `orchestration_infa_wrapped_wf_m_sequence_generator_reused` (`orchestration_infa_wrapped_wf_m_sequence_generator_reused`): 2 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_sequence_generator_reused`
> - `orchestration_infa_wrapped_wf_m_sequence_update_strategy` (`orchestration_infa_wrapped_wf_m_sequence_update_strategy`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_sequence_update_strategy`
> - `orchestration_infa_wrapped_wf_m_sorter_multi_key` (`orchestration_infa_wrapped_wf_m_sorter_multi_key`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_sorter_multi_key`
> - `orchestration_infa_wrapped_wf_m_sq_user_defined_join_two_tables` (`orchestration_infa_wrapped_wf_m_sq_user_defined_join_two_tables`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_sq_user_defined_join_two_tables`
> - `orchestration_infa_wrapped_wf_m_star_join_4satellite` (`orchestration_infa_wrapped_wf_m_star_join_4satellite`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_star_join_4satellite`
> - `orchestration_infa_wrapped_wf_m_three_sq_two_joiner_chain` (`orchestration_infa_wrapped_wf_m_three_sq_two_joiner_chain`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_three_sq_two_joiner_chain`
> - `orchestration_infa_wrapped_wf_m_transforms` (`orchestration_infa_wrapped_wf_m_transforms`): 3 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_transforms`
> - `orchestration_infa_wrapped_wf_m_two_mapplets_chained` (`orchestration_infa_wrapped_wf_m_two_mapplets_chained`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_two_mapplets_chained`
> - `orchestration_infa_wrapped_wf_m_underscore_schema_multi_target` (`orchestration_infa_wrapped_wf_m_underscore_schema_multi_target`): 2 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_underscore_schema_multi_target`
> - `orchestration_infa_wrapped_wf_m_union_heterogeneous_4way` (`orchestration_infa_wrapped_wf_m_union_heterogeneous_4way`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_union_heterogeneous_4way`
> - `orchestration_infa_wrapped_wf_m_update_strategy` (`orchestration_infa_wrapped_wf_m_update_strategy`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_update_strategy`
> - `orchestration_infa_wrapped_wf_m_wide_router_fanout` (`orchestration_infa_wrapped_wf_m_wide_router_fanout`): 6 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_wide_router_fanout`
> - `orchestration_infa_wrapped_wf_m_with_unsupported` (`orchestration_infa_wrapped_wf_m_with_unsupported`): 1 models from `.remodel_engine_exports\orchestration_infa_wrapped_wf_m_with_unsupported`
> - `wwi_sales_star` (`wwi_sales_star`): 5 models from `.remodel_engine_exports\_test_wwi`

## daily_etl_main_corpus (etl_to_dbt export format)

- **pipeline_id:** `daily_etl_main_active_diagnosis`
- **overall status:** `success`
- **legacy transformations (manifest):** 14
- **modern models:** 4
- **CTEs collapsed:** 0
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `raw_stg_diagnosis` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | — |
| `raw_int_diagnosis_enriched` | `intermediate` | `pass` | matched rule #2: ref() upstream with lookup join | — |
| `raw_m_active_diagnosis` | `intermediate` | `pass` | matched rule #2: ref() upstream with CASE | — |
| `raw_lookup_ambiguous` | `intermediate` | `pass` | matched rule #2: ref() upstream with lookup join | — |

## informatica/informatica_stress_corpus_aggregator_multi_groupby (etl_to_dbt export format)

- **pipeline_id:** `informatica_stress_corpus_aggregator_multi_groupby`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 4
- **modern models:** 1
- **CTEs collapsed:** 1
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_sales_rollup` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_sales_detail', 'int_agg_multi_group'] |

## informatica/informatica_stress_corpus_colliding_names_stress (etl_to_dbt export format)

- **pipeline_id:** `informatica_stress_corpus_colliding_names_stress`
- **overall status:** `success`
- **legacy transformations (manifest):** 4
- **modern models:** 1
- **CTEs collapsed:** 1
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_value_table` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_value', 'int_value_exp'] |

## informatica/informatica_stress_corpus_deep_lookup_chain (etl_to_dbt export format)

- **pipeline_id:** `informatica_stress_corpus_deep_lookup_chain`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 8
- **modern models:** 1
- **CTEs collapsed:** 1
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_txn_enriched` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_txn', 'lkp_lkp_cust'] |

## informatica/informatica_stress_corpus_dunder_schema_names_3merge (etl_to_dbt export format)

- **pipeline_id:** `informatica_stress_corpus_dunder_schema_names_3merge`
- **overall status:** `success`
- **legacy transformations (manifest):** 11
- **modern models:** 1
- **CTEs collapsed:** 6
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `dw_core_all_entities_master` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_fin_ap_vendor_master', 'int_exp_tag_vendor'], ['sq_sq_hr_core_employee_master', 'int_exp_tag_employee'], ['sq_sq_fin_ar_customer_master', 'int_exp_tag_customer'], ['int_exp_tag_customer', 'int_un_all_entities'], ['int_exp_tag_employee', 'int_un_all_entities'], ['int_exp_tag_vendor', 'int_un_all_entities'] |

## informatica/informatica_stress_corpus_filter_router_union_faninout (etl_to_dbt export format)

- **pipeline_id:** `informatica_stress_corpus_filter_router_union_faninout`
- **overall status:** `failed_parity`
- **legacy transformations (manifest):** 8
- **modern models:** 1
- **CTEs collapsed:** 5
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_claims_flagged` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_claims', 'int_fil_active'], ['int_fil_active', 'int_rtr_high_low'], ['int_rtr_high_low', 'int_exp_high_flag'], ['int_exp_low_flag', 'int_un_flagged_claims'], ['int_exp_high_flag', 'int_un_flagged_claims'] |

## informatica/informatica_stress_corpus_informatica_scd_type2 (etl_to_dbt export format)

- **pipeline_id:** `informatica_stress_corpus_informatica_scd_type2`
- **overall status:** `failed_parity`
- **legacy transformations (manifest):** 5
- **modern models:** 1
- **CTEs collapsed:** 2
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_dim_customer` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_customer_dim', 'int_exp_scd_dates'], ['int_exp_scd_dates', 'int_upd_scd'] |

## informatica/informatica_stress_corpus_long_linear_10stage (etl_to_dbt export format)

- **pipeline_id:** `informatica_stress_corpus_long_linear_10stage`
- **overall status:** `failed_parity`
- **legacy transformations (manifest):** 12
- **modern models:** 1
- **CTEs collapsed:** 8
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_log_processed` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_raw_log', 'int_exp_clean1'], ['int_exp_clean1', 'int_fil_not_debug'], ['int_fil_not_debug', 'lkp_lkp_severity_code'], ['int_exp_clean2', 'int_rtr_sev'], ['int_rtr_sev', 'int_exp_tag_critical'], ['int_exp_tag_normal', 'int_un_tagged'], ['int_exp_tag_critical', 'int_un_tagged'], ['int_un_tagged', 'int_srt_final'] |

## informatica/informatica_stress_corpus_lookup_composite_condition (etl_to_dbt export format)

- **pipeline_id:** `informatica_stress_corpus_lookup_composite_condition`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 4
- **modern models:** 1
- **CTEs collapsed:** 1
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_inventory_valued` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_inventory_movement', 'lkp_lkp_unit_cost'] |

## informatica/informatica_stress_corpus_multi_target_nonsequential_load_order (etl_to_dbt export format)

- **pipeline_id:** `informatica_stress_corpus_multi_target_nonsequential_load_order`
- **overall status:** `success`
- **legacy transformations (manifest):** 6
- **modern models:** 3
- **CTEs collapsed:** 3
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_type_c` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_master_data', 'int_rtr_type'] |
| `tgt_type_a` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_master_data', 'int_rtr_type'] |
| `tgt_type_b` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_master_data', 'int_rtr_type'] |

## informatica/informatica_stress_corpus_nested_conditional_expression (etl_to_dbt export format)

- **pipeline_id:** `informatica_stress_corpus_nested_conditional_expression`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 4
- **modern models:** 1
- **CTEs collapsed:** 1
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_student_grades` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_scores', 'int_exp_grade_prep'] |

## informatica/informatica_stress_corpus_nested_mapplet_pipeline (etl_to_dbt export format)

- **pipeline_id:** `informatica_stress_corpus_nested_mapplet_pipeline`
- **overall status:** `success`
- **legacy transformations (manifest):** 4
- **modern models:** 1
- **CTEs collapsed:** 7
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_clean_names` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_raw_names', 'map_mp_outer_inst_bind'], ['map_mp_outer_inst_bind', 'map_mp_outer_inst__mp_inner_inst__bind'], ['map_mp_outer_inst__mp_inner_inst__bind', 'map_mp_outer_inst__mp_inner_inst__exp_trim'], ['map_mp_outer_inst__mp_inner_inst__exp_trim', 'int_mp_outer_inst__mp_inner_inst'], ['int_mp_outer_inst__mp_inner_inst', 'map_mp_outer_inst_exp_upper_bind'], ['map_mp_outer_inst_exp_upper_bind', 'map_mp_outer_inst_exp_upper'], ['map_mp_outer_inst_exp_upper', 'int_mp_outer_inst'] |

## informatica/informatica_stress_corpus_rank_sorter_aggregator_chain (etl_to_dbt export format)

- **pipeline_id:** `informatica_stress_corpus_rank_sorter_aggregator_chain`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 6
- **modern models:** 1
- **CTEs collapsed:** 2
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_region_summary` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_sales', 'int_rnk_top_sales'], ['int_srt_by_amt', 'int_agg_region_total'] |

## informatica/informatica_stress_corpus_reused_mapplet_twice (etl_to_dbt export format)

- **pipeline_id:** `informatica_stress_corpus_reused_mapplet_twice`
- **overall status:** `success`
- **legacy transformations (manifest):** 8
- **modern models:** 2
- **CTEs collapsed:** 6
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_product_names_clean` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_product_names', 'map_mp_normalize_product_bind'], ['map_mp_normalize_product_bind', 'map_mp_normalize_product_exp_normalize'], ['map_mp_normalize_product_exp_normalize', 'int_mp_normalize_product'] |
| `tgt_supplier_names_clean` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_supplier_names', 'map_mp_normalize_supplier_bind'], ['map_mp_normalize_supplier_bind', 'map_mp_normalize_supplier_exp_normalize'], ['map_mp_normalize_supplier_exp_normalize', 'int_mp_normalize_supplier'] |

## informatica/informatica_stress_corpus_sequence_generator_reused (etl_to_dbt export format)

- **pipeline_id:** `informatica_stress_corpus_sequence_generator_reused`
- **overall status:** `success`
- **legacy transformations (manifest):** 9
- **modern models:** 2
- **CTEs collapsed:** 2
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_accounts` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_new_accounts', 'int_exp_acct_key'] |
| `tgt_contacts` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_new_contacts', 'int_exp_contact_key'] |

## informatica/informatica_stress_corpus_sequence_update_strategy (etl_to_dbt export format)

- **pipeline_id:** `informatica_stress_corpus_sequence_update_strategy`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 6
- **modern models:** 1
- **CTEs collapsed:** 1
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_customer_scd` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_customer_changes', 'int_exp_build_row'] |

## informatica/informatica_stress_corpus_sorter_multi_key (etl_to_dbt export format)

- **pipeline_id:** `informatica_stress_corpus_sorter_multi_key`
- **overall status:** `success`
- **legacy transformations (manifest):** 4
- **modern models:** 1
- **CTEs collapsed:** 1
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_leaderboard_sorted` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_leaderboard', 'int_srt_leaderboard'] |

## informatica/informatica_stress_corpus_star_join_4satellite (etl_to_dbt export format)

- **pipeline_id:** `informatica_stress_corpus_star_join_4satellite`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 12
- **modern models:** 1
- **CTEs collapsed:** 3
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_order_enriched` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_order_header', 'int_jnr_cust'], ['sq_sq_src_customer', 'int_jnr_cust'], ['sq_sq_src_shipping', 'int_jnr_ship'] |

## informatica/informatica_stress_corpus_three_sq_two_joiner_chain (etl_to_dbt export format)

- **pipeline_id:** `informatica_stress_corpus_three_sq_two_joiner_chain`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 9
- **modern models:** 1
- **CTEs collapsed:** 3
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_employee_full` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_employee', 'int_jnr_dept'], ['sq_sq_department', 'int_jnr_dept'], ['sq_sq_manager', 'int_jnr_mgr'] |

## informatica/informatica_stress_corpus_two_mapplets_chained (etl_to_dbt export format)

- **pipeline_id:** `informatica_stress_corpus_two_mapplets_chained`
- **overall status:** `success`
- **legacy transformations (manifest):** 5
- **modern models:** 1
- **CTEs collapsed:** 6
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_clean_labels` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_raw_labels', 'map_mp_trim_inst_bind'], ['map_mp_trim_inst_bind', 'map_mp_trim_inst_exp_trim'], ['map_mp_trim_inst_exp_trim', 'int_mp_trim_inst'], ['int_mp_trim_inst', 'map_mp_uppercase2_inst_bind'], ['map_mp_uppercase2_inst_bind', 'map_mp_uppercase2_inst_exp_upper2'], ['map_mp_uppercase2_inst_exp_upper2', 'int_mp_uppercase2_inst'] |

## informatica/informatica_stress_corpus_underscore_schema_multi_target (etl_to_dbt export format)

- **pipeline_id:** `informatica_stress_corpus_underscore_schema_multi_target`
- **overall status:** `success`
- **legacy transformations (manifest):** 6
- **modern models:** 2
- **CTEs collapsed:** 2
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `dw_core_tmp_staging_events_clean` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_legacy_ops_tmp_staging_raw_events', 'int_fil_valid'] |
| `dw_core_tmp_staging_events_rejected` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_legacy_ops_tmp_staging_raw_events', 'int_fil_invalid'] |

## informatica/informatica_stress_corpus_union_heterogeneous_4way (etl_to_dbt export format)

- **pipeline_id:** `informatica_stress_corpus_union_heterogeneous_4way`
- **overall status:** `success`
- **legacy transformations (manifest):** 10
- **modern models:** 1
- **CTEs collapsed:** 4
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_all_events` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_src_web_events', 'int_un_all_events'], ['sq_sq_src_pos_events', 'int_un_all_events'], ['sq_sq_src_mobile_events', 'int_un_all_events'], ['sq_sq_src_callcenter_events', 'int_un_all_events'] |

## informatica/informatica_stress_corpus_wide_router_fanout (etl_to_dbt export format)

- **pipeline_id:** `informatica_stress_corpus_wide_router_fanout`
- **overall status:** `success`
- **legacy transformations (manifest):** 9
- **modern models:** 6
- **CTEs collapsed:** 6
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_electronics` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_rtr_category'] |
| `tgt_apparel` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_rtr_category'] |
| `tgt_grocery` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_rtr_category'] |
| `tgt_furniture` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_rtr_category'] |
| `tgt_toys` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_rtr_category'] |
| `tgt_default` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_rtr_category'] |

## informatica/informatica_xml_aggregator_pipeline (etl_to_dbt export format)

- **pipeline_id:** `informatica_xml_aggregator_pipeline`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 8
- **modern models:** 3
- **CTEs collapsed:** 3
- **models NEEDS_MANUAL_REVIEW:** 2

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_distinct` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_sales', 'int_agg_distinct'] |
| `tgt_summary` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_sales', 'int_agg_summary'] |
| `tgt_global` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_sales', 'int_agg_global'] |

## informatica/informatica_xml_mapplet_pipeline (etl_to_dbt export format)

- **pipeline_id:** `informatica_xml_mapplet_pipeline`
- **overall status:** `success`
- **legacy transformations (manifest):** 4
- **modern models:** 1
- **CTEs collapsed:** 3
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_customers` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_customers', 'map_mp_upper_inst_bind'], ['map_mp_upper_inst_bind', 'map_mp_upper_inst_exp_upper'], ['map_mp_upper_inst_exp_upper', 'int_mp_upper_inst'] |

## informatica/informatica_xml_minimal_source_sq_exp_target (etl_to_dbt export format)

- **pipeline_id:** `informatica_xml_minimal_source_sq_exp_target`
- **overall status:** `success`
- **legacy transformations (manifest):** 4
- **modern models:** 1
- **CTEs collapsed:** 1
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_orders` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_exp_orders'] |

## informatica/informatica_xml_minimal_with_missing_transformation (etl_to_dbt export format)

- **pipeline_id:** `informatica_xml_minimal_with_missing_transformation`
- **overall status:** `failed_parity`
- **legacy transformations (manifest):** 2
- **modern models:** 1
- **CTEs collapsed:** 0
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_orders` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | — |

## informatica/informatica_xml_minimal_with_unsupported (etl_to_dbt export format)

- **pipeline_id:** `informatica_xml_minimal_with_unsupported`
- **overall status:** `failed_parity`
- **legacy transformations (manifest):** 3
- **modern models:** 1
- **CTEs collapsed:** 0
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_orders` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | — |

## informatica/informatica_xml_multi_input_union (etl_to_dbt export format)

- **pipeline_id:** `informatica_xml_multi_input_union`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 8
- **modern models:** 1
- **CTEs collapsed:** 6
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_union_out` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_branch_a', 'int_exp_branch_a'], ['sq_sq_branch_b', 'int_exp_branch_b'], ['sq_sq_branch_c', 'int_exp_branch_c'], ['int_exp_branch_c', 'int_union_custom'], ['int_exp_branch_b', 'int_union_custom'], ['int_exp_branch_a', 'int_union_custom'] |

## informatica/informatica_xml_multi_target_pipeline (etl_to_dbt export format)

- **pipeline_id:** `informatica_xml_multi_target_pipeline`
- **overall status:** `failed_parity`
- **legacy transformations (manifest):** 6
- **modern models:** 2
- **CTEs collapsed:** 2
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_customers` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_customers', 'int_exp_customers'] |
| `tgt_orders` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_exp_orders'] |

## informatica/informatica_xml_real_world_complex_pipeline (etl_to_dbt export format)

- **pipeline_id:** `informatica_xml_real_world_complex_pipeline`
- **overall status:** `failed_parity`
- **legacy transformations (manifest):** 47
- **modern models:** 5
- **CTEs collapsed:** 34
- **models NEEDS_MANUAL_REVIEW:** 4

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_fct_subscription_lifecycle` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_stg', 'int_exp_fct'], ['int_exp_fct', 'int_upd_fct'] |
| `tgt_lnd_open_subscription_detail` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_ext_cdc', 'int_exp_delta'] |
| `shortcut_to_stg_subscriber_account_key` | `needs_manual_review` | `fail` | failed rule #1 (sources only but disallowed transforms) and no other rule matched | ['int_exptrans1', 'int_rnktrans'], ['int_exptrans', 'int_srttrans1'], ['int_srttrans1', 'int_jnrtrans'], ['int_exp_src_subscription_detail1_bind', 'int_exp_src_subscription_detail1'], ['int_exp_src_subscription_detail1', 'int_union1'], ['int_union1', 'int_exp_cast_to_int_bind'], ['int_exp_cast_to_int_bind', 'int_exp_cast_to_int'], ['int_exp_cast_to_int', 'lkp_lkp_ref_billing_region'], ['map_mapplet_normalize_billing_date_bind', 'map_mapplet_normalize_billing_date_exp_date_prep'], ['int_mapplet_normalize_billing_date', 'int_exp_fields_bind'], ['int_agg_for_subscriber_key_bind', 'int_agg_for_subscriber_key'] |
| `shortcut_to_stg_subscription_key` | `needs_manual_review` | `fail` | failed rule #1 (sources only but disallowed transforms) and no other rule matched | ['int_exptrans1', 'int_rnktrans'], ['int_exptrans', 'int_srttrans1'], ['int_srttrans1', 'int_jnrtrans'], ['int_exp_src_subscription_detail1_bind', 'int_exp_src_subscription_detail1'], ['int_exp_src_subscription_detail1', 'int_union1'], ['int_union1', 'int_exp_cast_to_int_bind'], ['int_exp_cast_to_int_bind', 'int_exp_cast_to_int'], ['int_exp_cast_to_int', 'lkp_lkp_ref_billing_region'], ['map_mapplet_normalize_billing_date_bind', 'map_mapplet_normalize_billing_date_exp_date_prep'], ['int_mapplet_normalize_billing_date', 'int_exp_fields_bind'] |
| `shortcut_to_stg_subscription_lifecycle` | `needs_manual_review` | `fail` | failed rule #1 (sources only but disallowed transforms) and no other rule matched | ['int_exptrans1', 'int_rnktrans'], ['int_exptrans', 'int_srttrans1'], ['int_srttrans1', 'int_jnrtrans'], ['int_exp_src_subscription_detail1_bind', 'int_exp_src_subscription_detail1'], ['int_exp_src_subscription_detail1', 'int_union1'], ['int_union1', 'int_exp_cast_to_int_bind'], ['int_exp_cast_to_int_bind', 'int_exp_cast_to_int'], ['int_exp_cast_to_int', 'lkp_lkp_ref_billing_region'], ['map_mapplet_normalize_billing_date_bind', 'map_mapplet_normalize_billing_date_exp_date_prep'], ['int_mapplet_normalize_billing_date', 'int_exp_fields_bind'] |

## informatica/informatica_xml_sq_user_defined_join_two_tables (etl_to_dbt export format)

- **pipeline_id:** `informatica_xml_sq_user_defined_join_two_tables`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 4
- **modern models:** 1
- **CTEs collapsed:** 0
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_out` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | — |

## informatica/informatica_xml_transform_pipeline (etl_to_dbt export format)

- **pipeline_id:** `informatica_xml_transform_pipeline`
- **overall status:** `failed_parity`
- **legacy transformations (manifest):** 11
- **modern models:** 3
- **CTEs collapsed:** 6
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_joined` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_orders', 'int_jnr_orders'], ['sq_sq_customers', 'int_jnr_orders'] |
| `tgt_union` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_un_orders'], ['sq_sq_customers', 'int_un_orders'] |
| `tgt_vars` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_customers', 'int_exp_vars_prep'], ['int_exp_vars_prep', 'int_exp_vars'] |

## informatica/informatica_xml_update_strategy_pipeline (etl_to_dbt export format)

- **pipeline_id:** `informatica_xml_update_strategy_pipeline`
- **overall status:** `success`
- **legacy transformations (manifest):** 5
- **modern models:** 1
- **CTEs collapsed:** 2
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_orders` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_exp_orders'], ['int_exp_orders', 'int_upd_orders'] |

## informatica/orchestration_infa_synthetic_nonconforming_names (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_synthetic_nonconforming_names`
- **overall status:** `success`
- **legacy transformations (manifest):** 3
- **modern models:** 1
- **CTEs collapsed:** 0
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_row` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | — |

## informatica/orchestration_infa_synthetic_standalone_worklet_root (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_synthetic_standalone_worklet_root`
- **overall status:** `success`
- **legacy transformations (manifest):** 3
- **modern models:** 1
- **CTEs collapsed:** 0
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_row` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | — |

## informatica/orchestration_infa_wf_enterprise_daily_run (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wf_enterprise_daily_run`
- **overall status:** `failed_parity`
- **legacy transformations (manifest):** 25
- **modern models:** 4
- **CTEs collapsed:** 9
- **models NEEDS_MANUAL_REVIEW:** 3

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_sales_rollup` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_sales_detail', 'int_agg_multi_group'] |
| `tgt_txn_enriched` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_txn', 'lkp_lkp_cust'] |
| `tgt_claims_flagged` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_claims', 'int_fil_active'], ['int_fil_active', 'int_rtr_high_low'], ['int_rtr_high_low', 'int_exp_high_flag'], ['int_exp_low_flag', 'int_un_flagged_claims'], ['int_exp_high_flag', 'int_un_flagged_claims'] |
| `tgt_dim_customer` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_customer_dim', 'int_exp_scd_dates'], ['int_exp_scd_dates', 'int_upd_scd'] |

## informatica/orchestration_infa_wf_enterprise_master_repository (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wf_enterprise_master_repository`
- **overall status:** `failed_parity`
- **legacy transformations (manifest):** 245
- **modern models:** 51
- **CTEs collapsed:** 101
- **models NEEDS_MANUAL_REVIEW:** 26

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_distinct` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_sales', 'int_agg_distinct'] |
| `tgt_summary` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_sales', 'int_agg_summary'] |
| `tgt_global` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_sales', 'int_agg_global'] |
| `tgt_customers` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | — |
| `tgt_orders` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_exp_orders'] |
| `tgt_orders_2` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | — |
| `tgt_orders_3` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | — |
| `tgt_union_out` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_branch_a', 'int_exp_branch_a'], ['sq_sq_branch_b', 'int_exp_branch_b'], ['sq_sq_branch_c', 'int_exp_branch_c'], ['int_exp_branch_c', 'int_union_custom'], ['int_exp_branch_b', 'int_union_custom'], ['int_exp_branch_a', 'int_union_custom'] |
| `tgt_customers_2` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_customers', 'int_exp_customers'] |
| `tgt_orders_4` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_exp_orders'] |
| `shortcut_to_stg_subscriber_account_key` | `needs_manual_review` | `fail` | failed rule #1 (sources only but disallowed transforms) and no other rule matched | ['int_exptrans1', 'int_rnktrans'], ['int_exptrans', 'int_srttrans1'], ['int_srttrans1', 'int_jnrtrans'], ['int_exp_src_subscription_detail1_bind', 'int_exp_src_subscription_detail1'], ['int_exp_src_subscription_detail1', 'int_union1'], ['int_union1', 'int_exp_cast_to_int_bind'], ['int_exp_cast_to_int_bind', 'int_exp_cast_to_int'], ['int_exp_cast_to_int', 'lkp_lkp_ref_billing_region'], ['int_agg_for_subscriber_key_bind', 'int_agg_for_subscriber_key'] |
| `shortcut_to_stg_subscription_key` | `needs_manual_review` | `fail` | failed rule #1 (sources only but disallowed transforms) and no other rule matched | ['int_exptrans1', 'int_rnktrans'], ['int_exptrans', 'int_srttrans1'], ['int_srttrans1', 'int_jnrtrans'], ['int_exp_src_subscription_detail1_bind', 'int_exp_src_subscription_detail1'], ['int_exp_src_subscription_detail1', 'int_union1'], ['int_union1', 'int_exp_cast_to_int_bind'], ['int_exp_cast_to_int_bind', 'int_exp_cast_to_int'], ['int_exp_cast_to_int', 'lkp_lkp_ref_billing_region'] |
| `shortcut_to_stg_subscription_lifecycle` | `needs_manual_review` | `fail` | failed rule #1 (sources only but disallowed transforms) and no other rule matched | ['int_exptrans1', 'int_rnktrans'], ['int_exptrans', 'int_srttrans1'], ['int_srttrans1', 'int_jnrtrans'], ['int_exp_src_subscription_detail1_bind', 'int_exp_src_subscription_detail1'], ['int_exp_src_subscription_detail1', 'int_union1'], ['int_union1', 'int_exp_cast_to_int_bind'], ['int_exp_cast_to_int_bind', 'int_exp_cast_to_int'], ['int_exp_cast_to_int', 'lkp_lkp_ref_billing_region'] |
| `tgt_lnd_open_subscription_detail` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_ext_cdc', 'int_exp_delta'] |
| `tgt_fct_subscription_lifecycle` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_stg', 'int_exp_fct'], ['int_exp_fct', 'int_upd_fct'] |
| `tgt_joined` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_orders', 'int_jnr_orders'], ['sq_sq_customers', 'int_jnr_orders'] |
| `tgt_union` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_un_orders'], ['sq_sq_customers', 'int_un_orders'] |
| `tgt_vars` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_customers', 'int_exp_vars_prep'], ['int_exp_vars_prep', 'int_exp_vars'] |
| `tgt_orders_5` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_orders', 'int_exp_orders'], ['int_exp_orders', 'int_upd_orders'] |
| `tgt_sales_rollup` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_sales_detail', 'int_agg_multi_group'] |
| `tgt_value_table` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_value', 'int_value_exp'] |
| `tgt_txn_enriched` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_txn', 'lkp_lkp_cust'] |
| `dw_core_all_entities_master` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_fin_ap_vendor_master', 'int_exp_tag_vendor'], ['sq_sq_hr_core_employee_master', 'int_exp_tag_employee'], ['sq_sq_fin_ar_customer_master', 'int_exp_tag_customer'], ['int_exp_tag_customer', 'int_un_all_entities'], ['int_exp_tag_employee', 'int_un_all_entities'], ['int_exp_tag_vendor', 'int_un_all_entities'] |
| `tgt_claims_flagged` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_claims', 'int_fil_active'], ['int_fil_active', 'int_rtr_high_low'], ['int_rtr_high_low', 'int_exp_high_flag'], ['int_exp_low_flag', 'int_un_flagged_claims'], ['int_exp_high_flag', 'int_un_flagged_claims'] |
| `tgt_dim_customer` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_customer_dim', 'int_exp_scd_dates'], ['int_exp_scd_dates', 'int_upd_scd'] |
| `tgt_log_processed` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_raw_log', 'int_exp_clean1'], ['int_exp_clean1', 'int_fil_not_debug'], ['int_fil_not_debug', 'lkp_lkp_severity_code'], ['int_exp_clean2', 'int_rtr_sev'], ['int_rtr_sev', 'int_exp_tag_critical'], ['int_exp_tag_normal', 'int_un_tagged'], ['int_exp_tag_critical', 'int_un_tagged'], ['int_un_tagged', 'int_srt_final'] |
| `tgt_inventory_valued` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_inventory_movement', 'lkp_lkp_unit_cost'] |
| `tgt_type_c` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_master_data', 'int_rtr_type'] |
| `tgt_type_a` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_master_data', 'int_rtr_type'] |
| `tgt_type_b` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_master_data', 'int_rtr_type'] |
| `tgt_student_grades` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_scores', 'int_exp_grade_prep'] |
| `tgt_clean_names` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | — |
| `tgt_region_summary` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_sales', 'int_rnk_top_sales'], ['int_srt_by_amt', 'int_agg_region_total'] |
| `tgt_product_names_clean` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | — |
| `tgt_supplier_names_clean` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | — |
| `tgt_accounts` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_new_accounts', 'int_exp_acct_key'] |
| `tgt_contacts` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_new_contacts', 'int_exp_contact_key'] |
| `tgt_customer_scd` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_customer_changes', 'int_exp_build_row'] |
| `tgt_leaderboard_sorted` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_leaderboard', 'int_srt_leaderboard'] |
| `tgt_order_enriched` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_order_header', 'int_jnr_cust'], ['sq_sq_src_customer', 'int_jnr_cust'], ['sq_sq_src_shipping', 'int_jnr_ship'] |
| `tgt_employee_full` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_employee', 'int_jnr_dept'], ['sq_sq_department', 'int_jnr_dept'], ['sq_sq_manager', 'int_jnr_mgr'] |
| `tgt_clean_labels` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | — |
| `dw_core_tmp_staging_events_clean` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_legacy_ops_tmp_staging_raw_events', 'int_fil_valid'] |
| `dw_core_tmp_staging_events_rejected` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_legacy_ops_tmp_staging_raw_events', 'int_fil_invalid'] |
| `tgt_all_events` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_src_web_events', 'int_un_all_events'], ['sq_sq_src_pos_events', 'int_un_all_events'], ['sq_sq_src_mobile_events', 'int_un_all_events'], ['sq_sq_src_callcenter_events', 'int_un_all_events'] |
| `tgt_electronics` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_rtr_category'] |
| `tgt_apparel` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_rtr_category'] |
| `tgt_grocery` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_rtr_category'] |
| `tgt_furniture` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_rtr_category'] |
| `tgt_toys` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_rtr_category'] |
| `tgt_default` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_rtr_category'] |

## informatica/orchestration_infa_wf_with_nested_worklet (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wf_with_nested_worklet`
- **overall status:** `failed_parity`
- **legacy transformations (manifest):** 17
- **modern models:** 3
- **CTEs collapsed:** 8
- **models NEEDS_MANUAL_REVIEW:** 2

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_sales_rollup` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_sales_detail', 'int_agg_multi_group'] |
| `tgt_claims_flagged` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_claims', 'int_fil_active'], ['int_fil_active', 'int_rtr_high_low'], ['int_rtr_high_low', 'int_exp_high_flag'], ['int_exp_low_flag', 'int_un_flagged_claims'], ['int_exp_high_flag', 'int_un_flagged_claims'] |
| `tgt_dim_customer` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_customer_dim', 'int_exp_scd_dates'], ['int_exp_scd_dates', 'int_upd_scd'] |

## informatica/orchestration_infa_wrapped_wf_m_aggregator (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_aggregator`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 8
- **modern models:** 3
- **CTEs collapsed:** 3
- **models NEEDS_MANUAL_REVIEW:** 2

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_distinct` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_sales', 'int_agg_distinct'] |
| `tgt_summary` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_sales', 'int_agg_summary'] |
| `tgt_global` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_sales', 'int_agg_global'] |

## informatica/orchestration_infa_wrapped_wf_m_aggregator_multi_groupby (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_aggregator_multi_groupby`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 4
- **modern models:** 1
- **CTEs collapsed:** 1
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_sales_rollup` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_sales_detail', 'int_agg_multi_group'] |

## informatica/orchestration_infa_wrapped_wf_m_colliding_names_stress (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_colliding_names_stress`
- **overall status:** `success`
- **legacy transformations (manifest):** 4
- **modern models:** 1
- **CTEs collapsed:** 1
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_value_table` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_value', 'int_value_exp'] |

## informatica/orchestration_infa_wrapped_wf_m_deep_lookup_chain (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_deep_lookup_chain`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 8
- **modern models:** 1
- **CTEs collapsed:** 1
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_txn_enriched` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_txn', 'lkp_lkp_cust'] |

## informatica/orchestration_infa_wrapped_wf_m_dunder_schema_names_3merge (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_dunder_schema_names_3merge`
- **overall status:** `success`
- **legacy transformations (manifest):** 11
- **modern models:** 1
- **CTEs collapsed:** 6
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `dw_core_all_entities_master` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_fin_ap_vendor_master', 'int_exp_tag_vendor'], ['sq_sq_hr_core_employee_master', 'int_exp_tag_employee'], ['sq_sq_fin_ar_customer_master', 'int_exp_tag_customer'], ['int_exp_tag_customer', 'int_un_all_entities'], ['int_exp_tag_employee', 'int_un_all_entities'], ['int_exp_tag_vendor', 'int_un_all_entities'] |

## informatica/orchestration_infa_wrapped_wf_m_filter_router_union_faninout (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_filter_router_union_faninout`
- **overall status:** `failed_parity`
- **legacy transformations (manifest):** 8
- **modern models:** 1
- **CTEs collapsed:** 5
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_claims_flagged` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_claims', 'int_fil_active'], ['int_fil_active', 'int_rtr_high_low'], ['int_rtr_high_low', 'int_exp_high_flag'], ['int_exp_low_flag', 'int_un_flagged_claims'], ['int_exp_high_flag', 'int_un_flagged_claims'] |

## informatica/orchestration_infa_wrapped_wf_m_informatica_scd_type2 (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_informatica_scd_type2`
- **overall status:** `failed_parity`
- **legacy transformations (manifest):** 5
- **modern models:** 1
- **CTEs collapsed:** 2
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_dim_customer` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_customer_dim', 'int_exp_scd_dates'], ['int_exp_scd_dates', 'int_upd_scd'] |

## informatica/orchestration_infa_wrapped_wf_m_long_linear_10stage (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_long_linear_10stage`
- **overall status:** `failed_parity`
- **legacy transformations (manifest):** 12
- **modern models:** 1
- **CTEs collapsed:** 8
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_log_processed` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_raw_log', 'int_exp_clean1'], ['int_exp_clean1', 'int_fil_not_debug'], ['int_fil_not_debug', 'lkp_lkp_severity_code'], ['int_exp_clean2', 'int_rtr_sev'], ['int_rtr_sev', 'int_exp_tag_critical'], ['int_exp_tag_normal', 'int_un_tagged'], ['int_exp_tag_critical', 'int_un_tagged'], ['int_un_tagged', 'int_srt_final'] |

## informatica/orchestration_infa_wrapped_wf_m_lookup_composite_condition (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_lookup_composite_condition`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 4
- **modern models:** 1
- **CTEs collapsed:** 1
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_inventory_valued` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_inventory_movement', 'lkp_lkp_unit_cost'] |

## informatica/orchestration_infa_wrapped_wf_m_mapplet (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_mapplet`
- **overall status:** `success`
- **legacy transformations (manifest):** 4
- **modern models:** 1
- **CTEs collapsed:** 3
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_customers` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_customers', 'map_mp_upper_inst_bind'], ['map_mp_upper_inst_bind', 'map_mp_upper_inst_exp_upper'], ['map_mp_upper_inst_exp_upper', 'int_mp_upper_inst'] |

## informatica/orchestration_infa_wrapped_wf_m_minimal (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_minimal`
- **overall status:** `success`
- **legacy transformations (manifest):** 4
- **modern models:** 1
- **CTEs collapsed:** 1
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_orders` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_exp_orders'] |

## informatica/orchestration_infa_wrapped_wf_m_missing_transformation (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_missing_transformation`
- **overall status:** `failed_parity`
- **legacy transformations (manifest):** 2
- **modern models:** 1
- **CTEs collapsed:** 0
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_orders` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | — |

## informatica/orchestration_infa_wrapped_wf_m_multi_target (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_multi_target`
- **overall status:** `failed_parity`
- **legacy transformations (manifest):** 6
- **modern models:** 2
- **CTEs collapsed:** 2
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_customers` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_customers', 'int_exp_customers'] |
| `tgt_orders` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_exp_orders'] |

## informatica/orchestration_infa_wrapped_wf_m_multi_target_nonsequential_load_order (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_multi_target_nonsequential_load_order`
- **overall status:** `success`
- **legacy transformations (manifest):** 6
- **modern models:** 3
- **CTEs collapsed:** 3
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_type_c` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_master_data', 'int_rtr_type'] |
| `tgt_type_a` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_master_data', 'int_rtr_type'] |
| `tgt_type_b` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_master_data', 'int_rtr_type'] |

## informatica/orchestration_infa_wrapped_wf_m_multi_union (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_multi_union`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 8
- **modern models:** 1
- **CTEs collapsed:** 6
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_union_out` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_branch_a', 'int_exp_branch_a'], ['sq_sq_branch_b', 'int_exp_branch_b'], ['sq_sq_branch_c', 'int_exp_branch_c'], ['int_exp_branch_c', 'int_union_custom'], ['int_exp_branch_b', 'int_union_custom'], ['int_exp_branch_a', 'int_union_custom'] |

## informatica/orchestration_infa_wrapped_wf_m_nested_conditional_expression (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_nested_conditional_expression`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 4
- **modern models:** 1
- **CTEs collapsed:** 1
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_student_grades` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_scores', 'int_exp_grade_prep'] |

## informatica/orchestration_infa_wrapped_wf_m_nested_mapplet_pipeline (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_nested_mapplet_pipeline`
- **overall status:** `success`
- **legacy transformations (manifest):** 4
- **modern models:** 1
- **CTEs collapsed:** 7
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_clean_names` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_raw_names', 'map_mp_outer_inst_bind'], ['map_mp_outer_inst_bind', 'map_mp_outer_inst__mp_inner_inst__bind'], ['map_mp_outer_inst__mp_inner_inst__bind', 'map_mp_outer_inst__mp_inner_inst__exp_trim'], ['map_mp_outer_inst__mp_inner_inst__exp_trim', 'int_mp_outer_inst__mp_inner_inst'], ['int_mp_outer_inst__mp_inner_inst', 'map_mp_outer_inst_exp_upper_bind'], ['map_mp_outer_inst_exp_upper_bind', 'map_mp_outer_inst_exp_upper'], ['map_mp_outer_inst_exp_upper', 'int_mp_outer_inst'] |

## informatica/orchestration_infa_wrapped_wf_m_rank_sorter_aggregator_chain (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_rank_sorter_aggregator_chain`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 6
- **modern models:** 1
- **CTEs collapsed:** 2
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_region_summary` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_sales', 'int_rnk_top_sales'], ['int_srt_by_amt', 'int_agg_region_total'] |

## informatica/orchestration_infa_wrapped_wf_m_reused_mapplet_twice (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_reused_mapplet_twice`
- **overall status:** `success`
- **legacy transformations (manifest):** 8
- **modern models:** 2
- **CTEs collapsed:** 6
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_product_names_clean` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_product_names', 'map_mp_normalize_product_bind'], ['map_mp_normalize_product_bind', 'map_mp_normalize_product_exp_normalize'], ['map_mp_normalize_product_exp_normalize', 'int_mp_normalize_product'] |
| `tgt_supplier_names_clean` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_supplier_names', 'map_mp_normalize_supplier_bind'], ['map_mp_normalize_supplier_bind', 'map_mp_normalize_supplier_exp_normalize'], ['map_mp_normalize_supplier_exp_normalize', 'int_mp_normalize_supplier'] |

## informatica/orchestration_infa_wrapped_wf_m_sequence_generator_reused (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_sequence_generator_reused`
- **overall status:** `success`
- **legacy transformations (manifest):** 9
- **modern models:** 2
- **CTEs collapsed:** 2
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_accounts` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_new_accounts', 'int_exp_acct_key'] |
| `tgt_contacts` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_new_contacts', 'int_exp_contact_key'] |

## informatica/orchestration_infa_wrapped_wf_m_sequence_update_strategy (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_sequence_update_strategy`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 6
- **modern models:** 1
- **CTEs collapsed:** 1
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_customer_scd` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_customer_changes', 'int_exp_build_row'] |

## informatica/orchestration_infa_wrapped_wf_m_sorter_multi_key (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_sorter_multi_key`
- **overall status:** `success`
- **legacy transformations (manifest):** 4
- **modern models:** 1
- **CTEs collapsed:** 1
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_leaderboard_sorted` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_leaderboard', 'int_srt_leaderboard'] |

## informatica/orchestration_infa_wrapped_wf_m_sq_user_defined_join_two_tables (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_sq_user_defined_join_two_tables`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 4
- **modern models:** 1
- **CTEs collapsed:** 0
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_out` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | — |

## informatica/orchestration_infa_wrapped_wf_m_star_join_4satellite (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_star_join_4satellite`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 12
- **modern models:** 1
- **CTEs collapsed:** 3
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_order_enriched` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_order_header', 'int_jnr_cust'], ['sq_sq_src_customer', 'int_jnr_cust'], ['sq_sq_src_shipping', 'int_jnr_ship'] |

## informatica/orchestration_infa_wrapped_wf_m_three_sq_two_joiner_chain (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_three_sq_two_joiner_chain`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 9
- **modern models:** 1
- **CTEs collapsed:** 3
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_employee_full` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_employee', 'int_jnr_dept'], ['sq_sq_department', 'int_jnr_dept'], ['sq_sq_manager', 'int_jnr_mgr'] |

## informatica/orchestration_infa_wrapped_wf_m_transforms (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_transforms`
- **overall status:** `failed_parity`
- **legacy transformations (manifest):** 11
- **modern models:** 3
- **CTEs collapsed:** 6
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_joined` | `needs_manual_review` | `pass` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | ['sq_sq_orders', 'int_jnr_orders'], ['sq_sq_customers', 'int_jnr_orders'] |
| `tgt_union` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_un_orders'], ['sq_sq_customers', 'int_un_orders'] |
| `tgt_vars` | `staging` | `fail` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_customers', 'int_exp_vars_prep'], ['int_exp_vars_prep', 'int_exp_vars'] |

## informatica/orchestration_infa_wrapped_wf_m_two_mapplets_chained (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_two_mapplets_chained`
- **overall status:** `success`
- **legacy transformations (manifest):** 5
- **modern models:** 1
- **CTEs collapsed:** 6
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_clean_labels` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_raw_labels', 'map_mp_trim_inst_bind'], ['map_mp_trim_inst_bind', 'map_mp_trim_inst_exp_trim'], ['map_mp_trim_inst_exp_trim', 'int_mp_trim_inst'], ['int_mp_trim_inst', 'map_mp_uppercase2_inst_bind'], ['map_mp_uppercase2_inst_bind', 'map_mp_uppercase2_inst_exp_upper2'], ['map_mp_uppercase2_inst_exp_upper2', 'int_mp_uppercase2_inst'] |

## informatica/orchestration_infa_wrapped_wf_m_underscore_schema_multi_target (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_underscore_schema_multi_target`
- **overall status:** `success`
- **legacy transformations (manifest):** 6
- **modern models:** 2
- **CTEs collapsed:** 2
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `dw_core_tmp_staging_events_clean` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_legacy_ops_tmp_staging_raw_events', 'int_fil_valid'] |
| `dw_core_tmp_staging_events_rejected` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_legacy_ops_tmp_staging_raw_events', 'int_fil_invalid'] |

## informatica/orchestration_infa_wrapped_wf_m_union_heterogeneous_4way (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_union_heterogeneous_4way`
- **overall status:** `success`
- **legacy transformations (manifest):** 10
- **modern models:** 1
- **CTEs collapsed:** 4
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_all_events` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_src_web_events', 'int_un_all_events'], ['sq_sq_src_pos_events', 'int_un_all_events'], ['sq_sq_src_mobile_events', 'int_un_all_events'], ['sq_sq_src_callcenter_events', 'int_un_all_events'] |

## informatica/orchestration_infa_wrapped_wf_m_update_strategy (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_update_strategy`
- **overall status:** `success`
- **legacy transformations (manifest):** 5
- **modern models:** 1
- **CTEs collapsed:** 2
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_orders` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_exp_orders'], ['int_exp_orders', 'int_upd_orders'] |

## informatica/orchestration_infa_wrapped_wf_m_wide_router_fanout (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_wide_router_fanout`
- **overall status:** `success`
- **legacy transformations (manifest):** 9
- **modern models:** 6
- **CTEs collapsed:** 6
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_electronics` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_rtr_category'] |
| `tgt_apparel` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_rtr_category'] |
| `tgt_grocery` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_rtr_category'] |
| `tgt_furniture` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_rtr_category'] |
| `tgt_toys` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_rtr_category'] |
| `tgt_default` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['sq_sq_orders', 'int_rtr_category'] |

## informatica/orchestration_infa_wrapped_wf_m_with_unsupported (etl_to_dbt export format)

- **pipeline_id:** `orchestration_infa_wrapped_wf_m_with_unsupported`
- **overall status:** `failed_parity`
- **legacy transformations (manifest):** 3
- **modern models:** 1
- **CTEs collapsed:** 0
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `tgt_orders` | `needs_manual_review` | `fail` | rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target' | — |

## wwi_corpus (etl_to_dbt export format)

- **pipeline_id:** `wwi_sales_star`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 11
- **modern models:** 6
- **CTEs collapsed:** 2
- **models NEEDS_MANUAL_REVIEW:** 1

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `raw_stg_customers` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['source_rows', 'filtered'] |
| `raw_int_sales_enriched` | `intermediate` | `pass` | matched rule #2: ref() upstream with lookup join | ['invoice_base', 'joined'] |
| `raw_tgt_dim_customer` | `marts` | `pass` | matched rule #3: direct 1:1 target mapping to DIM_CUSTOMER, update_strategy_scd | — |
| `raw_tgt_fct_invoice_lines` | `marts` | `pass` | matched rule #3: direct 1:1 target mapping to FCT_INVOICE_LINES, aggregator_fact_load | — |
| `raw_passthrough_ref_only` | `intermediate` | `pass` | matched rule #2: ref() upstream with projection/filter/expression | — |
| `raw_multi_consumer_window` | `needs_manual_review` | `pass` | failed rule #1 (sources only but disallowed transforms) and no other rule matched | — |

## Failures (unfiltered)

**informatica_stress_corpus_filter_router_union_faninout / tgt_claims_flagged**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Catalog Error: Table with name int_rtr_high_low does not exist!\nDid you mean \"sqlite_temp_schema\"?\n\nLINE 44:     FROM int_rtr_high_low base\n                  ^"
}
```
**informatica_stress_corpus_informatica_scd_type2 / tgt_dim_customer**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Parser Error: syntax error at or near \")\"\n\nLINE 29: ... > (SELECT coalesce(max(START_DATE), '1900-01-01') FROM )\n                                                                    ^"
}
```
**informatica_stress_corpus_long_linear_10stage / tgt_log_processed**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Catalog Error: Table with name int_rtr_sev does not exist!\nDid you mean \"sqlite_master\"?\n\nLINE 78:     FROM int_rtr_sev base\n                  ^"
}
```
**informatica_xml_minimal_with_missing_transformation / tgt_orders**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Parser Error: syntax error at end of input"
}
```
**informatica_xml_minimal_with_unsupported / tgt_orders**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Parser Error: syntax error at end of input"
}
```
**informatica_xml_multi_target_pipeline / tgt_customers**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Binder Error: Referenced column \"IS_DELETED\" not found in FROM clause!\nCandidate bindings: \"CUSTOMER_ID\"\n\nLINE 7: ... CUSTOMER_ID, CUSTOMER_NAME FROM dw_core.dim_customers WHERE IS_DELETED = 0\n                                                                        ^"
}
```
**informatica_xml_multi_target_pipeline / tgt_orders**

```json
{
  "status": "fail",
  "row_count_match": true,
  "column_diff": [
    {
      "column": "__rows__",
      "raw_null_count": 6,
      "remodeled_null_count": 6,
      "sample_mismatches": [
        {
          "kind": "row_diff_count",
          "diff_rows": 8,
          "sample": [
            [
              "order_id_3",
              "customer_id_3",
              "2026-09-27 11:19:13.547511+03:00"
            ],
            [
              "order_id_2",
              "customer_id_2",
              "2026-09-27 11:19:13.547511+03:00"
            ],
            [
              null,
              null,
              "2026-09-27 11:19:13.547511+03:00"
            ],
            [
              "order_id_4",
              "customer_id_4",
              "2026-09-27 11:19:13.547511+03:00"
            ],
            [
              "order_id_4",
              "customer_id_4",
              "2026-09-27 11:19:13.547976+03:00"
            ]
          ]
        }
      ]
    }
  ],
  "error": null
}
```
**informatica_xml_real_world_complex_pipeline / tgt_fct_subscription_lifecycle**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Parser Error: syntax error at or near \"AS\"\n\nLINE 8:          AS load_batch_id\n                 ^"
}
```
**informatica_xml_real_world_complex_pipeline / tgt_lnd_open_subscription_detail**

```json
{
  "status": "fail",
  "row_count_match": null,
  "column_diff": [],
  "error": "Conversion Error: invalid timestamp field format: \"\", expected format is (YYYY-MM-DD HH:MM:SS[.US][\u00b1HH[:MM[:SS]]| ZONE])\n\nLINE 3: ... cdc.src_ext_cdc_subscription_events WHERE TX_TIMESTAMP >= CAST('' AS TIMESTAMP)\n                                                                      ^"
}
```
**informatica_xml_real_world_complex_pipeline / shortcut_to_stg_subscriber_account_key**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: \"Unknown source: ('dwh', 'ref_rate_plan_aliases')\""
}
```
**informatica_xml_real_world_complex_pipeline / shortcut_to_stg_subscription_key**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: \"Unknown source: ('dwh', 'ref_rate_plan_aliases')\""
}
```
**informatica_xml_real_world_complex_pipeline / shortcut_to_stg_subscription_lifecycle**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: \"Unknown source: ('dwh', 'ref_rate_plan_aliases')\""
}
```
**informatica_xml_transform_pipeline / tgt_vars**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Binder Error: Referenced column \"RAW_DATE\" not found in FROM clause!\nCandidate bindings: \"CUSTOMER_ID\"\n\nLINE 8:         substr(RAW_DATE, 1, 10) AS PARSED_DATE\n                       ^"
}
```
**orchestration_infa_wf_enterprise_daily_run / tgt_txn_enriched**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: \"Unknown source: ('dbo', 'ref_customer')\""
}
```
**orchestration_infa_wf_enterprise_daily_run / tgt_claims_flagged**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Catalog Error: Table with name int_rtr_high_low does not exist!\nDid you mean \"parity_rem_tgt_sales_rollup\"?\n\nLINE 44:     FROM int_rtr_high_low base\n                  ^"
}
```
**orchestration_infa_wf_enterprise_daily_run / tgt_dim_customer**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Parser Error: syntax error at or near \")\"\n\nLINE 29: ... > (SELECT coalesce(max(START_DATE), '1900-01-01') FROM )\n                                                                    ^"
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_customers**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Parser Error: syntax error at end of input"
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_orders_2**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Parser Error: syntax error at end of input"
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_orders_3**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Parser Error: syntax error at end of input"
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_customers_2**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: \"Unknown source: ('dw_core', 'dim_customers')\""
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_orders_4**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: \"Unknown source: ('dw_core', 'fct_orders')\""
}
```
**orchestration_infa_wf_enterprise_master_repository / shortcut_to_stg_subscriber_account_key**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: \"Unknown source: ('dwh', 'ref_rate_plan_aliases')\""
}
```
**orchestration_infa_wf_enterprise_master_repository / shortcut_to_stg_subscription_key**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: \"Unknown source: ('dwh', 'ref_rate_plan_aliases')\""
}
```
**orchestration_infa_wf_enterprise_master_repository / shortcut_to_stg_subscription_lifecycle**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: \"Unknown source: ('dwh', 'ref_rate_plan_aliases')\""
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_lnd_open_subscription_detail**

```json
{
  "status": "fail",
  "row_count_match": null,
  "column_diff": [],
  "error": "Conversion Error: invalid timestamp field format: \"\", expected format is (YYYY-MM-DD HH:MM:SS[.US][\u00b1HH[:MM[:SS]]| ZONE])\n\nLINE 3: ... cdc.src_ext_cdc_subscription_events WHERE TX_TIMESTAMP >= CAST('' AS TIMESTAMP)\n                                                                      ^"
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_fct_subscription_lifecycle**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: \"Unknown source: ('billing_core', 'stg_subscription_lifecycle')\""
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_joined**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Binder Error: Referenced column \"CUSTOMER_ID\" not found in FROM clause!\nCandidate bindings: \"CUSTOMER_NAME\"\n\nLINE 7: SELECT CUSTOMER_ID, REGION FROM dbo.src_customers\n               ^"
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_union**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Binder Error: Referenced column \"CUSTOMER_ID\" not found in FROM clause!\nCandidate bindings: \"CUSTOMER_NAME\", \"ORDER_ID\"\n\nLINE 6: SELECT ORDER_ID, CUSTOMER_ID FROM dbo.src_orders\n                         ^"
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_vars**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Binder Error: Referenced column \"CUSTOMER_ID\" not found in FROM clause!\nCandidate bindings: \"CUSTOMER_NAME\"\n\nLINE 10: SELECT CUSTOMER_ID, REGION FROM dbo.src_customers\n                ^"
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_orders_5**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Parser Error: syntax error at or near \")\"\n\nLINE 20: ... > (SELECT coalesce(max(CREATED_DATE), '1900-01-01') FROM )\n                                                                      ^"
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_txn_enriched**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: \"Unknown source: ('dbo', 'ref_customer')\""
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_claims_flagged**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Catalog Error: Table with name int_rtr_high_low does not exist!\nDid you mean \"parity_rem_tgt_global\"?\n\nLINE 44:     FROM int_rtr_high_low base\n                  ^"
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_dim_customer**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Parser Error: syntax error at or near \")\"\n\nLINE 29: ... > (SELECT coalesce(max(START_DATE), '1900-01-01') FROM )\n                                                                    ^"
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_log_processed**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: \"Unknown source: ('dbo', 'ref_severity')\""
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_inventory_valued**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: \"Unknown source: ('dbo', 'ref_inventory_cost')\""
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_clean_names**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Parser Error: syntax error at end of input"
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_region_summary**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Binder Error: Referenced column \"SALESPERSON\" not found in FROM clause!\nCandidate bindings: \"CUSTOMER_ID\"\n\nLINE 10: SELECT SALESPERSON, REGION, AMT FROM dbo.src_sales\n                ^"
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_product_names_clean**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Parser Error: syntax error at end of input"
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_supplier_names_clean**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Parser Error: syntax error at end of input"
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_clean_labels**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Parser Error: syntax error at end of input"
}
```
**orchestration_infa_wf_enterprise_master_repository / dw_core_tmp_staging_events_clean**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: \"Unknown source: ('legacy_ops_tmp', 'staging_raw_events')\""
}
```
**orchestration_infa_wf_enterprise_master_repository / dw_core_tmp_staging_events_rejected**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: \"Unknown source: ('legacy_ops_tmp', 'staging_raw_events')\""
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_electronics**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Binder Error: Referenced column \"CATEGORY\" not found in FROM clause!\nCandidate bindings: \"CUSTOMER_NAME\", \"ORDER_ID\"\n\nLINE 5: SELECT ORDER_ID, CATEGORY, AMT FROM dbo.src_orders\n                         ^"
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_apparel**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Binder Error: Referenced column \"CATEGORY\" not found in FROM clause!\nCandidate bindings: \"CUSTOMER_NAME\", \"ORDER_ID\"\n\nLINE 5: SELECT ORDER_ID, CATEGORY, AMT FROM dbo.src_orders\n                         ^"
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_grocery**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Binder Error: Referenced column \"CATEGORY\" not found in FROM clause!\nCandidate bindings: \"CUSTOMER_NAME\", \"ORDER_ID\"\n\nLINE 5: SELECT ORDER_ID, CATEGORY, AMT FROM dbo.src_orders\n                         ^"
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_furniture**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Binder Error: Referenced column \"CATEGORY\" not found in FROM clause!\nCandidate bindings: \"CUSTOMER_NAME\", \"ORDER_ID\"\n\nLINE 5: SELECT ORDER_ID, CATEGORY, AMT FROM dbo.src_orders\n                         ^"
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_toys**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Binder Error: Referenced column \"CATEGORY\" not found in FROM clause!\nCandidate bindings: \"CUSTOMER_NAME\", \"ORDER_ID\"\n\nLINE 5: SELECT ORDER_ID, CATEGORY, AMT FROM dbo.src_orders\n                         ^"
}
```
**orchestration_infa_wf_enterprise_master_repository / tgt_default**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Binder Error: Referenced column \"CATEGORY\" not found in FROM clause!\nCandidate bindings: \"CUSTOMER_NAME\", \"ORDER_ID\"\n\nLINE 5: SELECT ORDER_ID, CATEGORY, AMT FROM dbo.src_orders\n                         ^"
}
```
**orchestration_infa_wf_with_nested_worklet / tgt_claims_flagged**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Catalog Error: Table with name int_rtr_high_low does not exist!\nDid you mean \"parity_rem_tgt_sales_rollup\"?\n\nLINE 44:     FROM int_rtr_high_low base\n                  ^"
}
```
**orchestration_infa_wf_with_nested_worklet / tgt_dim_customer**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Parser Error: syntax error at or near \")\"\n\nLINE 29: ... > (SELECT coalesce(max(START_DATE), '1900-01-01') FROM )\n                                                                    ^"
}
```
**orchestration_infa_wrapped_wf_m_filter_router_union_faninout / tgt_claims_flagged**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Catalog Error: Table with name int_rtr_high_low does not exist!\nDid you mean \"sqlite_temp_schema\"?\n\nLINE 44:     FROM int_rtr_high_low base\n                  ^"
}
```
**orchestration_infa_wrapped_wf_m_informatica_scd_type2 / tgt_dim_customer**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Parser Error: syntax error at or near \")\"\n\nLINE 29: ... > (SELECT coalesce(max(START_DATE), '1900-01-01') FROM )\n                                                                    ^"
}
```
**orchestration_infa_wrapped_wf_m_long_linear_10stage / tgt_log_processed**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Catalog Error: Table with name int_rtr_sev does not exist!\nDid you mean \"sqlite_master\"?\n\nLINE 78:     FROM int_rtr_sev base\n                  ^"
}
```
**orchestration_infa_wrapped_wf_m_missing_transformation / tgt_orders**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Parser Error: syntax error at end of input"
}
```
**orchestration_infa_wrapped_wf_m_multi_target / tgt_customers**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Binder Error: Referenced column \"IS_DELETED\" not found in FROM clause!\nCandidate bindings: \"CUSTOMER_ID\"\n\nLINE 7: ... CUSTOMER_ID, CUSTOMER_NAME FROM dw_core.dim_customers WHERE IS_DELETED = 0\n                                                                        ^"
}
```
**orchestration_infa_wrapped_wf_m_multi_target / tgt_orders**

```json
{
  "status": "fail",
  "row_count_match": true,
  "column_diff": [
    {
      "column": "__rows__",
      "raw_null_count": 6,
      "remodeled_null_count": 6,
      "sample_mismatches": [
        {
          "kind": "row_diff_count",
          "diff_rows": 8,
          "sample": [
            [
              "order_id_4",
              "customer_id_4",
              "2026-09-27 11:19:20.595539+03:00"
            ],
            [
              null,
              null,
              "2026-09-27 11:19:20.595539+03:00"
            ],
            [
              "order_id_2",
              "customer_id_2",
              "2026-09-27 11:19:20.595539+03:00"
            ],
            [
              "order_id_3",
              "customer_id_3",
              "2026-09-27 11:19:20.595539+03:00"
            ],
            [
              "order_id_4",
              "customer_id_4",
              "2026-09-27 11:19:20.596009+03:00"
            ]
          ]
        }
      ]
    }
  ],
  "error": null
}
```
**orchestration_infa_wrapped_wf_m_transforms / tgt_vars**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Binder Error: Referenced column \"RAW_DATE\" not found in FROM clause!\nCandidate bindings: \"CUSTOMER_ID\"\n\nLINE 8:         substr(RAW_DATE, 1, 10) AS PARSED_DATE\n                       ^"
}
```
**orchestration_infa_wrapped_wf_m_with_unsupported / tgt_orders**

```json
{
  "status": "fail",
  "row_count_match": false,
  "column_diff": [],
  "error": "explain_gate: Parser Error: syntax error at end of input"
}
```

## NEEDS_MANUAL_REVIEW (unfiltered)

- `informatica_stress_corpus_aggregator_multi_groupby` → `tgt_sales_rollup`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `informatica_stress_corpus_deep_lookup_chain` → `tgt_txn_enriched`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `informatica_stress_corpus_informatica_scd_type2` → `tgt_dim_customer`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `informatica_stress_corpus_long_linear_10stage` → `tgt_log_processed`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `informatica_stress_corpus_lookup_composite_condition` → `tgt_inventory_valued`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `informatica_stress_corpus_nested_conditional_expression` → `tgt_student_grades`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `informatica_stress_corpus_rank_sorter_aggregator_chain` → `tgt_region_summary`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `informatica_stress_corpus_sequence_update_strategy` → `tgt_customer_scd`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `informatica_stress_corpus_star_join_4satellite` → `tgt_order_enriched`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `informatica_stress_corpus_three_sq_two_joiner_chain` → `tgt_employee_full`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `informatica_xml_aggregator_pipeline` → `tgt_summary`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `informatica_xml_aggregator_pipeline` → `tgt_global`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `informatica_xml_minimal_with_missing_transformation` → `tgt_orders`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `informatica_xml_minimal_with_unsupported` → `tgt_orders`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `informatica_xml_multi_input_union` → `tgt_union_out`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `informatica_xml_real_world_complex_pipeline` → `tgt_fct_subscription_lifecycle`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `informatica_xml_real_world_complex_pipeline` → `shortcut_to_stg_subscriber_account_key`: failed rule #1 (sources only but disallowed transforms) and no other rule matched
- `informatica_xml_real_world_complex_pipeline` → `shortcut_to_stg_subscription_key`: failed rule #1 (sources only but disallowed transforms) and no other rule matched
- `informatica_xml_real_world_complex_pipeline` → `shortcut_to_stg_subscription_lifecycle`: failed rule #1 (sources only but disallowed transforms) and no other rule matched
- `informatica_xml_sq_user_defined_join_two_tables` → `tgt_out`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `informatica_xml_transform_pipeline` → `tgt_joined`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_daily_run` → `tgt_sales_rollup`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_daily_run` → `tgt_txn_enriched`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_daily_run` → `tgt_dim_customer`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_summary`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_global`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_customers`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_orders_2`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_orders_3`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_union_out`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `shortcut_to_stg_subscriber_account_key`: failed rule #1 (sources only but disallowed transforms) and no other rule matched
- `orchestration_infa_wf_enterprise_master_repository` → `shortcut_to_stg_subscription_key`: failed rule #1 (sources only but disallowed transforms) and no other rule matched
- `orchestration_infa_wf_enterprise_master_repository` → `shortcut_to_stg_subscription_lifecycle`: failed rule #1 (sources only but disallowed transforms) and no other rule matched
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_fct_subscription_lifecycle`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_joined`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_orders_5`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_sales_rollup`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_txn_enriched`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_dim_customer`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_log_processed`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_inventory_valued`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_student_grades`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_clean_names`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_region_summary`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_product_names_clean`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_supplier_names_clean`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_customer_scd`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_order_enriched`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_employee_full`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_enterprise_master_repository` → `tgt_clean_labels`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_with_nested_worklet` → `tgt_sales_rollup`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wf_with_nested_worklet` → `tgt_dim_customer`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wrapped_wf_m_aggregator` → `tgt_summary`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wrapped_wf_m_aggregator` → `tgt_global`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wrapped_wf_m_aggregator_multi_groupby` → `tgt_sales_rollup`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wrapped_wf_m_deep_lookup_chain` → `tgt_txn_enriched`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wrapped_wf_m_informatica_scd_type2` → `tgt_dim_customer`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wrapped_wf_m_long_linear_10stage` → `tgt_log_processed`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wrapped_wf_m_lookup_composite_condition` → `tgt_inventory_valued`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wrapped_wf_m_missing_transformation` → `tgt_orders`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wrapped_wf_m_multi_union` → `tgt_union_out`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wrapped_wf_m_nested_conditional_expression` → `tgt_student_grades`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wrapped_wf_m_rank_sorter_aggregator_chain` → `tgt_region_summary`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wrapped_wf_m_sequence_update_strategy` → `tgt_customer_scd`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wrapped_wf_m_sq_user_defined_join_two_tables` → `tgt_out`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wrapped_wf_m_star_join_4satellite` → `tgt_order_enriched`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wrapped_wf_m_three_sq_two_joiner_chain` → `tgt_employee_full`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wrapped_wf_m_transforms` → `tgt_joined`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `orchestration_infa_wrapped_wf_m_with_unsupported` → `tgt_orders`: rule #3 ambiguous: legacy target mapping present but unknown last_transformation_type='target'
- `wwi_sales_star` → `raw_multi_consumer_window`: failed rule #1 (sources only but disallowed transforms) and no other rule matched
