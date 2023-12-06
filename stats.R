# Imports
library(ggplot2)
library(ggpubr)
library(rstatix)
library(tools)

# https://www.datanovia.com/en/blog/how-to-add-p-values-to-ggplot-facets/
df <- read.csv("~/Code/hci-vr-app/data/results.csv")
metrics <- c("accuracy", "throughput", "efficiency", "overshoots")
online_metrics <- c("overshoots", "throughput", "efficiency")

wilcoxon_box_plot <- function(metric) {
  formula <- as.formula(paste(metric, "~ method"))
  cutpoints = c(0, 1e-04, 0.001, 0.01, 0.05, 1)
  if (metric %in% online_metrics) {
    # Divide by number of online metrics (bonferroni correction)
    print(metric)
    cutpoints <- cutpoints / length(online_metrics)
  }
  stat.test <- df %>%
    wilcox_test(formula, paired = TRUE) %>%
    add_significance()
  
  # Create a box plot
  ylab <- toTitleCase(metric) # capitalize
  if (metric %in% c("accuracy", "efficiency")) {
    # Add % sign
    ylab <- paste(ylab, " (%)")
  }
  bxp <- ggboxplot(
    df, x = "method", y = metric, fill = "method", legend = "none",
    xlab = "Training Method", ylab = ylab
  )
  
  # Add p-values and significance
  stat.test <- stat.test %>% add_xy_position(x = "method")
  bxp <- bxp + stat_pvalue_manual(stat.test, hide.ns = FALSE, label = "{p}{p.signif}")
  return (bxp)
}

# Create plots
plots <- list()
for (metric in metrics) {
  plot <- wilcoxon_box_plot(metric)
  plots[[metric]] <- plot
}

combined_plots <- ggarrange(plotlist = plots, nrow = 2, ncol = 2)
combined_plots