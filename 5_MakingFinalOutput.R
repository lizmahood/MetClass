args <- commandArgs(TRUE)

##if not all args present, print what args are needed
if (length(args) != 6){
  stop('ARGS are: 1) full path to predfile directory 2) full path to sub confusion matrices 3) full output directory path
       4) Main thresh: yes OR no 5) Sub thresh: yes OR no 6) Input file name')
}


#this thing is going to:
#read in all of the .parsed.thresh.tab files and the .pred subclass files that were just made
#for each predfil: 1) parse it. Makes "we think" column. Should also make a "precision" column 
#2) associate it with its .parsed.thresh.tab file
#3) For thresh: if precision of a row is below 0.9, we remove it.
#4) Put all classes together into final output file


preddir <- args[1]
confdir <- args[2]
outdir <- args[3]
mthresh <- args[4]
sthresh <- args[5]
innam <- args[6]

predfils <- list.files(path = preddir, pattern = '.pred', full.names = T)
outfils <- list.files(path = preddir, pattern = paste0('.thresh', toupper(mthresh), '.parsed.tab$'), full.names = T)

parse_pred <- function(predfile){

  ##removing first 2 lines
  predfile <- predfile[-c(1,2),]
  
  ##removing + and*
  predfile <- gsub('+', '', predfile, fixed = T)
  predfile <- gsub('*', '', predfile, fixed = T)
  predfile <- gsub('  ', ' ', predfile, fixed = T)
  
  predspl <- strsplit(predfile, '  ')
  predspl <-strsplit(predfile, ' ')
  
  ##getting only the necessary parts from predspl
  for (i in 1:length(predspl)){
    predspl[[i]] <- predspl[[i]][grepl('[[:punct:]]',predspl[[i]])]
  }

  ##converting to df
  preddf <- setNames(do.call(rbind.data.frame, predspl), c("actual", "predicted", "probability", "ID"))
  preddf$probability <- as.character(preddf$probability)
  preddf$actual <- as.character(preddf$actual)
  preddf$predicted <- as.character(preddf$predicted)
  preddf$ID <- as.character(preddf$ID)
  preddf$ID <- substring(preddf$ID, 3, nchar(preddf$ID)-1)
  preddf$ID <- as.integer(preddf$ID)
  return(preddf)
}

make_probVec <- function(confmat){
  probVec <- matrix(nrow = nrow(confmat), ncol = 3)
  
  for (i in 1:ncol(confmat)){
    
    ##getting the name of the predicted class
    probVec[i,1] <- as.character(colnames(confmat)[i])
    
    ##now finding %s of actuals making up that class, getting precision
    total <- sum(confmat[,i])
    percents <- round((confmat[,i]/total) * 100, digits = 2)
    prec <- confmat[i,i]/ total
    names(percents) <- colnames(confmat)
    bigPercents <- percents[which(percents > 5)]
    
    ##making a string to contain class probabilities
    names <- c()
    for (nam in 1:length(bigPercents)){
      name <- paste(names(bigPercents[as.integer(nam)]), unname(bigPercents[as.integer(nam)]), sep = ':')
      name <- paste0(name, '%')
      names <- c(names, name)
    }
    Clsprobs <- paste(names, collapse = ', ')
    probVec[i, 2] <- Clsprobs
    probVec[i, 3] <- prec
  }
  probVec[,3] <- gsub('NaN', 0, probVec[,3])
  return(probVec)
}

##making final output file
outdf <- data.frame()

for (fil in 1:length(predfils)){
  
  ##reading in the data for each class
  pred <- read.table(predfils[fil], sep = '\t', stringsAsFactors = F)
  pred_df <- parse_pred(pred)
  
  namspl <- strsplit(predfils[fil], '/')
  nam <- gsub('_output.pred', '', namspl[[1]][lengths(namspl)])
  conf <- list.files(path = confdir, pattern = nam, full.names = T)
  confm <- read.table(conf, sep = '\t', header = T, stringsAsFactors = F)
  
  ##combining the main class output for this subclass with the subclass output
  outf <- read.table(outfils[fil], sep = '\t', stringsAsFactors = F, header = T)
  full <- as.data.frame(merge(outf, pred_df, by.x = 'InstanceID', by.y ='ID'))
  full <- full[,-5]
  names(full) <- c('InstanceID', 'Main_Class', 'Main_Probability', 'Main_Precision',
                   'Subclass', 'Subclass_Probability')
  probV <- make_probVec(confm)
  rowstokeep <- c()
  weThink <- c()
  
  ##going through output file, applying threshold if wanted
  ##If the threshold is applied, we remove rows falling into classes with low precision
  for(i in 1:nrow(full)){
    rightrow <- as.integer(strsplit(full[i, 'Subclass'], ':')[[1]][1])
    prec <- probV[rightrow, 3]
    if (as.numeric(prec) == 0) {
      prec <- 0
    }
    if((sthresh == 'yes' & prec >= 0.9) | sthresh == 'no'){
      rowstokeep <- c(rowstokeep, i)
      weThink <- c(weThink, probV[rightrow, 2])
    }
  }
  
  ##removing low prec rows and adding the weThink column
  full <- full[rowstokeep,]
  
  Subclass_Precision <- weThink
  full <- cbind(full, Subclass_Precision)
  outdf <- rbind(outdf, full)
}
soutdf <- outdf[order(outdf$InstanceID),]

write.table(soutdf, file = paste0(outdir, '/', innam, '_FinalMetClassOutput_mainThresh', 
                                 toupper(mthresh), 'subThresh', toupper(sthresh), '.tab'),
            sep = '\t', row.names = F, quote = F)

print('Done!')
