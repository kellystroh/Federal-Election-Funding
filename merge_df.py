import build_financial_df as fin
import build_results_df as res
merge_df_start = res.results_GE.merge(fin.finance_df, how="inner", left_on="elec-cand", right_on="ELEC-CAND")
merge_df_start.head(5)