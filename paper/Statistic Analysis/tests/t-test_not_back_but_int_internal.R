library("Rcmdr", lib.loc="~/R/win-library/3.5")

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="x_y_not_back_but_int", stringsAsFactors=TRUE)

with(Dataset, (t.test(Xdoc, Ydoc, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  Xdoc and Ydoc
# t = -12.838, df = 22271, p-value < 2.2e-16
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   -92.33016 -67.87126
# sample estimates:
#   mean of the differences 
# -80.10071 

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="x_f_not_back_but_int", stringsAsFactors=TRUE)

with(Dataset, (t.test(Xdoc, Nr_frame, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  Xdoc and Nr_frame
# t = -3.9769, df = 15, p-value = 0.001215
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   -1227.9011  -370.9739
# sample estimates:
#   mean of the differences 
# -799.4375 

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="y_f_not_back_but_int", stringsAsFactors=TRUE)


with(Dataset, (t.test(Ydoc, Nr_frame, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  Ydoc and Nr_frame
# t = -1.1617, df = 15, p-value = 0.2635
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   -705.3377  207.7127
# sample estimates:
#   mean of the differences 
# -248.8125