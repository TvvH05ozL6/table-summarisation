library("Rcmdr", lib.loc="~/R/win-library/3.5")
Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="x_y_back_not_int", stringsAsFactors=TRUE)

with(Dataset, (t.test(Xdoc, Ydoc, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  Xdoc and Ydoc
# t = -3.9369, df = 15750, p-value = 0.00008288
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   -54.41666 -18.24171
# sample estimates:
#   mean of the differences 
# -36.32919

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="x_f_back_not_int", stringsAsFactors=TRUE)

with(Dataset, (t.test(Xdoc, Nr_frame, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  Xdoc and Nr_frame
# t = -3.3826, df = 18, p-value = 0.003317
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   -1459.1508  -341.0597
# sample estimates:
#   mean of the differences 
# -900.1053 

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="y_f_back_not_int", stringsAsFactors=TRUE)

with(Dataset, (t.test(Ydoc, Nr_frame, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  Ydoc and Nr_frame
# t = -5.044, df = 18, p-value = 0.00008442
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   -1886.5819  -777.1024
# sample estimates:
#   mean of the differences 
# -1331.842 