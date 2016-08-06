load('../TDI_dump/gadj.rda')

cn = colnames(gadj)
rn = rownames(gadj)

sink("../TDI_dump/pathway.cfacts")
for (r in rn) {
  for (c in cn) {
    if (gadj[r,c] == 1) {
      cat('leadTo')
      cat('\t')
      cat(r)
      cat('\t')
      cat(c)
      cat('\n')
      cat('resultFrom')
      cat('\t')
      cat(c)
      cat('\t')
      cat(r)
      cat('\n')
    }
  }
}
sink()

print('Done!')

