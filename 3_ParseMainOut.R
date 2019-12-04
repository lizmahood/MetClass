args <- commandArgs(TRUE)
#print(length(args))
##if not all args present, print what args are needed
if (length(args) != 4){
  stop('ARGS are: 1 full path to predfile 2 full path to MAIN confusion matrix 3) full output directory path
       4) Thresh: yes OR no')
}

prednam <- args[1]
conf <- args[2]
outdir <- args[3]
thresh <- args[4]

##reading in conf matrix
confmat <- read.table(conf, sep = '\t', header = T, stringsAsFactors = F)

##reading in pred file
predfile <- read.table(prednam, sep = '\t', stringsAsFactors = F)

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

condProbClass <- function(df, confmat){
  ##This function takes preddf and the confusion matrix as input.
  ##For each instance in the preddf, it finds the class it was 
  ##predicted as, checks the distribution of Actuals that 
  ##were predicted as that class, and outputs this info
  ##WRITES OUT: tsv, TAB1: inst #, 2: predicted class,
  ##3: prob of being other classes, 4: Ins ID
  
  ##making a vector of conditional probabilities per predicted class
  probVec <- matrix(nrow = nrow(confmat), ncol = 2)
  
  for (i in 1:ncol(confmat)){
    
    ##getting the name of the predicted class
    probVec[i,1] <- as.character(colnames(confmat)[i])
    
    ##now finding %s of actuals making up that class, getting precision
    total <- sum(confmat[,i])
    percents <- round((confmat[,i]/total) * 100, digits = 2)
    names(percents) <- colnames(confmat)
    #bigPercents <-unname(which(apply(percents, 2, function(x) {x >= 5})))
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
  }

  ##writing first line of output file
  print('Writing out Probabilities_for_Prediction files. Do not open them before the script completes!')
  
  for (i in unique(df$predicted)){
    print(paste0('Working on ', i))
    rightcol <- as.integer(substr(i, 1,1))
    prec <- confmat[rightcol, rightcol] / sum(confmat[,rightcol])
    if (is.nan(prec) == T) prec <- 0
    subdf <- df[df$predicted == i, ]
    
    if ((prec >= 0.9 & thresh == 'yes') | thresh == 'no'){
      sink(paste0(outdir, '/', gsub(':', '\\.', i), '.thresh', toupper(thresh), '.parsed.tab'))
      cat(paste0('InstanceID\tPredicted\tProbability\tPrecision\n'))
      
      ##now looping through preddf, finding Clsprobs for each instance
      for (j in 1:nrow(subdf)){
        cls <- paste0('X', gsub(':', '\\.', subdf[j, 'predicted']))
        Clsprobs <- probVec[,2][which(probVec[,1] == cls)]
        outstr <- paste0(substr(subdf[j, 'ID'], 3, nchar(subdf[j, 'ID'])-1),
                         '\t', cls, '\t', subdf[j, 'probability'],'\t', Clsprobs, '\n')
        cat(outstr)
      }
      sink()
    }
  }  
}

condProbClass(preddf, confmat)

print('Done!')
  