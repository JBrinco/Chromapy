#!/bin/R

library("rsm")
library("ggplot2")


first_var_names <- list("run.order", "std.order")
last_var_name <- list("Results")
var_names <- list("Inj_Temp", "Inj_Time", "Source_Temp")
vls <- list(250, 60, 260, 10, 290)
dvt <- list(15, 30, 20, 2, 20)

# design <- bbd(5, block = FALSE,  coding =
#     list(x1 ~ (a - values[[1]])/deviation[[1]], x2 ~ (b - values[[2]])/deviation[[2]], x3 ~ (c - values[[3]])/deviation[[3]], x4 ~ (d - values[[4]])/deviation[[4]], x5 ~ (e - values[[5]])/deviation[[5]]  ))

Factors_number <- 3
design <- bbd(Factors_number, block = FALSE, randomize = FALSE,  coding =
    list(x1 ~ (a - vls[[1]])/dvt[[1]], x2 ~ (b - vls[[2]])/dvt[[2]], x3 ~ (c - vls[[3]])/dvt[[3]] ))



# print(design)

design_out <- decode.data(design)

# results <- c(7, 7, 7, 9, 9, 9, 7, 9, 10, 9, 10, 6, 10, 6, 6, 7)
# results <- c(6, 9, 6, 9, 9, 14, 7, 14, 7, 14, 14, 6, 7, 9, 6, 7)
results <- c(7, 7, 6, 5, 9, 10, 8, 8, 6, 7, 6, 5, 13, 14, 13, 12) # Near Perfect-fit data, DO NOT RANDOMIZE BBD!

design_out$Results <- results


design_results <- coded.data(design_out, formulas =
    list(x1 ~ (a - vls[[1]])/dvt[[1]], x2 ~ (b - vls[[2]])/dvt[[2]], x3 ~ (c - vls[[3]])/dvt[[3]] ))


variable_names <- c(first_var_names, var_names, last_var_name)

## For this to work, no two letters of the variable name can be in the list names for the coding variables (vls and dvt). It will add the new variable names in the middle of "vls" or "dvt" and the variables will not work properly.
# truenames(design_results) <- list("run.order", "std.order", "Vaira1", "Vaira2", "Varia3", "Results")
truenames(design_results) <- variable_names
# print(names(design_results))
# print(design_results)
# print(truenames(design_results))


# print(design_results)

# print(as.data.frame(design_results))
# print(design_results)

# design_results.rsm <- rsm(Results ~ FO(x1, x2, x3), data = design_results)
# design_results.rsmi <- update(design_results.rsm, . ~ . +  TWI(x1, x2, x3))

design_results.rsm <- rsm(Results ~ SO(x1, x2, x3), data = design_results)

# summary(design_results.rsm)
print("----")
# attributes(design_results.rsm)
cat("Stationary point of response surface:\n")
print(canonical(design_results.rsm)$xs)
cat("\nStationary point in original units:\n")
print (code2val (canonical(design_results.rsm)$xs, design_results.rsm$coding))

pdf(file = "Output_Plot.pdf")

# par(mfrow = c(3, 3))
contour(design_results.rsm, ~ x1 + x2 + x3, image =TRUE)
image(design_results.rsm, ~ x1 + x2 + x3)
contour(design_results.rsm, ~ x1 + x2 + x3, image =TRUE, at = summary(design_results.rsm$canonical$xs))
persp(design_results.rsm, ~ x1 + x2 + x3)

# Generates a hook on the stationary point, so that we can plot around it!
xs <- canonical(design_results.rsm)$xs
myhook <- list()
myhook$post.plot <- function(lab) {
idx <- sapply(lab[3:4], grep, names(xs))
points (xs[idx[1]], xs[idx[2]], pch=2, col="red")}

contour (design_results.rsm, ~ x1 + x2 + x3, image = TRUE,
at = xs, hook = myhook)

persp (design_results.rsm, ~ x1 + x2 + x3, at = xs, col = rainbow(50), contours = "colors")
persp (design_results.rsm, ~ x1 + x2 + x3, at = xs, col = rainbow(50), contours = "colors", hook = myhook)

# dev.off()


# write.csv(design_out, "BBD.csv", row.names=FALSE)



# design_2 <- bbd(y1 + y2 ~ A + B + C + D + E,  n0 = 5,  block = "Plant")
# as.data.frame(design)    Shows coded data, not the dataframe I want to see
# print(design_2)
