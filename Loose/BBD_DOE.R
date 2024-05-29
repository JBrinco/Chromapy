#!/bin/R

library("rsm")


#Fixed variables to help set the correct names later
first_var_names <- list("run.order", "std.order")
last_var_name <- list("Results")

# These will eventually be parsed from the input data and give all we need for the calculations
var_names <- list("Inj_Temp", "Inj_Time", "Source_Temp")
vls <- list(250, 60, 260, 10, 290) #Center values for each variable
dvt <- list(15, 30, 20, 2, 20) # deviations, +-. For example, 250+- 15, which is 235, 250 and 265.
results <- c(7, 7, 6, 5, 9, 10, 8, 8, 6, 7, 6, 5, 13, 14, 13, 12) # Near Perfect-fit data, DO NOT RANDOMIZE BBD! It will be randomized in production, but for now it would loose it's perfect fit



# Box-Behnken design generation, needs an if elif for handling different number of factors. This has to be hardcoded because rsm is not built for this stuff
Factors_number <- 3
if (Factors_number == 2) {
	design <- bbd(Factors_number, block = FALSE, randomize = FALSE,  coding = list(x1 ~ (a - vls[[1]])/dvt[[1]], x2 ~ (b - vls[[2]])/dvt[[2]] ))

} else if (Factors_number == 3) {
	design <- bbd(Factors_number, block = FALSE, randomize = FALSE,  coding = list(x1 ~ (a - vls[[1]])/dvt[[1]], x2 ~ (b - vls[[2]])/dvt[[2]], x3 ~ (c - vls[[3]])/dvt[[3]] ))

} else if  (Factors_number == 4) {
	design <- bbd(Factors_number, block = FALSE, randomize = FALSE,  coding = list(x1 ~ (a - vls[[1]])/dvt[[1]], x2 ~ (b - vls[[2]])/dvt[[2]], x3 ~ (c - vls[[3]])/dvt[[3]]))

} else if (Factors_number == 5) {
	design <- bbd(Factors_number, block = FALSE, randomize = FALSE,  coding = list(x1 ~ (a - vls[[1]])/dvt[[1]], x2 ~ (b - vls[[2]])/dvt[[2]], x3 ~ (c - vls[[3]])/dvt[[3]] , x4 ~ (c - vls[[4]])/dvt[[4]] , x5 ~ (c - vls[[5]])/dvt[[5]]))

} else if (Factors_number == 6) {
	design <- bbd(Factors_number, block = FALSE, randomize = FALSE,  coding = list(x1 ~ (a - vls[[1]])/dvt[[1]], x2 ~ (b - vls[[2]])/dvt[[2]], x3 ~ (c - vls[[3]])/dvt[[3]] , x4 ~ (c - vls[[4]])/dvt[[4]] , x5 ~ (c - vls[[5]])/dvt[[5]] , x6 ~ (c - vls[[6]])/dvt[[6]]))

} else if (Factors_number == 7) {
	design <- bbd(Factors_number, block = FALSE, randomize = FALSE,  coding = list(x1 ~ (a - vls[[1]])/dvt[[1]], x2 ~ (b - vls[[2]])/dvt[[2]], x3 ~ (c - vls[[3]])/dvt[[3]] , x4 ~ (c - vls[[4]])/dvt[[4]] , x5 ~ (c - vls[[5]])/dvt[[5]] , x6 ~ (c - vls[[6]])/dvt[[6]] , x7 ~ (c - vls[[7]])/dvt[[7]]))

} else{
	print("Unrecognized or unsuported number of Factors (variables)")}


# Output data after generating the design
write.csv(decode.data(design), "Path to export the DataFrame\\File Name.csv", row.names=FALSE)

# Import results from csv. Ideally the entire dataframe, the same as was exported, but with a "Results" column. Here it adds the results vector from above
design_out <- decode.data(design)
design_out$Results <- results


# Re-code the design into the dataframe. Will need if-else as above.
design_results <- coded.data(design_out, formulas =
    list(x1 ~ (a - vls[[1]])/dvt[[1]], x2 ~ (b - vls[[2]])/dvt[[2]], x3 ~ (c - vls[[3]])/dvt[[3]] ))

# Merges all the variable names changes the "a", "b", etc. for them.
variable_names <- c(first_var_names, var_names, last_var_name)
truenames(design_results) <- variable_names


# Generate the response-surface model. SO creates FO (first-order), TWI (two-way interactions) and PQ (pure-quadratic terms), in that order.
design_results.rsm <- rsm(Results ~ SO(x1, x2, x3), data = design_results)

#Summary of results
summary(design_results.rsm)

#Stationary point. The eigenvalues should be within -1 to 1, which means the stationary point is within the experiment boundaries
cat("Stationary point of response surface:\nShould be within -1 to 1, which means it is within the experiment boundaries")
print(canonical(design_results.rsm)$xs)
cat("\nStationary point in original units:\n")
print (code2val (canonical(design_results.rsm)$xs, design_results.rsm$coding))

#Some graphical output. Still working on it.
par(mfrow = c(3, 3))
contour(design_results.rsm, ~ x1 + x2 + x3, image =TRUE)
image(design_results.rsm, ~ x1 + x2 + x3)
contour(design_results.rsm, ~ x1 + x2 + x3, image =TRUE, at = summary(design_results.rsm$canonical$xs))


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

contour (design_results.rsm, ~ x1 + x2 + x3, image = TRUE, at = xs, hook = myhook)

persp (design_results.rsm, ~ x1 + x2 + x3, at = xs, col = rainbow(50), contours = "colors")
persp (design_results.rsm, ~ x1 + x2 + x3, at = xs, col = rainbow(50), contours = "colors", hook = myhook)

# dev.off()
