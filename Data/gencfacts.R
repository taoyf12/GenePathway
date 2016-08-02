# i <- c(1,3:8)
# j <- c(2,9,6:10)
# x <- 7 * (1:7)
# X <- sparseMatrix(i, j, x = x)

load('gadj.rda')

cn = colnames(gadj)
rn = rownames(gadj)



sink("test_delete.txt")
for (r in rn) {
  cat(r)
  cat('\t')
  cat(r)
  cat('\n')
}
sink()







#fileConn<-file("test_delete.txt")

for (r in rn) {
  writeLines(c(r,'\t',r,'\n'), fileConn)
}

close(fileConn)

# for (r in rn) {
#   for (c in cn) {
#     print(gadj[r,c])
#   }
# }



# a = attributes(gadj)
# b = dimnames(gadj)[1]
#len = dim(gadj)[1]

# for (i in c(1:100)) {
#   for (j in c(1:100)) {
#     print(gadj[i][j])
#   }
# }

# write.table(gadj, file = "name.csv", append = FALSE, quote = FALSE, sep = " ",
#             eol = "\n", na = "NA", dec = ".", row.names = TRUE,
#             col.names = TRUE, qmethod = c("escape", "double"),
#             fileEncoding = "")
# 
# 
# write.table(gadj, file = "name1.csv", append = TRUE, quote = TRUE, sep = " ",
#             eol = "\n", na = "NA", dec = ".", row.names = TRUE,
#             col.names = TRUE, qmethod = c("escape", "double"),
#             fileEncoding = "")

