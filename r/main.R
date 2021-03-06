# Load most commonly used libraries

list.of.packages <- c("tidyverse", "magrittr")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)

library(tidyverse)
library(magrittr)

# ---- begin ----
# Step One: Load Data:
source("code/load.R")

# ---- analysis ----
# Step Two: Analyzing data for report:
source("code/analysis.R")

# ---- plot ----
# Step Three: Analyzing data for report:
source("code/plots/plots.R")

# ---- render ----
# Step Four: Knitting Report
rmarkdown::render("rmd/","github_document", "../analysis/")
