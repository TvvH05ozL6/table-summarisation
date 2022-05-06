library("Rcmdr", lib.loc="~/R/win-library/3.5")

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="backint_backnotint", stringsAsFactors=TRUE)

with(Dataset, (t.test(back_int, back_not_int, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  back_int and back_not_int
# t = -34.429, df = 27253, p-value < 2.2e-16
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   -171.3931 -152.9292
# sample estimates:
#   mean of the differences 
# -162.1612 

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="backint_nobackbutint", stringsAsFactors=TRUE)

with(Dataset, (t.test(back_int, no_back_but_int, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  back_int and no_back_but_int
# t = 13.397, df = 22271, p-value < 2.2e-16
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   73.05568 98.09635
# sample estimates:
#   mean of the differences 
# 85.57601 

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="backint_nobackandint", stringsAsFactors=TRUE)

with(Dataset, (t.test(back_int, no_back_and_int, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  back_int and no_back_and_int
# t = 0.79312, df = 19492, p-value = 0.4277
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   -7.714639 18.201070
# sample estimates:
#   mean of the differences 
# 5.243216 

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="backnoint_intnoback", stringsAsFactors=TRUE)

with(Dataset, (t.test(back_but_no_int, no_back_but_int, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  back_but_no_int and no_back_but_int
# t = 35.876, df = 22271, p-value < 2.2e-16
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   203.1144 226.5913
# sample estimates:
#   mean of the differences 
# 214.8528 

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="nobackbutint_nobackint", stringsAsFactors=TRUE)

with(Dataset, (t.test(no_back_and_int, no_back_but_int, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  no_back_and_int and no_back_but_int
# t = 14.233, df = 19492, p-value < 2.2e-16
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   82.00055 108.19378
# sample estimates:
#   mean of the differences 
# 95.09716 

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="nointbutback_nobackandint", stringsAsFactors=TRUE)


with(Dataset, (t.test(back_but_no_int, no_back_and_int, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  back_but_no_int and no_back_and_int
# t = 15.489, df = 19492, p-value < 2.2e-16
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   89.52981 115.47260
# sample estimates:
#   mean of the differences 
# 102.5012

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="y_backint_nobackbutint", stringsAsFactors=TRUE)

with(Dataset, (t.test(back_and_int, no_back_but_int, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  back_and_int and no_back_but_int
# t = -33.892, df = 22271, p-value < 2.2e-16
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   -190.3716 -169.5561
# sample estimates:
#   mean of the differences 
# -179.9639 

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="y_backint_backbutnotint", stringsAsFactors=TRUE)

with(Dataset, (t.test(back_and_int, back_but_no_int, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  back_and_int and back_but_no_int
# t = -36.883, df = 15750, p-value < 2.2e-16
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   -350.3483 -314.9893
# sample estimates:
#   mean of the differences 
# -332.6688 

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="y_backint_nobackint", stringsAsFactors=TRUE)

with(Dataset, (t.test(back_and_int, no_back_int, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  back_and_int and no_back_int
# t = -32.901, df = 19492, p-value < 2.2e-16
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   -281.6336 -249.9633
# sample estimates:
#   mean of the differences 
# -265.7984 

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="y_backbutnoint_nobackbutint", stringsAsFactors=TRUE)

with(Dataset, (t.test(back_but_no_int, no_back_but_int, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  back_but_no_int and no_back_but_int
# t = 26.508, df = 15750, p-value < 2.2e-16
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   234.8377 272.3409
# sample estimates:
#   mean of the differences 
# 253.5893 

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="y_backbutnoint_nobackint", stringsAsFactors=TRUE)

with(Dataset, (t.test(back_but_no_int, no_back_and_int, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  back_but_no_int and no_back_and_int
# t = 2.0424, df = 15750, p-value = 0.04112
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   0.9728981 47.2992116
# sample estimates:
#   mean of the differences 
# 24.13605

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="y_nobackbutint_nobackint", stringsAsFactors=TRUE)

with(Dataset, (t.test(no_back_but_int, no_back_int, alternative='two.sided',conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  no_back_but_int and no_back_int
# t = -17.493, df = 19492, p-value < 2.2e-16
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   -178.0417 -142.1626
# sample estimates:
#   mean of the differences 
# -160.1021 

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="Foglio31", stringsAsFactors=TRUE)

with(Dataset, (t.test(back_and_int, back_no_int, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  back_and_int and back_no_int
# t = 0.47201, df = 18, p-value = 0.6426
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   -5.630625  8.893783
# sample estimates:
#   mean of the differences 
# 1.631579 

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="Foglio32", stringsAsFactors=TRUE)

with(Dataset, (t.test(back_and_int, int_no_back, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  back_and_int and int_no_back
# t = 2.0868, df = 15, p-value = 0.05439
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   -0.1363225 12.8863225
# sample estimates:
#   mean of the differences 
# 6.375 

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="Foglio33", stringsAsFactors=TRUE)

with(Dataset, (t.test(back_and_int, no_back_int, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  back_and_int and no_back_int
# t = 1.1363, df = 13, p-value = 0.2763
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   -3.862196 12.433624
# sample estimates:
#   mean of the differences 
# 4.285714 

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="Foglio34", stringsAsFactors=TRUE)

with(Dataset, (t.test(back_no_int, int_no_back, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  back_no_int and int_no_back
# t = 1.8696, df = 15, p-value = 0.08118
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   -0.8576663 13.1076663
# sample estimates:
#   mean of the differences 
# 6.125

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="Foglio35", stringsAsFactors=TRUE)

with(Dataset, (t.test(back_no_int, no_back_int, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  back_no_int and no_back_int
# t = 0, df = 13, p-value = 1
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   -6.824174  6.824174
# sample estimates:
#   mean of the differences 
# 0 

Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="Foglio36", stringsAsFactors=TRUE)

with(Dataset, (t.test(int_no_back, no_back_int, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  int_no_back and no_back_int
# t = -0.92509, df = 13, p-value = 0.3718
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   -10.005887   4.005887
# sample estimates:
#   mean of the differences 
# -3 