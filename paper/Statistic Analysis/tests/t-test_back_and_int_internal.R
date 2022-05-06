library("Rcmdr", lib.loc="~/R/win-library/3.5")  
Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, , sheet="x_y_back_and_int", na="",  sheet="Foglio1", stringsAsFactors=TRUE)


 with(Dataset, (t.test(Xdoc, Ydoc, alternative='two.sided', conf.level=.95, paired=TRUE)))

# Paired t-test
# 
# data:  Xdoc and Ydoc
# t = 30.498, df = 62615, p-value < 2.2e-16
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   137.7483 156.6699
# sample estimates:
#   mean of the differences 
# 147.2091
 
  Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="x_f_back_and_int", stringsAsFactors=TRUE)

 
   with(Dataset, (t.test(Xdoc, Nr_frame, alternative='two.sided', conf.level=.95, paired=TRUE)))
 # 
 # Paired t-test
 # 
 # data:  Xdoc and Nr_frame
 # t = -7.542, df = 34, p-value = 0.000000009308
 # alternative hypothesis: true difference in means is not equal to 0
 # 95 percent confidence interval:
 #   -1598.3552  -919.8162
 # sample estimates:
 #   mean of the differences 
 # -1259.086 
   
  Dataset <- readXL("analysis.xlsx", rownames=FALSE, header=TRUE, na="", sheet="y_f_back_and_int", stringsAsFactors=TRUE)

   
 with(Dataset, (t.test(Ydoc, Nr_frame, alternative='two.sided', conf.level=.95, paired=TRUE)))
   
   # Paired t-test
   # 
   # data:  Ydoc and Nr_frame
   # t = -9.5395, df = 34, p-value = 3.846e-11
   # alternative hypothesis: true difference in means is not equal to 0
   # 95 percent confidence interval:
   #   -1826.656 -1185.058
   # sample estimates:
   #   mean of the differences 
   # -1505.857 