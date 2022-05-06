library("Rcmdr", lib.loc="~/R/win-library/3.5")

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="x_y_not_back_and_int", stringsAsFactors=TRUE)

with(Dataset, (t.test(Xdoc, Ydoc, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  Xdoc and Ydoc
# t = -11.18, df = 19492, p-value < 2.2e-16
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   -117.12510  -82.18142
# sample estimates:
#   mean of the differences 
# -99.65326 

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="x_f_not_back_and_int", stringsAsFactors=TRUE)

with(Dataset, (t.test(Xdoc, Nr_frame, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  Xdoc and Nr_frame
# t = -2.7718, df = 13, p-value = 0.01586
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   -1205.048  -149.381
# sample estimates:
#   mean of the differences 
# -677.2143 

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="y_f_not_back_and_int", stringsAsFactors=TRUE)

with(Dataset, (t.test(Ydoc, Nr_frame, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  Ydoc and Nr_frame
# t = -4.4967, df = 13, p-value = 0.0006009
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   -1519.2389  -533.1896
# sample estimates:
#   mean of the differences 
# -1026.214