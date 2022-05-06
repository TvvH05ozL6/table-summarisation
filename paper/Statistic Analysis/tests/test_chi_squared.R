 library(abind, pos=17)

  .Table <- matrix(c(712,749,562,569,565,714,482,669,19,18,13,15), 3, 4, byrow=TRUE)

dimnames(.Table) <- list("rows"=c("Xdoc", "Ydoc", "NFrame"), "columns"=c("back_and_int", "back_not_int", "int_not_back", "not_back_int"))

  .Table  # Counts
  # columns
  # rows     back_and_int back_not_int int_not_back not_back_int
  # Xdoc            712          749          562          569
  # Ydoc            565          714          482          669
  # NFrame           19           18           13           15

 rowPercents(.Table) # Row Percentages
 # columns
 # rows     back_and_int back_not_int int_not_back not_back_int Total Count
 # Xdoc           27.5         28.9         21.7         22.0 100.1  2592
 # Ydoc           23.3         29.4         19.8         27.5 100.0  2430
 # NFrame         29.2         27.7         20.0         23.1 100.0    65

  .Test <- chisq.test(.Table, correct=FALSE)
  .Test

# Pearson's Chi-squared test
# 
# data:  .Table
# X-squared = 27.26, df = 6, p-value = 0.0001294